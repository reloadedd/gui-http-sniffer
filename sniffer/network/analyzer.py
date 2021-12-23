from .layers import Layer3, Layer4, Layer7
from ..exceptions.network import UninterestingPacketException


class PacketAnalyzer:
    def __init__(self, packet_bytes: bytes):
        if b'HTTP/' not in packet_bytes:
            raise UninterestingPacketException

        self.layer3 = Layer3(packet_bytes)
        self.layer4 = Layer4(packet_bytes)
        self.layer7 = Layer7(packet_bytes)

    def get_ip_version(self):
        return self.layer3.version

    def get_source_ip(self):
        return self.layer3.source_ip

    def get_dest_ip(self):
        return self.layer3.dest_ip

    def get_source_port(self):
        return self.layer4.source_port

    def get_dest_port(self):
        return self.layer4.dest_port

    def get_content(self):
        return self.layer7.data
