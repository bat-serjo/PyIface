from .iface import Interface, getIfaces
from .ifreqioctls import *

__all__ = ['Interface', 'getIfaces']

ll = dir()
for l in ll:
    if l.startswith('IFF_'):
        __all__.append(l)
    if l.startswith('SIOC'):
        __all__.append(l)

