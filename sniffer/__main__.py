"""
    GUI HTTP Sniffer i.e. GHS, is a layer-7 sniffer, targeting
    unencrypted HTTP traffic and is capable of reading and analyzing
    that traffic.
"""

import sys
import asyncio
import argparse

from .utils import constants
from .tui.display import render
from .__version__ import __version__
from .network.engine import SnifferEngine
from .parser.options import list_interfaces
from .parser.textutils import BANNER, EPILOG
from .parser.custom import ColoredArgumentParser


def create_parser():
    parser = ColoredArgumentParser(
        description=f'{BANNER}\n{__doc__}',
        formatter_class=lambda prog: argparse.RawDescriptionHelpFormatter(
            prog,
            max_help_position=40
        ),
        add_help=False,
        epilog=EPILOG
    )

    positional_args = parser.add_argument_group('POSITIONAL ARGUMENTS')

    optional_args = parser.add_argument_group('OPTIONAL ARGUMENTS')
    optional_args.add_argument(
        '-f',
        '--filter',
        default=argparse.SUPPRESS,
        help='[blue]Filter expression to be applied when sniffing traffic.'
             '[/blue]'
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
        '-l',
        '--list-interfaces',
        help='[blue]List all network interfaces present in the system[/blue]',
        dest='list_interfaces',
        action='store_true'
    )
    optional_args.add_argument(
        '-v',
        '--version',
        action='version',
        version=f'{parser.prog} {__version__}',
        help="[blue]Show program's version number and exit.[/blue]"
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

    # By parsing all the arguments until here, we are able to bypass the need
    # to fill the positional arguments
    parsed, _ = parser.parse_known_args()

    if parsed.list_interfaces:
        list_interfaces()
        exit(constants.EXIT_SUCCESS)

    # This will be parsed after checking all optional arguments
    positional_args.add_argument(
        'a',
        help='[blue]a first argument[/blue]'
    )

    # Move the help menu here in order to include the positional arguments
    optional_args.add_argument(
        '-h',
        '--help',
        action='help',
        default=argparse.SUPPRESS,
        help='[blue]Show this help message and exit.[/blue]'
    )

    return parser.parse_args()


async def run():
    args = create_parser()

    sniffer = SnifferEngine(args.interface, args.file)
    await render(args, sniffer)


def main():
    asyncio.run(run())


if __name__ == '__main__':
    main()
