import typing
from rich.console import Console


from .. import __version__
from ..network.analyzer import PacketAnalyzer
from ..utils.funcutils import get_commit_hash

# Global object which will be used throughout the whole package
console = Console()

version = f'[bold cyan]v{__version__.__version__}[/bold cyan]'
commit_hash = f'[bold cyan]{get_commit_hash()}[/bold cyan]'

BANNER = f"""\
                     ██████╗ ██╗  ██╗███████╗
                    ██╔════╝ ██║  ██║██╔════╝   [Author: Roșca Ionuț]
                    ██║  ███╗███████║███████╗   [License: GPL-3.0]
                    ██║   ██║██╔══██║╚════██║   [Version: {version}]
                    ╚██████╔╝██║  ██║███████║   [Commit: {commit_hash}]
                     ╚═════╝ ╚═╝  ╚═╝╚══════╝
                  ＧＵＩ ＨＴＴＰ ＳＮＩＦＦＥＲ
"""

EPILOG = "© Copyright 2021-2022, Roșca Ionuț."


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
