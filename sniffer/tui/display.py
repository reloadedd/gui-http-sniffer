import sys
import asyncio
import argparse
import netifaces
from time import sleep
from datetime import datetime

from rich.text import Text
from rich.live import Live
from rich.tree import Tree
from rich.align import Align
from rich.panel import Panel
from rich.layout import Layout
from rich.columns import Columns

from ..utils import constants
from ..parser.filter import Filter
from ..parser.textutils import console
from ..__version__ import __version__
from ..network.engine import SnifferEngine
from ..utils.funcutils import get_commit_hash
from ..network.analyzer import PacketAnalyzer
from ..parser.textutils import write_output_to_file
from ..exceptions.parser import InvalidFilterException


# Credits for the clock: rich module examples
# https://github.com/willmcgugan/rich/blob/master/examples/layout.py
class Header:
    """Render the time in the center of the screen, used as header."""
    @staticmethod
    def __rich__() -> Text:
        text = f'Gui Http Sniffer - GHS [{datetime.now().ctime()}]'
        return Text(text, style="bold magenta", justify="center")


class Footer:
    """Return a panel filled with information to be used as footer.

    Attributes
    ----------
    interface : str, optional
        The network interface used. Defaults to 'any'.
    stage : str, optional
        The current stage. Defaults to 'beginning'. Other option is 'end'.
    count : int, optional
        The number of packets to be sniffed by the engine.
    seconds : int, optional
        The number of seconds to wait before quitting.
    message : str, optional
        The error message, in case of error.
    """
    def __init__(self, interface: str = 'any',
                 stage: str = 'beginning',
                 count: int = constants.INFINITY,
                 seconds: int = constants.INFINITY,
                 message: str = ''):
        self.interface = interface
        self.stage = stage
        self.count = count
        self.seconds = seconds
        self.message = message

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
                     title="[red]Status[/red]",
                     title_align="center",
                     border_style='bold red',
                     style="cyan")

    def __rich_footer_end(self):
        text = f'All [b cyan]{self.count}[/b cyan] packets have been ' \
               f'sniffed! Exiting in [b cyan]{self.seconds}[/b cyan] ' \
               f'seconds...'

        return Panel(Align.center(text),
                     title="[red]Status[/red]",
                     title_align="center",
                     border_style='bold red',
                     style="cyan")

    def __rich_footer_error(self):
        return Panel(Align.center(f'{self.message}. Exiting in [b cyan]'
                                  f'{self.seconds}[/b cyan] seconds...'),
                     title="[red]Status[/red]",
                     title_align="center",
                     border_style='bold red',
                     style="cyan")

    def __rich__(self):
        if self.stage == 'beginning':
            return self.__rich_footer_begin()
        elif self.stage == 'end':
            return self.__rich_footer_end()
        elif self.stage == 'error':
            return self.__rich_footer_error()

        return Panel(Align.center('Wrong stage name'),
                     title="[red]Status[/red]",
                     title_align="center",
                     border_style='bold red',
                     style="cyan")


class SidePanel:
    """Draw a side panel in the right area of the terminal.

    Attributes
    ----------
    sniffer : SnifferEngine
        The sniffer object, used for harvesting information.
    _filter : str
        The filter currently used for packets.
    """
    def __init__(self, sniffer: SnifferEngine, _filter: str):
        self.sniffer = sniffer
        self.filter = _filter

    def __rich__(self):
        text = f"""\
▶ Total Packet Count\t[b yellow]{self.sniffer.total_packet_count}[/b yellow]
▶ HTTP Packet Count\t[b yellow]{self.sniffer.http_packet_count}[/b yellow]
▶ Filtered HTTP Packets\t[b yellow]{self.sniffer.filtered_packets}[/b yellow]
"""

        columns = Columns(
            [
                Panel(text,
                      expand=True),
                Panel(f'▶ Filter\t[b purple]{self.filter}[/b purple]',
                      expand=True),
            ], expand=True
        )

        return Panel(columns,
                     title="[red]Statistics[/red]",
                     title_align="center",
                     border_style='bold red',
                     style="cyan",
                     expand=True)


class Body:
    """Draw the entire body and displays live the sniffed packets.

    Attributes
    ----------
    packets : list[PacketAnalyzer]
        A list with the current packets that will be displayed.
    max_height : int
        The maximum height that could be used to display packet information.
    """
    def __init__(self, analyzer: list[PacketAnalyzer], max_height: int):
        self.packets = analyzer
        self.max_height = max_height

    def __rich__(self):
        packet_list = []

        for analyzer in self.packets:
            formatted_packet = [
                f'▷ [b magenta]#{analyzer.packet_count}[/b magenta]\t'
                f'[b green]{analyzer.source_ip}[/b green] ⟶ '
                f'[b red]{analyzer.dest_ip}[/b red] | '
                f'[b green]HTTP Version:[/b green]\t'
                f'[b]{analyzer.http_version}[/b]'
            ]

            # This means it's an HTTP response
            if analyzer.http_verb is None:
                formatted_packet.append(f' | [b green]Status code:[/b green]\t'
                                        f'[b]{analyzer.status_code}[/b]\t'
                                        f'[b purple][Response][/b purple]')
            else:
                formatted_packet.append(f' | [b green]Method:[/b green]\t'
                                        f'[b]{analyzer.http_verb}[/b]\t'
                                        f'[b magenta][Request][/b magenta]')

            tree = Tree(''.join(formatted_packet),
                        guide_style='underline2 cyan')

            if analyzer.http_verb is not None:
                path = tree.add('⚫[b magenta]Path[/b magenta]')
                path.add(f'{analyzer.request_path}')

            headers = tree.add('⚫[b magenta]Headers[/b magenta]')
            for key, value in analyzer.http_headers:
                headers.add(f'[b green]{key}:[/b green]{value}')

            body = tree.add('⚫[b magenta]Body[/b magenta]')

            if not analyzer.http_body:
                body.add('[b purple]<empty>[/b purple]')
            else:
                body.add(Text(f'{analyzer.http_body}'))

            packet_list.append(Panel(tree,
                                     expand=True,
                                     border_style='dim white',
                                     height=analyzer.packet_height))

        return Columns(packet_list, expand=True)


