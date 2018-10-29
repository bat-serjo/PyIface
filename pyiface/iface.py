from __future__ import absolute_import
import sys
import fcntl
import struct
import socket

from ctypes import *
from .ifreqioctls import *
from binascii import hexlify
from os import listdir

flags2str = {
    IFF_UP: 'Interface is up.',
    IFF_BROADCAST: 'Broadcast address valid.',
    IFF_DEBUG: 'Turn on debugging.',
    IFF_LOOPBACK: 'Is a loopback net.',
    IFF_POINTOPOINT: 'Interface is point-to-point link.',
    IFF_NOTRAILERS: 'Avoid use of trailers.',
    IFF_RUNNING: 'Resources allocated.',
    IFF_NOARP: 'No address resolution protocol.',
    IFF_PROMISC: 'Receive all packets.',
    IFF_ALLMULTI: 'Receive all multicast packets.',
    IFF_MASTER: 'Master of a load balancer.',
    IFF_SLAVE: 'Slave of a load balancer.',
    IFF_MULTICAST: 'Supports multicast.',
    IFF_PORTSEL: 'Can set media type.',
    IFF_AUTOMEDIA: 'Auto media select active.',
    IFF_DYNAMIC: 'Dialup device with changing addresses.'
}


def flagsToStr(fin):
    ret = ''
    for k in flags2str.keys():
        if fin & k:
            ret = ret + '\t' + flags2str[k] + '\n'

    return ret


class sockaddr_gen(Structure):
    _fields_ = [
        ("sa_family", c_uint16),
        ("sa_data", (c_uint8 * 22))
    ]


# AF_INET / IPv4
class in_addr(Structure):
    _pack_ = 1
    _fields_ = [
        ("s_addr", c_uint32),
    ]


class sockaddr_in(Structure):
    _pack_ = 1
    _fields_ = [
        ("sin_family", c_ushort),
        ("sin_port", c_ushort),
        ("sin_addr", in_addr),
        ("sin_zero", (c_uint8 * 16)),  # padding
    ]


# AF_INET6 / IPv6
class in6_u(Union):
    _pack_ = 1
    _fields_ = [
        ("u6_addr8", (c_uint8 * 16)),
        ("u6_addr16", (c_uint16 * 8)),
        ("u6_addr32", (c_uint32 * 4))
    ]


class in6_addr(Structure):
    _pack_ = 1
    _fields_ = [
        ("in6_u", in6_u),
    ]


class sockaddr_in6(Structure):
    _pack_ = 1
    _fields_ = [
        ("sin6_family", c_short),
        ("sin6_port", c_ushort),
        ("sin6_flowinfo", c_uint32),
        ("sin6_addr", in6_addr),
        ("sin6_scope_id", c_uint32),
    ]


# AF_LINK / BSD|OSX
class sockaddr_dl(Structure):
    _fields_ = [
        ("sdl_len", c_uint8),
        ("sdl_family", c_uint8),
        ("sdl_index", c_uint16),
        ("sdl_type", c_uint8),
        ("sdl_nlen", c_uint8),
        ("sdl_alen", c_uint8),
        ("sdl_slen", c_uint8)
        #        ("sdl_data",   (c_uint8 * 46) )
    ]


class sockaddr(Union):
    _pack_ = 1
    _fields_ = [
        ('gen', sockaddr_gen),
        ('in4', sockaddr_in),
        ('in6', sockaddr_in6)
    ]


class ifmap(Structure):
    _pack_ = 1
    _fields_ = [
        ('mem_start', c_ulong),
        ('mem_end', c_ulong),
        ('base_addr', c_ushort),
        ('irq', c_ubyte),
        ('dma', c_ubyte),
        ('port', c_ubyte)
    ]


IFNAMSIZ = 16
IFHWADDRLEN = 6


class ifr_data(Union):
    _pack_ = 1
    _fields_ = [
        ('ifr_addr', sockaddr),
        ('ifr_dstaddr', sockaddr),
        ('ifr_broadaddr', sockaddr),
        ('ifr_netmask', sockaddr),
        ('ifr_hwaddr', sockaddr),
        ('ifr_flags', c_short),
        ('ifr_ifindex', c_int),
        ('ifr_ifqlen', c_int),
        ('ifr_metric', c_int),
        ('ifr_mtu', c_int),
        ('ifr_map', ifmap),
        ('ifr_slave', (c_ubyte * IFNAMSIZ)),
        ('ifr_newname', (c_ubyte * IFNAMSIZ)),
        ('ifr_data', c_void_p)
    ]


class ifreq(Structure):
    _pack_ = 1
    _fields_ = [
        ('ifr_name', (c_ubyte * IFNAMSIZ)),
        ('data', ifr_data)
    ]


