import argparse
import typing

import netifaces
import asyncio
from time import sleep
from datetime import datetime
from rich.text import Text
from rich.live import Live
from rich.align import Align
from rich.panel import Panel
from rich.layout import Layout

from ..utils import constants
from ..__version__ import __version__
from ..network.analyzer import PacketAnalyzer
from ..network.engine import SnifferEngine
from ..utils.funcutils import get_commit_hash


# Credits for the clock: rich module examples
# https://github.com/willmcgugan/rich/blob/master/examples/layout.py
class Header:
    """Render the time in the center of the screen, used as header."""
    @staticmethod
    def __rich__() -> Text:
        text = f'Gui Http Sniffer - GHS [{datetime.now().ctime()}]'
        return Text(text, style="bold magenta", justify="center")


class Footer:
    """Return a panel filled with information to be used as footer."""
    def __init__(self, interface: str = 'any',
                 stage: str = 'beginning',
                 count: int = constants.INFINITY,
                 seconds: int = constants.INFINITY):
        self.interface = interface
        self.stage = stage
        self.count = count
        self.seconds = seconds

    def __rich_footer_begin(self):
        ip_address = 'any'
        if self.interface != 'any':
            ip_address = netifaces.ifaddresses(
                self.interface)[netifaces.AF_INET][0]['addr'] if \
                netifaces.ifaddresses(self.interface).get(
                    netifaces.AF_INET, None
                ) is not None else 'Unavailable'

        text = f'Interface: {self.interface} | ' \
               f'IP Address: {ip_address} | ' \
               f'Commit Hash: {get_commit_hash()} | ' \
               f'Version: v{__version__}'

        return Panel(Text(text, justify="center"),
                     title="[red]Information[/red]",
                     title_align="center",
                     border_style='bold red',
                     style="cyan")

    def __rich_footer_end(self):
        text = f'All [b cyan]{self.count}[/b cyan] packets have been ' \
               f'sniffed! Exiting in [b cyan]{self.seconds}[/b cyan] ' \
               f'seconds...'

        return Panel(Align.center(text),
                     title="[red]Information[/red]",
                     title_align="center",
                     border_style='bold red',
                     style="cyan")

    def __rich__(self):
        if self.stage == 'beginning':
            return self.__rich_footer_begin()
        else:
            return self.__rich_footer_end()


class SidePanel:
    def __init__(self, sniffer):
        self.sniffer = sniffer

    def __rich__(self):
        text = f"""\
▶ Total Packet Count\t[b yellow]{self.sniffer.total_packet_count}[/b yellow]
▶ HTTP Packet Count\t[b yellow]{self.sniffer.http_packet_count}[/b yellow]
"""

        return Panel(text,
                     title="[red]Statistics[/red]",
                     title_align="center",
                     border_style='bold red',
                     style="cyan")


class Body:
    def __init__(self, analyzer):
        self.packets = analyzer

    def __rich__(self):
        text_list = []
        for analyzer in self.packets:
            formatted_packet = [
                f'▷ [b magenta]#{analyzer.packet_count}[/b magenta]\t'
                f'[green]{analyzer.source_ip}[/green] ⟶ '
                f'[red]{analyzer.dest_ip}[/red] | '
                f'[green]HTTP Version:[/green]\t'
                f'[b]{analyzer.http_version}[/b]'
            ]
            # This means it's an HTTP response
            if analyzer.http_verb is None:
                formatted_packet.append(f' | [green]Status code:[/green]\t'
                                        f'[b]{analyzer.status_code}[/b]\t'
                                        f'[b purple][Response][/b purple]')
            else:
                formatted_packet.append(f' | [green]Method:[/green]\t'
                                        f'[b]{analyzer.http_verb}[/b]\t'
                                        f'[b magenta][Request][/b magenta]')

            formatted_packet.append(f'\nContent: {analyzer.content}\n')
            text_list.append(''.join(formatted_packet))

        return Align.left(''.join(text_list))


class Banner:
    """Display an animated ASCII Art text.

    This class implements an iterator, which at each step return the next
    frame in the animation. A frame, in this context, is an entry in a string
    list.
    """
    # Path is relative to the sniffer package
    # Credits for the animation: https://ascii.co.uk/animated
    BANNER_FILE = './sniffer/tui/banner.txt'

    def __init__(self):
        self.index = 0

        with open(Banner.BANNER_FILE) as banner:
            self.banner_array = banner.readlines()

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == len(self.banner_array):
            raise StopIteration

        panel = Panel(
            Align.center(
                Text(self.banner_array[self.index].replace('\\n', '\n'),
                     justify='left', style='bold red'), vertical='middle'),
            border_style='bold dark_cyan'
        )
        self.index += 1

        return panel

    def __rich__(self):
        # Return a panel created using the first frame
        return Panel(Align.center(
            Text(self.banner_array[0].replace('\\n', '\n'), justify='left'),
            vertical='middle'
        ), border_style='dim dark_cyan')


