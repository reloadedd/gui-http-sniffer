import socket
import struct
import netifaces
from pwn import hexdump
from ..utils.constants import ETH_P_IP
from .analyzer import PacketAnalyzer
from ..exceptions.network import SLLUnsupportedError,\
    UninterestingPacketException, UnsupportedVersionException


class SnifferEngine:
    NET_INTERFACE_ANY = 'any'

    def __init__(self, interface: str):
        self.interface = interface
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
            except SLLUnsupportedError:
                continue
            except UnsupportedVersionException:
                continue
            # except struct.error:
            #     continue
            except UninterestingPacketException:
                continue
