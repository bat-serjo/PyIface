Python access network interfaces
================================

General information
-------------------

Pyiface is a package that exposes the network interfaces of the operating
system in an easy to use and transparent way. Typical usage looks like this:

.. code-block:: python

    #!/usr/bin/env python
    
    import pyiface
    from pyiface.ifreqioctls import IFF_UP
    
    # Get all available network interfaces
    allIfaces = pyiface.getIfaces()
    for iface in allIfaces:
        print(iface)
    
    # Get a specific interface by name
    eth0 = pyiface.Interface(name='eth0')
    
    # view eth0 info
    print(eth0)
    
    # bring eth0 up
    eth0.flags = eth0.flags | IFF_UP
    
    # set ipv4 address of the interface
    eth0.addr = (socket.AF_INET, '1.2.3.4')
    
    # set ipv6 address of the interface
    eth0.addr = (socket.AF_INET6, '2001:0db8:85a3:0000:0000:8a2e:0370:7334')


Installation
------------

To install the package simply call `setup.py` with the install option.

Links
-----

For more information go to my `blogspot  <http://python-a-day.blogspot.com>`_.
Or browse the `github  <https://github.com/bat-serjo/PyIface>`_ repository.
