import socket
import struct
import netifaces
from pwn import hexdump
from ..utils.constants import ETH_P_IP
from .analyzer import PacketAnalyzer
from ..exceptions.network import UninterestingPacketException,\
    UnsupportedVersionException


class SnifferEngine:
    NET_INTERFACE_ANY = 'any'
    INFINITY = -1

    def __init__(self, interface: str):
        self.interface = interface
        self.total_packet_count = 0
        self.http_packet_count = 0

        self.socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_RAW,
                                    socket.IPPROTO_TCP)

        if self.interface != SnifferEngine.NET_INTERFACE_ANY:
            # Attach to network interface
            self.socket.bind((
                netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr'],
                0
            ))

        # self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    @property
    def total_packet_count(self):
        return self._packet_count

    @total_packet_count.setter
    def total_packet_count(self, value):
        self._packet_count = value

    @property
    def http_packet_count(self):
        return self._http_packet_count

    @http_packet_count.setter
    def http_packet_count(self, value):
        self._http_packet_count = value

    def sniff(self, count: int = -1):
        while count == SnifferEngine.INFINITY or self.http_packet_count <= count:
            print(self.total_packet_count, self.http_packet_count)
            packet = self.socket.recvfrom(65535)[0]
            self.total_packet_count += 1

            try:
                print(hexdump(packet), len(packet), b'HTTP/' in packet)
                analyzer = PacketAnalyzer(packet)
                print(analyzer.get_source_mac())
                print(analyzer.get_dest_mac())
                print(analyzer.get_source_ip())
                print(analyzer.get_dest_ip())
                print(analyzer.get_source_port())
                print(analyzer.get_dest_port())
                print(analyzer.get_content())
            except UnsupportedVersionException:
                continue
            except UninterestingPacketException:
                continue

            self.http_packet_count += 1