class in6_ifreq(Structure):
    _pack_ = 1
    _fields_ = [
        ('addr', in6_addr),
        ('prefixlen', c_uint32),
        ('ifindex', c_int)
    ]


class Interface(object):
    """
    Represents a network interface.
    
    Almost all interesting attributes are exported in the form
    of a variable. You can get or set this variable. For example:
    
    ifeth0 = Interface("eth0")
    print ifeth0.addr  # will print the current address
    ...
    or
    ...
    ifeth0.addr = (AF_INET, '1.2.3.4') # will set a new address
    
    """

    def __init__(self, idx=1, name=None):
        self._af_mode = socket.AF_INET

        self._index = idx
        self._name = name

        # Get the name of the interface
        if self._name is None:
            self._name = self.name
        else:
            self._name = (c_ubyte * IFNAMSIZ)(*bytearray(self._name.encode('utf8')))
            self._index = self.index

    def __newIfreqWithName(self):
        ifr = ifreq()
        ifr.ifr_name = (c_ubyte * IFNAMSIZ)(*bytearray(self._name))
        return ifr

    def __doIoctl(self, ifr, SIOC, mutate=True):
        try:
            skt = socket.socket(self._af_mode, socket.SOCK_DGRAM, 0)
            fcntl.fcntl(skt,
                        fcntl.F_SETFD,
                        fcntl.fcntl(skt, fcntl.F_GETFD) | fcntl.FD_CLOEXEC)
            fcntl.ioctl(skt, SIOC, ifr, mutate)
        except IOError as ioException:
            if ioException.errno == 99 or ioException.errno == 17:
                pass
            else:
                raise ioException
        finally:
            if skt:
                skt.close()

    def __getSimple(self, ioctl, elem):
        ifr = self.__newIfreqWithName()
        self.__doIoctl(ifr, ioctl)

        elem = elem.split('.')
        tmpVal = ifr
        for curElem in elem:
            tmpVal = getattr(tmpVal, curElem)

        return tmpVal

    def __setSimple(self, ioctl, elem, val):
        ifr = self.__newIfreqWithName()

        elem = elem.split('.')
        tmpVal = ifr

        for curElem in elem[:-1]:
            tmpVal = getattr(tmpVal, curElem)

        setattr(tmpVal, elem[-1], val)
        self.__doIoctl(ifr, ioctl)

    @property
    def index(self):
        ifr = self.__newIfreqWithName()
        self.__doIoctl(ifr, SIOCGIFINDEX)
        self._index = ifr.data.ifr_ifindex
        return self._index

    @property
    def name(self):
        ifr = ifreq()
        ifr.data.ifr_ifindex = self._index
        self.__doIoctl(ifr, SIOCGIFNAME)
        self._name = ifr.ifr_name
        return string_at(self._name).decode('utf8', 'backslashreplace')

    @name.setter
    def name(self, val):
        ifr = ifreq()
        ifr.ifr_name = self._name
        ifr.data.ifr_newname = val
        self.__doIoctl(ifr, SIOCGIFNAME)
        self._name = val

    @property
    def flags(self):
        return self.__getSimple(SIOCGIFFLAGS, 'data.ifr_flags')

    @flags.setter
    def flags(self, val):
        self.__setSimple(SIOCSIFFLAGS, 'data.ifr_flags', val)

    @property
    def ifqlen(self):
        return self.__getSimple(SIOCGIFTXQLEN, 'data.ifr_ifqlen')

    @ifqlen.setter
    def ifqlen(self, val):
        self.__setSimple(SIOCSIFTXQLEN, 'data.ifr_ifqlen', val)

    @property
    def metric(self):
        return self.__getSimple(SIOCGIFMETRIC, 'data.ifr_metric')

    @metric.setter
    def metric(self, val):
        self.__getSimple(SIOCSIFMETRIC, 'data.ifr_metric', val)

    @property
    def mtu(self):
        return self.__getSimple(SIOCGIFMTU, 'data.ifr_mtu')

    @mtu.setter
    def mtu(self, val):
        self.__getSimple(SIOCSIFMTU, 'data.ifr_mtu', val)

    @property
    def hwaddr(self):
        ifr = self.__newIfreqWithName()
        self.__doIoctl(ifr, SIOCGIFHWADDR)
        hw = ifr.data.ifr_hwaddr.gen.sa_data

        self._hwaddr = ''
        for i in hw[:IFHWADDRLEN]:
            self._hwaddr = self._hwaddr + '%.2X:' % i

        return self._hwaddr

    @hwaddr.setter
    def hwaddr(self, val):
        ifr = self.__newIfreqWithName()
        ifr.data.ifr_hwaddr.sin_addr.s_addr = val
        self.__doIoctl(ifr, SIOCSIFHWADDR)

    @property
    def addr(self):
        ifr = self.__newIfreqWithName()
        self.__doIoctl(ifr, SIOCGIFADDR)
        return ifr.data.ifr_addr

    @addr.setter
    def addr(self, val):
        ifr = self.__newIfreqWithName()
        ifr.data.ifr_addr = self.__sockaddrFromTuple(val)

        if self._af_mode == socket.AF_INET6:
            ifr6 = in6_ifreq()
            ifr6.ifindex = self.index
            ifr6.prefixlen = 64
            ifr6.addr = ifr.data.ifr_addr.in6.sin6_addr
            self.__doIoctl(ifr6, SIOCSIFADDR, False)
        else:
            self.__doIoctl(ifr, SIOCSIFADDR, False)

        self._af_mode = socket.AF_INET

    @property
    def broadaddr(self):
        ifr = self.__newIfreqWithName()
        self.__doIoctl(ifr, SIOCGIFBRDADDR)
        return ifr.data.ifr_broadaddr

    @broadaddr.setter
    def broadaddr(self, val):
        ifr = self.__newIfreqWithName()
        ifr.data.ifr_broadaddr = self.__sockaddrFromTuple(val)
        self.__doIoctl(ifr, SIOCSIFBRDADDR)

    @property
    def netmask(self):
        ifr = self.__newIfreqWithName()
        self.__doIoctl(ifr, SIOCGIFNETMASK)
        return ifr.data.ifr_netmask

    @netmask.setter
    def netmask(self, val):
        ifr = self.__newIfreqWithName()
        ifr.data.ifr_netmask = self.__sockaddrFromTuple(val)
        self.__doIoctl(ifr, SIOCSIFNETMASK, False)

    @staticmethod
    def __getSinAddr(sockaddr):
        if sockaddr.gen.sa_family == socket.AF_INET:
            return sockaddr.in4.sin_addr.s_addr
        if sockaddr.gen.sa_family == socket.AF_INET6:
            return sockaddr.in6.sin6_addr.in6_u
        return 0

    def __sockaddrFromTuple(self, inVal):
        if inVal[0] == socket.AF_INET:
            self._af_mode = socket.AF_INET
            sin4 = sockaddr()

            sin4.in4.sin_family = inVal[0]
            sin4.in4.sin_addr.s_addr = struct.unpack('<L', socket.inet_pton(
                inVal[0],
                inVal[1]))[0]
            return sin4

        elif inVal[0] == socket.AF_INET6:
            self._af_mode = socket.AF_INET6

            sin6 = sockaddr()
            sin6.in6.sin6_family = inVal[0]
            sin6.in6.sin6_addr.in6_u = in6_u((c_ubyte*16)(*bytearray(socket.inet_pton(
                inVal[0],
                inVal[1]))))
            return sin6

        raise Exception("Input must be tuple like (AF_INET, '127.0.0.1')")

    def sockaddrToStr(self, sockaddr):
        if sockaddr.gen.sa_family == 0:
            return 'None'

        p = struct.pack('<L', self.__getSinAddr(sockaddr))
        return socket.inet_ntop(sockaddr.gen.sa_family, p)

    def __str__(self):
        x = ''
        x = x + 'Iface: %s Index: %d HWAddr: %s\n' % (
            self.name,
            self._index,
            self.hwaddr)

        x = x + 'Addr:%s Bcast:%s Mask:%s\n' % (
            self.sockaddrToStr(self.addr),
            self.sockaddrToStr(self.broadaddr),
            self.sockaddrToStr(self.netmask))
        x = x + 'MTU: %d Metric: %d Txqueuelen: %d\n' % (
            self.mtu,
            self.metric + 1,
            self.ifqlen)
        x = x + 'Flags:\n%s' % flagsToStr(self.flags)
        return x


def getIfaces():
    """
    Returns a list of all available interfaces.
    """
    ret = []
    interfaces = listdir('/sys/class/net')
    for interface in interfaces:
        try:
            ifa = Interface(name=interface.lower())
            ret.append(ifa)
        except IOError:
            continue
    return ret


if __name__ == '__main__':
    print('All your interfaces')
    allIfaces = getIfaces()
    for iface in allIfaces:
        print(iface)

    iff = Interface(name='eth0')
    iff.flags = iff.flags & ~IFF_UP
    print(iff)
    iff.flags = iff.flags | IFF_UP | IFF_RUNNING
    iff.addr = (socket.AF_INET, sys.argv[1])
    print(iff)
    iff.netmask = (socket.AF_INET, sys.argv[2])
    print(iff)
    iff.addr = (socket.AF_INET6, '2001::0')
    print(iff)
    iff.flags = iff.flags | IFF_UP
    print(iff)
    iff.flags = iff.flags & ~IFF_UP
    print(iff)
