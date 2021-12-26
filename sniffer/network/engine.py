import socket
from pwn import hexdump
from ..utils.constants import ETH_P_ALL
from .analyzer import PacketAnalyzer
from ..exceptions.network import UninterestingPacketException,\
    UnsupportedVersionException


class SnifferEngine:
    NET_INTERFACE_ANY = 'any'
    INFINITY = -1
    MAX_PACKET_LEN = 65535

    def __init__(self, interface: str):
        self.interface = interface
        self.total_packet_count = 0
        self.http_packet_count = 0

        self.socket = socket.socket(socket.AF_PACKET,
                                    socket.SOCK_RAW,
                                    socket.ntohs(ETH_P_ALL))

        # self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        # self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        if self.interface != SnifferEngine.NET_INTERFACE_ANY:
            # Attach to network interface
            self.socket.bind((self.interface, 0))

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

    async def __sniff(self):
        while True:
            yield self.socket.recvfrom(SnifferEngine.MAX_PACKET_LEN)[0]

    async def sniff(self, count: int = -1):
        # while count == SnifferEngine.INFINITY or self.http_packet_count <= count:
        async for i in self.__sniff():
            # print(self.total_packet_count, self.http_packet_count)
            packet = self.socket.recvfrom(65535)[0]
            self.total_packet_count += 1

            print(hexdump(packet), len(packet), b'HTTP/' in packet)
            try:
                analyzer = PacketAnalyzer(packet)
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
