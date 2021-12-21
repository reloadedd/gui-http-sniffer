import sys
import rich
from rich.panel import Panel
from . import constants


def handle_error(message: str) -> None:
    """Display a visible error message and exit the program.

    Parameters
    ----------
    message : str
        The message to be displayed
    """
    rich.print(Panel(f'{message}.',
                     title="[red]ERROR[/red]",
                     title_align="left",
                     expand=False,
                     style="bold red"))
    sys.exit(constants.EXIT_FAILURE)
