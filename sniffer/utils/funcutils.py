import sys
import rich
from rich.panel import Panel
from . import constants


def handle_error(message):
    rich.print(Panel(f'{message}.',
                     title="[red]ERROR[/red]",
                     title_align="left",
                     expand=False,
                     style="bold red"))
    sys.exit(constants.EXIT_FAILURE)