def intro(banner: Banner, live: Live) -> None:
    """Create cinematic intro effect.

    Parameters
    ----------
    banner : Banner
        A renderable object that `rich` knows how to display
    live : Live
        The context manager object used to create the whole 'graphics'
    """
    for frame in banner:
        live.update(frame)
        live.refresh()
        sleep(0.048)


def outro(layout: Layout, live: Live, count: int) -> None:
    """Create cinematic outro effect.
    
    Parameters
    ----------
    layout : Layout
        A layout object which represent a rectangular area in the application
    live : Live
        The context manager object used to create the whole 'graphics'
    count : int
        The number of packets that were displayed   
    """
    for seconds in range(5, 0, -1):
        layout['footer'].update(Footer(stage='end',
                                       count=count,
                                       seconds=seconds))
        live.refresh()
        sleep(1)


def make_layouts(args: argparse.Namespace, sniffer: SnifferEngine):
    layout = Layout()
    panel = Panel(layout, border_style='bold dark_cyan')

    layout.split(
        Layout(name='header', size=1),
        Layout(ratio=1, name='main'),
        Layout(size=3, name='footer'),
    )

    layout['main'].split_row(Layout(name='body', ratio=3), Layout(name='side'))
    layout['body'].update(
        Align.center(
            Text('Sniffing the air for unencrypted HTTP packets...',
                 justify='center', style='dim red'),
            vertical="middle"
        )
    )

    layout['header'].update(Header())
    layout['side'].update(SidePanel(sniffer))
    layout['footer'].update(Footer(args.interface))

    return layout, panel


async def write_output_to_file(handle: typing.TextIO,
                               analyzer: PacketAnalyzer) -> None:
    """Write the output from sniffed packets to a file.

    If the user didn't chose to save the output to a file, the function will
    simply exit by returning None.

    Parameters
    ----------
    handle : typing.TextIO
        The file handle corresponding to the output file
    analyzer : PacketAnalyzer
        Parsed information from the currently sniffed packet
    """
    if not handle:
        return

    formatted_packet = [
        f'▷ #{analyzer.packet_count}\t'
        f'{analyzer.source_ip} ⟶ '
        f'{analyzer.dest_ip} | '
        f'HTTP Version:\t'
        f'{analyzer.http_version}'
    ]

    # This means it's an HTTP response
    if analyzer.http_verb is None:
        formatted_packet.append(f' | Status code:\t'
                                f'{analyzer.status_code}\t'
                                f'[Response]')
    else:
        formatted_packet.append(f' | Method:\t'
                                f'{analyzer.http_verb}\t'
                                f'[Request]')

    formatted_packet.append(f'\nContent: {analyzer.content}\n')
    handle.write(''.join(formatted_packet))


async def update_and_refresh(layout: Layout,
                             live: Live,
                             packets: list[PacketAnalyzer]) -> None:
    """Update the screen with the new information and refresh it.

    Parameters
    ----------
    layout : Layout
        The rectangular area which is to be updated
    live : Live
        The context manager object which orchestrates the visible areas
    packets : list[PacketAnalyzer]
        A list containing parsed information from sniffed packets
    """
    layout.update(Body(packets))
    live.refresh()


async def render(args: argparse.Namespace, sniffer: SnifferEngine):
    layout, panel = make_layouts(args, sniffer)

    banner = Banner()
    with Live(banner,
              screen=True,
              redirect_stderr=False,
              auto_refresh=False) as live:
        # The coolest thing you will see today
        intro(banner, live)

        live.update(panel, refresh=True)
        try:
            packets = []
            async for analyzer in sniffer.sniff(args.count):
                if len(packets) == 8:
                    packets = [analyzer]
                else:
                    packets.append(analyzer)

                await asyncio.gather(*(
                    asyncio.create_task(
                        update_and_refresh(layout['body'], live, packets)),
                    asyncio.create_task(
                        write_output_to_file(sniffer.file_handle, analyzer))
                ))

            # This code is reachable only if the count is not `INFINITY`
            outro(layout['footer'], live, args.count)
        except KeyboardInterrupt:
            pass
        finally:
            sniffer.close_handle()
