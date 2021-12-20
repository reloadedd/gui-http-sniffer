import socket
from pwn import hexdump
from ..utils.constants import ETH_P_IP
from .analyzer import PacketAnalyzer
from ..exceptions.network import SLLUnsupportedError


class SnifferEngine:
    def __init__(self):
        self.socket = socket.socket(socket.AF_PACKET,
                                    socket.SOCK_RAW,
                                    socket.htons(ETH_P_IP))

    def sniff(self):
        while True:
            packet = self.socket.recvfrom(65535)[0]
            print(hexdump(packet), len(packet))

            try:
                analyzer = PacketAnalyzer(packet)
                print(analyzer.get_source_mac())
                print(analyzer.get_dest_mac())
                print(analyzer.get_source_ip())
                print(analyzer.get_dest_ip())
                print(analyzer.get_source_port())
                print(analyzer.get_dest_port())
                print(analyzer.get_content())
            except SLLUnsupportedError:
                continue
