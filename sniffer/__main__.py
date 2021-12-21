"""
    GUI HTTP Sniffer i.e. GHS, is a layer-7 sniffer, targeting
    unencrypted HTTP traffic and is capable of reading and analyzing
    that traffic.
"""

import argparse
from argparse import RawDescriptionHelpFormatter
from .__version__ import __version__
from .network.engine import SnifferEngine
from .utils.decorators import require_root
from .utils.constants import PARSER_IGNORE
from .parser.textutils import BANNER, EPILOG
from .parser.ColoredArgumentParser import ColoredArgumentParser


def create_parser():
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

    # Mood update: feeling determined
    # This is what I call 'o românească'
    usage = parser.add_argument_group('USAGE')
    usage.add_argument(
        f'[u]{parser.format_usage()[7: 7 + len(parser.prog)]}[/u]'
        f'{parser.format_usage()[7 + len(parser.prog):]}',
        default=PARSER_IGNORE,
        nargs='?'   # Bypass the required value for positional arguments
    )

    return parser.parse_args()


@require_root
def sniff(interface):
    sniffer = SnifferEngine(interface)
    sniffer.sniff()


def main():
    args = create_parser()
    print(f'Using {args.interface}')

    sniff(args.interface)


# Don't worry, this won't be called whenever you import the package in your
# script, only when run through a zip file or by using python -m ...
main()
