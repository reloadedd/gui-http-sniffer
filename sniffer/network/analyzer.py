import re
import typing
from urllib.parse import unquote

from ..parser.textutils import console
from .layers import Layer3, Layer4, Layer7
from ..exceptions.network import UninterestingPacketException


class PacketAnalyzer:
    """Analyze a sniffed network packet.

    Attributes
    ----------
    packet_bytes : bytes
        The content of the packet, represented as bytes.
    """
    HTTP_METHODS = [
        'GET',
        'HEAD',
        'POST',
        'PUT',
        'DELETE',
        'CONNECT',
        'OPTIONS',
        'TRACE',
        'PATCH'
    ]

    def __init__(self, packet_bytes: bytes, packet_count: int):
        if b'HTTP/' not in packet_bytes:
            raise UninterestingPacketException

        self.packet_count = packet_count + 1
        self.layer3 = Layer3(packet_bytes)
        self.layer4 = Layer4(packet_bytes)
        self.layer7 = Layer7(packet_bytes)

    @property
    def packet_count(self) -> int:
        """Get the current packet number."""
        return self._packet_count

    @packet_count.setter
    def packet_count(self, value) -> None:
        """Set the current packet number."""
        self._packet_count = value

    @property
    def ip_version(self) -> int:
        """Get the IP version of the packet."""
        return self.layer3.version

    @property
    def source_ip(self) -> "IPv4Address":
        """Get the source IP of the packet."""
        return self.layer3.source_ip

    @property
    def dest_ip(self) -> "IPv4Address":
        """Get the destination IP of the packet."""
        return self.layer3.dest_ip

    @property
    def source_port(self) -> int:
        """Get the source port of the packet."""
        return self.layer4.source_port

    @property
    def dest_port(self) -> int:
        """Get the destination port of the packet."""
        return self.layer4.dest_port

    @property
    def content(self) -> bytes:
        """Get the packet data, with the headers removed."""
        return self.layer7.data

    @property
    def http_version(self) -> str:
        """Get the HTTP version."""
        regex = re.compile(br'HTTP/\d\.\d')

        if match_obj := regex.search(self.content):
            return match_obj.group().decode('utf8')

        return 'Unknown'

    @property
    def status_code(self) -> typing.Any:
        """Get the status code of the response."""
        end = self.content.find(b'\r\n')
        start = self.content.find(
            self.http_version.encode('utf-8')
        ) + len(self.http_version) + 1

        if start == -1 or end == -1:
            return None

        return self.content[start:end].decode('utf8')

    @property
    def http_verb(self) -> typing.Any:
        """Get the method of the request."""
        for method in PacketAnalyzer.HTTP_METHODS:
            if self.content.startswith(method.encode('utf-8')):
                return method

        return None

    @property
    def request_path(self) -> str:
        """Get the path of the request."""
        regex = re.compile(br'\w{3,7}\s(.*)\sHTTP')

        if match_obj := regex.match(self.content):
            return unquote(match_obj.group(1).decode('utf8'))

        return ''

    @property
    def http_headers(self) -> \
            typing.Generator[tuple[typing.Any, typing.Any], None, None]:
        """Get the packet's headers.

        Yields
        ------
        key : typing.Any
            The header name
        value : typing.Any
            The header value

        Notes
        -----
        The `key` and `value` will be either strings (if successful) or bytes
        (if the bytes could not be decoded).
        """
        for header in self.content.split(b'\r\n')[1:]:
            if not header:
                break

            try:
                key = header.split(b':')[0].decode('utf8')
                value = header.split(b':')[1].decode('utf8')
            except UnicodeDecodeError:
                key = header.split(b':')[0]
                value = header.split(b':')[1]

            yield key, value

    @property
    def http_body(self) -> bytes:
        """Get the body of the HTTP packet."""
        try:
            return self.content.split(b'\r\n\r\n')[1]
        except IndexError:
            return b''

    @property
    def packet_height(self) -> int:
        """Get the height that the packet will take on screen if displayed."""
        headers_len = len([_ for _ in self.http_headers])
        # Some crazy math: 3/4 is the ratio of the 'body' layout
        # 12 characters are taken by the tree's branch
        # 1 character in case the text is less than one line
        body_len = len(self.http_body) // (console.width * 3 // 4 - 12) + 1

        path_len = 0
        if self.request_path:
            path_len = 2

        return sum((3, 2, path_len, headers_len, body_len))
