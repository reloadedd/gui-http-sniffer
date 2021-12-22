import sys
import rich
import subprocess
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


def get_commit_hash() -> str:
    """Return the current commit hash."""
    return subprocess.run(['git', 'rev-parse', '--short', 'HEAD'],
                          capture_output=True).stdout.decode('utf-8').strip()
