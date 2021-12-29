import re
import typing
from urllib.parse import unquote
from .layers import Layer3, Layer4, Layer7
from ..exceptions.network import UninterestingPacketException


class PacketAnalyzer:
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
    def packet_count(self):
        return self._packet_count

    @packet_count.setter
    def packet_count(self, value):
        self._packet_count = value

    @property
    def ip_version(self):
        return self.layer3.version

    @property
    def source_ip(self):
        return self.layer3.source_ip

    @property
    def dest_ip(self):
        return self.layer3.dest_ip

    @property
    def source_port(self):
        return self.layer4.source_port

    @property
    def dest_port(self):
        return self.layer4.dest_port

    @property
    def content(self) -> bytes:
        return self.layer7.data

    @property
    def http_version(self) -> str:
        regex = re.compile(br'HTTP\/\d\.\d')

        if match_obj := regex.search(self.content):
            return match_obj.group().decode('utf8')

        return 'Unknown'

    @property
    def status_code(self) -> str | None:
        end = self.content.find(b'\r\n')
        start = self.content.find(
            self.http_version.encode('utf-8')
        ) + len(self.http_version) + 1

        if start == -1 or end == -1:
            return None

        return self.content[start:end].decode('utf8')

    @property
    def http_verb(self) -> str | None:
        for method in PacketAnalyzer.HTTP_METHODS:
            if self.content.startswith(method.encode('utf-8')):
                return method

        return None

    @property
    def request_path(self) -> str:
        regex = re.compile(br'\w{3,7}\s(.*)\sHTTP')

        if match_obj := regex.match(self.content):
            return unquote(match_obj.group(1).decode('utf8'))

        return ''

    @property
    def http_headers(self) -> \
            typing.Generator[tuple[str | bytes, str | bytes], None, None]:
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
    def http_body(self):
        return self.content.split(b'\r\n\r\n')[1]
