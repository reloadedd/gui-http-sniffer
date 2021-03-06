import struct
import ipaddress

from ..exceptions.network import UnsupportedVersionException


class Layer3:
    """Parse the layer 3 data of a packet.

    Attributes
    ----------
    version : int
        The IP protocol version.
    source_ip : IPv4Address
        The source IP address of the packet.
    dest_ip : IPv4Address
        The destination IP address of the packet.
    """
    IP_VERSION_4 = 0x45

    def __init__(self, packet_bytes: bytes):
        # Ignoring 11 bytes
        ip_header = struct.unpack('!B11s4s4s', packet_bytes[14:34])

        self.version = ip_header[0]

        if self.version != Layer3.IP_VERSION_4:
            raise UnsupportedVersionException('Only IPv4 is supported')

        self.source_ip = ipaddress.IPv4Address(ip_header[2])
        self.dest_ip = ipaddress.IPv4Address(ip_header[3])


class Layer4:
    """Parse the layer 4 data of a packet.

    Attributes
    ----------
    source_port : int
        The source port.
    dest_port : int
        The destination port.
    """
    def __init__(self, packet_bytes: bytes):
        # Ignoring 28 bytes
        tcp_header = struct.unpack('!HH28s', packet_bytes[34:66])

        self.source_port = tcp_header[0]
        self.dest_port = tcp_header[1]


class Layer7:
    """Parse the layer 7 data of a packet (that's the actual data).

    Attributes
    ----------
    data : bytes
        The data of the packet, without headers.
    """
    def __init__(self, packet_bytes: bytes):
        self.data = packet_bytes[66:]
