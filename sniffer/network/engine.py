import socket
import struct
from pwn import hexdump
from ..utils.constants import ETH_P_IP
from .analyzer import PacketAnalyzer
from ..exceptions.network import SLLUnsupportedError, UninterestingPacketException


class SnifferEngine:
    NET_INTERFACE_ANY = 'any'

    def __init__(self, interface: str):
        self.interface = interface
        self.socket = socket.socket(socket.AF_PACKET,
                                    socket.SOCK_RAW,
                                    socket.htons(ETH_P_IP))

        if self.interface != SnifferEngine.NET_INTERFACE_ANY:
            # Attach to network interface
            self.socket.bind((self.interface, 0))

    def sniff(self):
        while True:
            packet = self.socket.recvfrom(65535)[0]

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
            # except SLLUnsupportedError:
            #     continue
            # except struct.error:
            #     continue
            except UninterestingPacketException:
                continue
