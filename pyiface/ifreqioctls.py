# Complete list of ifreq flags for linux as of2013

IFF_UP          = 0x1
IFF_BROADCAST   = 0x2
IFF_DEBUG       = 0x4
IFF_LOOPBACK    = 0x8
IFF_POINTOPOINT = 0x10
IFF_NOTRAILERS  = 0x20
IFF_RUNNING     = 0x40
IFF_NOARP       = 0x80
IFF_PROMISC     = 0x100
IFF_ALLMULTI    = 0x200
IFF_MASTER      = 0x400
IFF_SLAVE       = 0x800
IFF_MULTICAST   = 0x1000
IFF_PORTSEL     = 0x2000
IFF_AUTOMEDIA   = 0x4000
IFF_DYNAMIC     = 0x8000 


#Incomplete list of most IOCTLs used to control interfaces

SIOCADDRT       = 0x0000890B # ['const', 'struct', 'rtentry', '*', '//', 'MORE']
SIOCDELRT       = 0x0000890C # ['const', 'struct', 'rtentry', '*', '//', 'MORE']
SIOCGIFNAME     = 0x00008910 # ['char', '[]']
SIOCSIFLINK     = 0x00008911 # ['void']
SIOCGIFCONF     = 0x00008912 # ['struct', 'ifconf', '*', '//', 'MORE', '//', 'I-O']
SIOCGIFFLAGS    = 0x00008913 # ['struct', 'ifreq', '*', '//', 'I-O']
SIOCSIFFLAGS    = 0x00008914 # ['const', 'struct', 'ifreq', '*']
SIOCGIFINDEX    = 0x00008933 # [ifr_ifindex]
SIOCGIFADDR     = 0x00008915 # ['struct', 'ifreq', '*', '//', 'I-O']
SIOCSIFADDR     = 0x00008916 # ['const', 'struct', 'ifreq', '*']
SIOCGIFDSTADDR  = 0x00008917 # ['struct', 'ifreq', '*', '//', 'I-O']
SIOCSIFDSTADDR  = 0x00008918 # ['const', 'struct', 'ifreq', '*']
SIOCGIFBRDADDR  = 0x00008919 # ['struct', 'ifreq', '*', '//', 'I-O']
SIOCSIFBRDADDR  = 0x0000891A # ['const', 'struct', 'ifreq', '*']
SIOCGIFNETMASK  = 0x0000891B # ['struct', 'ifreq', '*', '//', 'I-O']
SIOCSIFNETMASK  = 0x0000891C # ['const', 'struct', 'ifreq', '*']
SIOCGIFMETRIC   = 0x0000891D # ['struct', 'ifreq', '*', '//', 'I-O']
SIOCSIFMETRIC   = 0x0000891E # ['const', 'struct', 'ifreq', '*']
SIOCGIFMEM      = 0x0000891F # ['struct', 'ifreq', '*', '//', 'I-O']
SIOCSIFMEM      = 0x00008920 # ['const', 'struct', 'ifreq', '*']
SIOCGIFMTU      = 0x00008921 # ['struct', 'ifreq', '*', '//', 'I-O']
SIOCSIFMTU      = 0x00008922 # ['const', 'struct', 'ifreq', '*']
OLD_SIOCGIFHWADDR = 0x00008923 # ['struct', 'ifreq', '*', '//', 'I-O']
SIOCSIFHWADDR   = 0x00008924 # ['const', 'struct', 'ifreq', '*', '//', 'MORE']
SIOCGIFENCAP    = 0x00008925 # ['int', '*']
SIOCSIFENCAP    = 0x00008926 # ['const', 'int', '*']
SIOCGIFHWADDR   = 0x00008927 # ['struct', 'ifreq', '*', '//', 'I-O']
SIOCGIFSLAVE    = 0x00008929 # ['void']
SIOCSIFSLAVE    = 0x00008930 # ['void']
SIOCADDMULTI    = 0x00008931 # ['const', 'struct', 'ifreq', '*']
SIOCDELMULTI    = 0x00008932 # ['const', 'struct', 'ifreq', '*']
SIOCADDRTOLD    = 0x00008940 # ['void']
SIOCDELRTOLD    = 0x00008941 # ['void']
SIOCGIFTXQLEN   = 0x00008942 # ['ifr_ifqlen']
SIOCSIFTXQLEN   = 0x00008943 # ['ifr_ifqlen']     
SIOCDARP        = 0x00008950 # ['const', 'struct', 'arpreq', '*']
SIOCGARP        = 0x00008951 # ['struct', 'arpreq', '*', '//', 'I-O']
SIOCSARP        = 0x00008952 # ['const', 'struct', 'arpreq', '*']
SIOCDRARP       = 0x00008960 # ['const', 'struct', 'arpreq', '*']
SIOCGRARP       = 0x00008961 # ['struct', 'arpreq', '*', '//', 'I-O']
SIOCSRARP       = 0x00008962 # ['const', 'struct', 'arpreq', '*']
SIOCGIFMAP      = 0x00008970 # ['struct', 'ifreq', '*', '//', 'I-O']
SIOCSIFMAP      = 0x00008971 # ['const', 'struct', 'ifreq', '*']
