"""
    GUI HTTP Sniffer i.e. GHS, is a layer-7 sniffer, targeting
    unencrypted HTTP traffic and is capable of reading and analyzing
    that traffic.
"""

import argparse
from .__version__ import __version__
from .parser.textutils import BANNER, EPILOG
from argparse import RawDescriptionHelpFormatter
from .parser.ColoredArgumentParser import ColoredArgumentParser
from .network.engine import SnifferEngine
from .utils.constants import PARSER_IGNORE
from .utils.funcutils import handle_error


def run():
    parser = ColoredArgumentParser(
        description=f'{BANNER}\n{__doc__}',
        formatter_class=RawDescriptionHelpFormatter,
        add_help=False,
        epilog=EPILOG
    )

    positional_args = parser.add_argument_group('POSITIONAL ARGUMENTS')
    positional_args.add_argument(
        'a',
        help='[blue]a first argument[/blue]'
    )

    optional_args = parser.add_argument_group('OPTIONAL ARGUMENTS')
    optional_args.add_argument(
        '-f',
        '--filter',
        default=argparse.SUPPRESS,
        help='[blue]Filter expression to be applied when sniffing traffic.'
             '[/blue]'
    )
    optional_args.add_argument(
        '-n',
        '--no-color',
        help='[blue]Disable output coloring.[/blue]',
        action='version'
    )
    optional_args.add_argument(
        '-i',
        '--interface',
        help='[blue]The network interface to be used. Default: any[/blue]',
        default='any',
        dest='interface'
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

    usage = parser.add_argument_group('USAGE')
    # Mood update: feeling determined
    usage.add_argument(
        f'[u]{parser.format_usage()[7: 7 + len(parser.prog)]}[/u]'
        f'{parser.format_usage()[7 + len(parser.prog):]}',
        default=PARSER_IGNORE,
        nargs='?'   # Bypass the required value for positional arguments
    )

    args = parser.parse_args()
    print(f'Using {args.interface}')

    try:
        sniffer = SnifferEngine(args.interface)
        sniffer.sniff()
    except PermissionError:
        handle_error("You need [i]root[/i] privileges in order to use raw "
                     "sockets")


if __name__ == '__main__':
    run()
