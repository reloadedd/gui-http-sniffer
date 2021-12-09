"""GUI HTTP Sniffer

This script allows the user to print to the console all columns in the
spreadsheet. It is assumed that the first row of the spreadsheet is the
location of the columns.

This tool accepts comma separated value files (.csv) as well as excel
(.xls, .xlsx) files.

This script requires that `pandas` be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions:

    * get_spreadsheet_cols - returns the column headers of the file
    * main - the main function of the script
"""

from .parser.ColoredArgumentParser import ColoredArgumentParser
import argparse


def run():
    parser = ColoredArgumentParser(
        description=f'[green]{__doc__}[/green]',
        add_help=False,
        epilog='Copyright © 2021-2022 Roșca Ionuț'
    )

    parser.add_argument('-f',
                        '--filter',
                        help='[blue]Florin Salam regele manelelor[/blue]')

    parser.add_argument('a',
                        help='[blue]a first argument[/blue]')
    parser.add_argument('--no-color',
                        help='[blue]Disable output coloring.[/blue]')

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 1.0',
                        help="[blue]Show program's version number and exit.[/blue]")
    parser.add_argument('-h', '--help', action='help',
                        default=argparse.SUPPRESS,
                        help='[blue]Show this help message and exit.[/blue]')

    args = parser.parse_args()

    parser.print_help()
    # parser.print_usage()
