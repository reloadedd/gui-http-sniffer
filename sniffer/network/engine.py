import socket
from pwn import hexdump
from ..utils.constants import ETH_P_ALL
from .analyzer import PacketAnalyzer
from ..utils.decorators import require_root
from ..exceptions.network import UninterestingPacketException,\
    UnsupportedVersionException


class SnifferEngine:
    NET_INTERFACE_ANY = 'any'
    INFINITY = -1
    MAX_PACKET_LEN = 65535

    @require_root
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
        async for packet in self.__sniff():
            self.total_packet_count += 1

            try:
                analyzer = PacketAnalyzer(packet, self.http_packet_count)
                # print(hexdump(packet))
                self.http_packet_count += 1

                yield self.http_packet_count, analyzer
            except UnsupportedVersionException:
                continue
            except UninterestingPacketException:
                continue
