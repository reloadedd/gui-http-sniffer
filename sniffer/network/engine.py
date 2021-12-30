import socket
import typing
from ..utils import constants
from .analyzer import PacketAnalyzer
from ..utils.decorators import require_root
from ..exceptions.network import UninterestingPacketException,\
    UnsupportedVersionException


class SnifferEngine:
    NET_INTERFACE_ANY = 'any'
    INFINITY = -1
    MAX_PACKET_LEN = 65535

    @require_root
    def __init__(self, interface: str, filename: str = ''):
        self.interface = interface
        self.total_packet_count = 0
        self.http_packet_count = 0
        self.filtered_packets = 0
        self.filename = filename
        self.file_handle = self.__create_file_handle()

        self.socket = socket.socket(socket.AF_PACKET,
                                    socket.SOCK_RAW,
                                    socket.ntohs(constants.ETH_P_ALL))

        if self.interface != SnifferEngine.NET_INTERFACE_ANY:
            # Attach to network interface
            self.socket.bind((self.interface, 0))

    def __create_file_handle(self):
        """Open the requested file in write-only mode."""
        if self.filename == '':
            return None

        return open(self.filename, 'w')

    def close_handle(self):
        """Close the opened file."""
        if self.file_handle:
            self.file_handle.close()

    @property
    def file_handle(self):
        return self._file_handle

    @file_handle.setter
    def file_handle(self, value):
        self._file_handle = value

    @property
    def total_packet_count(self) -> int:
        return self._packet_count

    @total_packet_count.setter
    def total_packet_count(self, value) -> None:
        self._packet_count = value

    @property
    def filtered_packets(self):
        return self._filtered_packets

    @filtered_packets.setter
    def filtered_packets(self, value):
        self._filtered_packets = value

    @property
    def http_packet_count(self) -> int:
        return self._http_packet_count

    @http_packet_count.setter
    def http_packet_count(self, value) -> None:
        self._http_packet_count = value

    async def __sniff(self) -> typing.AsyncGenerator[bytes, None]:
        """Primitive generator that return the next packet sniffed."""
        while True:
            yield self.socket.recvfrom(SnifferEngine.MAX_PACKET_LEN)[0]

    async def sniff(self,
                    count: int) -> typing.AsyncGenerator[PacketAnalyzer, None]:
        """Filter sniffed packets and generate only HTTP packets.

        Parameters
        ----------
        count : int
            The number of packets to sniff. May be infinite.
        """
        async for packet in self.__sniff():
            if count != constants.INFINITY and self.http_packet_count >= count:
                break

            self.total_packet_count += 1

            try:
                analyzer = PacketAnalyzer(packet, self.http_packet_count)
                self.http_packet_count += 1

                yield analyzer
            # Skip over uninteresting packets
            except UnsupportedVersionException:
                continue
            except UninterestingPacketException:
                continue