class Banner:
    """Display an animated ASCII Art text.

    This class implements an iterator, which at each step return the next
    frame in the animation. A frame, in this context, is an entry in a string
    list.

    Attributes
    ----------
    index : int
        Keep track of the current frame when iterated.
    banner_array : list[str]
        A list with all the frames.
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
    """Update the status bar upon exit.
    
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


def error(layout: Layout, live: Live, message: str) -> None:
    """Update status bar upon exit.
    
    Parameters
    ----------
    layout : Layout
        A layout object which represent a rectangular area in the application
    live : Live
        The context manager object used to create the whole 'graphics'
    message: str
        The error message.
    """
    for seconds in range(5, 0, -1):
        layout['footer'].update(Footer(stage='error',
                                       seconds=seconds,
                                       message=message))
        live.refresh()
        sleep(1)


def make_layouts(args: argparse.Namespace, sniffer: SnifferEngine):
    """Create the layouts for the application.

    Parameters
    ----------
    args : argparse.Namespace
        The list of all command-line arguments.
    sniffer : SnifferEngine
        The sniffer object.

    Returns
    -------
    Layout
        An layout incorporating all the layouts.
    Panel
        All layouts are encapsulated inside this panel.

    Notes
    -----
    The Panel is used for drawing the borders of the application.
    """
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
            Text(f'Sniffing the air for unencrypted HTTP packets...',
                 justify='center', style='dim red'),
            vertical="middle"
        )
    )

    layout['header'].update(Header())
    layout['side'].update(SidePanel(sniffer, args.filter))
    layout['footer'].update(Footer(args.interface))

    return layout, panel


async def update_and_refresh(layout: Layout,
                             live: Live,
                             packets: list[PacketAnalyzer],
                             max_height: int) -> None:
    """Update the screen with the new information and refresh it.

    Parameters
    ----------
    layout : Layout
        The rectangular area which is to be updated
    live : Live
        The context manager object which orchestrates the visible areas
    packets : list[PacketAnalyzer]
        A list containing parsed information from sniffed packets
    max_height : int
        The maximum height to be used by the layout
    """
    layout.update(Body(packets, max_height))
    live.refresh()


async def fit_packets(packets: list[PacketAnalyzer], max_height: int) -> None:
    """Fit the packets to the screen by height.

    Parameters
    ----------
    packets : list[PacketAnalyzer]
        The list of HTTP packets
    max_height : int
        The maximum height allowed to be used for displaying the packets on
        the screen
    """
    cumulative_sum = sum((packet.packet_height for packet in packets))
    while len(packets) > 1 and cumulative_sum > max_height:
        packets.pop(0)


async def render(args: argparse.Namespace, sniffer: SnifferEngine) -> None:
    """Render the application and coordinate the backend.

    Parameters
    ----------
    args : argparse.Namespace
        The list of all command-line arguments.
    sniffer : SnifferEngine
        The sniffer object.

    Notes
    -----
    Even though not explicitly stated, this method is the brain of the
    application as it coordinates both the fronted and the backend.
    """
    layout, panel = make_layouts(args, sniffer)

    banner = Banner()
    with Live(banner,
              screen=True,
              redirect_stderr=False,
              auto_refresh=False,
              transient=True,
              console=console) as live:
        # The coolest thing you will see today
        intro(banner, live)

        live.update(panel, refresh=True)
        try:
            packets = []

            async for analyzer in sniffer.sniff(args.count):
                # Filter HTTP packets based on the filter provided
                if not (lambda: Filter(analyzer, args.filter))():
                    sniffer.filtered_packets += 1

                    live.refresh()
                    continue

                # 3 is footer + 1 is header + 2 for the borders (top & bottom)
                max_height = console.height - 6

                packets.append(analyzer)
                await fit_packets(packets, max_height)

                await asyncio.gather(*(
                    asyncio.create_task(
                        update_and_refresh(layout['body'],
                                           live,
                                           packets,
                                           max_height)),
                    asyncio.create_task(
                        write_output_to_file(sniffer.file_handle, analyzer))
                ))

            # This code is reachable only if the count is not `INFINITY`
            outro(layout['footer'], live, args.count)
        except KeyboardInterrupt:
            pass
        except InvalidFilterException:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            error(layout['footer'], live, f'InvalidFilterException: {exc_obj}')
        finally:
            sniffer.close_handle()
