import sys
import rich
from . import constants


def handle_error(message):
    rich.print(f'[red]ERROR[/red]\t{message}.')
    sys.exit(constants.EXIT_FAILURE)
