import socket
import typing

from ..utils import constants
from .analyzer import PacketAnalyzer
from ..utils.decorators import require_root
from ..exceptions.network import UninterestingPacketException,\
    UnsupportedVersionException


class SnifferEngine:
    """The Sniffer Engine sniffs the packets that flow through the network.

    Attributes
    ----------
    interface : str
        The name of the interface to be used for sniffing packets.
    filename : str, optional
        The name of the file to be used for writing the output.
    socket : socket.socket
        The socket used for sniffing packets.
    """
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

    def __create_file_handle(self) -> typing.Any:
        """Open the requested file in write-only mode."""
        if self.filename == '':
            return None

        return open(self.filename, 'w')

    def close_handle(self) -> None:
        """Close the opened file."""
        if self.file_handle:
            self.file_handle.close()

    @property
    def file_handle(self) -> typing.TextIO:
        """Get the file handle."""
        return self._file_handle

    @file_handle.setter
    def file_handle(self, value) -> None:
        """Set the file handle."""
        self._file_handle = value

    @property
    def total_packet_count(self) -> int:
        """Get the total number of sniffed packets."""
        return self._packet_count

    @total_packet_count.setter
    def total_packet_count(self, value) -> None:
        """Set the total number of sniffed packets."""
        self._packet_count = value

    @property
    def filtered_packets(self) -> int:
        """Get the number of filtered packets."""
        return self._filtered_packets

    @filtered_packets.setter
    def filtered_packets(self, value) -> None:
        """Set the number of filtered packets."""
        self._filtered_packets = value

    @property
    def http_packet_count(self) -> int:
        """Get the number of HTTP packets."""
        return self._http_packet_count

    @http_packet_count.setter
    def http_packet_count(self, value) -> None:
        """Set the number of HTTP packets."""
        self._http_packet_count = value

    async def __sniff(self) -> typing.AsyncGenerator[bytes, None]:
        """Primitive generator that yields the next packet sniffed.

        Yields
        ------
        bytes
            The sniffed packet.
        """
        while True:
            yield self.socket.recvfrom(SnifferEngine.MAX_PACKET_LEN)[0]

    async def sniff(self,
                    count: int) -> typing.AsyncGenerator[PacketAnalyzer, None]:
        """Filter sniffed packets and generate only HTTP packets.

        Parameters
        ----------
        count : int
            The number of packets to sniff. May be infinite.

        Yields
        ------
        PacketAnalyzer
            The content of the sniffed packet, wrapped in a parsable format.
        """
        async for packet in self.__sniff():
            if count != constants.INFINITY and \
                    self.http_packet_count - self.filtered_packets >= count:
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
