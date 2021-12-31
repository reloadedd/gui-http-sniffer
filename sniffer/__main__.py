"""
    GUI HTTP Sniffer i.e. GHS, is a layer-7 sniffer, targeting
    unencrypted HTTP traffic and is capable of reading and analyzing
    that traffic.
"""

import asyncio
import argparse

from .utils import constants
from .tui.display import render
from .__version__ import __version__
from .network.engine import SnifferEngine
from .parser.textutils import BANNER, EPILOG
from .parser.custom import ColoredArgumentParser
from .parser.options import list_interfaces, list_filters


def create_parser() -> argparse.Namespace:
    """Create the parser with the given arguments.

    Returns
    -------
    argparse.Namespace
        An object containing parsed options and their values.
    """
    parser = ColoredArgumentParser(
        description=f'{BANNER}\n{__doc__}',
        formatter_class=lambda prog: argparse.RawDescriptionHelpFormatter(
            prog,
            max_help_position=40
        ),
        add_help=False,
        epilog=EPILOG
    )

    optional_args = parser.add_argument_group('ARGUMENTS')
    optional_args.add_argument(
        '-f',
        '--filter',
        help='[blue]Filter expression to be applied when sniffing traffic.'
             '[/blue]',
        type=str,
        default=constants.DEFAULT_FILTER,
        dest='filter'
    )
    optional_args.add_argument(
        '-i',
        '--interface',
        help='[blue]The network interface to be used. Default: any[/blue]',
        default='any',
        dest='interface'
    )
    optional_args.add_argument(
        '-c',
        '--count',
        help='[blue]How many packets to sniff[/blue]',
        type=int,
        default=constants.INFINITY,
        dest='count'
    )
    optional_args.add_argument(
        '-o',
        '--output',
        help='[blue]Store the output in the given file[/blue]',
        type=str,
        default='',
        dest='file'
    )
    optional_args.add_argument(
        '-li',
        '--list-interfaces',
        help='[blue]List all network interfaces present in the system[/blue]',
        dest='list_interfaces',
        action='store_true'
    )
    optional_args.add_argument(
        '-lf',
        '--list-filters',
        help='[blue]List all possible filters for sniffed packets[/blue]',
        dest='list_filters',
        action='store_true'
    )
    optional_args.add_argument(
        '-v',
        '--version',
        action='version',
        version=f'{parser.prog} {__version__}',
        help="[blue]Show program's version number and exit.[/blue]"
    )
    optional_args.add_argument(
        '-h',
        '--help',
        action='help',
        default=argparse.SUPPRESS,
        help='[blue]Show this help message and exit.[/blue]'
    )

    # Mood update: feeling determined
    # This is what I call 'o românească'
    usage = parser.add_argument_group('USAGE')
    usage.add_argument(
        f'[u]{parser.format_usage()[7: 7 + len(parser.prog)]}[/u]'
        f'{parser.format_usage()[7 + len(parser.prog):]}',
        default=constants.PARSER_IGNORE,
        nargs='?'   # Bypass the required value for positional arguments
    )

    parsed = parser.parse_args()
    if parsed.list_interfaces:
        list_interfaces()
        exit(constants.EXIT_SUCCESS)

    if parsed.list_filters:
        list_filters()
        exit(constants.EXIT_SUCCESS)

    return parsed


async def run():
    """Initialize the components and run the application."""
    args = create_parser()

    sniffer = SnifferEngine(args.interface, args.file)
    await render(args, sniffer)


def main():
    """Wrapper over the `run()` function.

    Needed for async IO.
    """
    asyncio.run(run())


if __name__ == '__main__':
    main()
