import struct
import binascii
import ipaddress
from ..exceptions.network import UnsupportedVersionException, \
    SLLUnsupportedError, UninterestingPacketException


class Layer2:
    """Parse the layer 2 data of a packet."""
    NULL_MAC_ADDRESS = b'00:00:00:00:00:00'

    """Parse the layer 2 data of a packet."""
    def __init__(self, packet_bytes: bytes):
        ethernet_header = struct.unpack('!6s6s2s', packet_bytes[:14])

        self.source_mac = Layer2.parse_mac_address(ethernet_header[0])
        if self.source_mac == Layer2.NULL_MAC_ADDRESS:
            raise SLLUnsupportedError

        self.dest_mac = Layer2.parse_mac_address(ethernet_header[1])
        self.type = ethernet_header[2]

    @staticmethod
    def parse_mac_address(address: bytes):
        return binascii.hexlify(address, sep=':')


class Layer3:
    """Parse the layer 3 data of a packet."""
    IP_VERSION_4 = 0x45

    """Parse the layer 4 data of a packet."""
    def __init__(self, packet_bytes: bytes):
        # Ignoring 11 bytes
        ip_header = struct.unpack('!B11s4s4s', packet_bytes[14:34])

        self.version = ip_header[0]
        print(self.version)

        if self.version != Layer3.IP_VERSION_4:
            raise UnsupportedVersionException('Only IPv4 is supported')

        self.source_ip = ipaddress.IPv4Address(ip_header[2])
        self.dest_ip = ipaddress.IPv4Address(ip_header[3])


class Layer4:
    """Parse the layer 4 data of a packet."""
    def __init__(self, packet_bytes: bytes):
        # Ignoring 16 bytes
        tcp_header = struct.unpack('!HH16s', packet_bytes[34:54])

        self.source_port = tcp_header[0]
        self.dest_port = tcp_header[1]


class Layer7:
    """Parse the layer 7 data of a packet (that's the actual data)."""
    def __init__(self, packet_bytes: bytes):
        self.data = packet_bytes[54:]
