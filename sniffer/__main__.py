"""GUI HTTP Sniffer

This script allows the user to print to the console all columns in the
spreadsheet. It is assumed that the first row of the spreadsheet is the
location of the columns.

This file can also be imported as a module and contains the following
functions:

    * get_spreadsheet_cols - returns the column headers of the file
    * main - the main function of the script
"""

from .parser.ColoredArgumentParser import ColoredArgumentParser
from .__version__ import __version__
import argparse
import sys
from .parser.textutils import BANNER
from argparse import RawDescriptionHelpFormatter


def run():
    parser = ColoredArgumentParser(
        # description=f'[green]{BANNER}\n{__doc__}[/green]',
        description=f'{BANNER}\n{__doc__}',
        formatter_class=RawDescriptionHelpFormatter,
        add_help=False,
        epilog='Copyright © 2021-2022 Roșca Ionuț'
    )

    positional_args = parser.add_argument_group('POSITIONAL ARGUMENTS')
    optional_args = parser.add_argument_group('OPTIONAL ARGUMENTS')
    usage = parser.add_argument_group('USAGE')

    optional_args.add_argument('-f',
                        '--filter',
                        # action='version',
                       default=argparse.SUPPRESS,
                       help='[blue]Filter expression to be aplied when '
                            'sniffing traffic.[/blue]')

    positional_args.add_argument('a',
                        help='[blue]a first argument[/blue]')
    optional_args.add_argument('-n',
                        '--no-color',
                        help='[blue]Disable output coloring.[/blue]',
                        action='version')

    optional_args.add_argument('-v', '--version', action='version',
                        version=f'%(prog)s {__version__}',
                        help="[blue]Show program's version number and exit.[/blue]")
    optional_args.add_argument('-h', '--help', action='help',
                        default=argparse.SUPPRESS,
                        help='[blue]Show this help message and exit.[/blue]')

    # Mood update: feeling determined
    usage.add_argument(
        f'[u]{parser.format_usage()[7: 7 + len(sys.argv[0][2:])]}[/u]'
        f'{parser.format_usage()[7 + len(sys.argv[0][2:]):]}'
    )

    args = parser.parse_args()

    # parser.print_help()
    # parser.print_usage()


if __name__ == '__main__':
    run()
