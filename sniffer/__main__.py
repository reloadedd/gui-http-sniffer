"""
    GUI HTTP Sniffer i.e. GHS, is a layer-7 sniffer, targeting
    unencrypted HTTP traffic and is capable of reading and analyzing
    that traffic.
"""

import sys
import asyncio
import argparse
from .__version__ import __version__
from .network.engine import SnifferEngine
from .utils.constants import EXIT_SUCCESS
from .utils.decorators import require_root
from .utils.constants import PARSER_IGNORE
from .parser.options import list_interfaces
from .parser.textutils import BANNER, EPILOG
from .parser.custom import ColoredArgumentParser
from .tui.display import render


def create_parser():
    parser = ColoredArgumentParser(
        prog='sniffer' if sys.argv[0] == '-m' else sys.argv[0],
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
        default=PARSER_IGNORE,
        nargs='?'   # Bypass the required value for positional arguments
    )

    # By parsing all the arguments until here, we are able to bypass the need
    # to fill the positional arguments
    parsed, _ = parser.parse_known_args()

    if parsed.list_interfaces:
        list_interfaces()
        exit(EXIT_SUCCESS)

    # This will be parsed after checking all optional arguments
    positional_args.add_argument(
        'a',
        help='[blue]a first argument[/blue]'
    )

    return parser.parse_args()


async def sniff(interface):
    sniffer = SnifferEngine(interface)
    # print(sniffer.total_packet_count)
    await sniffer.sniff(300)


async def run():
    args = create_parser()

    # await sniff(args.interface)
    render(args)


@require_root
def main():
    asyncio.run(run())


if __name__ == '__main__':
    main()
