import typing
import argparse
import sys as _sys
from rich import print as rich_print

from ..utils.constants import *


class ColoredArgumentParser(argparse.ArgumentParser):
    """Custom argument parser with colored output.

    This class overrides the `argparse.ArgumentParser` from the Python
    Standard Library in order to add color to the help menu.
    """
    # =====================
    # Help-printing methods
    # =====================
    def print_usage(self, file: typing.TextIO = None) -> None:
        """Print the usage message for the script.

        Parameters
        ----------
        file : typing.TextIO, optional
            The file in which the message will be printed, defaults to `stderr`
        """
        if file is None:
            file = _sys.stdout
        self._print_message(self.format_usage(), file)

    def print_help(self, file: typing.TextIO = None) -> None:
        """Print the help message, describing the available options.

        Parameters
        ----------
        file : typing.TextIO, optional
            The file in which the message will be printed, defaults to `stderr`
        """
        if file is None:
            file = _sys.stdout
        self._print_message(self.format_help(), file)

    def _print_message(self, message: str, file: typing.TextIO = None) -> None:
        """Display the given message using syntax enhancing.

        Parameters
        ----------
        message : str
            The message to be printed
        file : typing.TextIO, optional
            The file in which the message will be printed, defaults to `stderr`
        """
        if message:
            if file is None:
                file = _sys.stderr
            rich_print(message, file=file)

    # =======================
    # Help-formatting methods
    # =======================
    def format_help(self) -> str:
        """Format the help message and return it as string."""
        formatter = self._get_formatter()

        # description
        formatter.add_text(self.description)

        # positionals, optionals and user-defined groups
        for action_group in self._action_groups:
            formatter.start_section(f'[red]{action_group.title}[/red]')
            formatter.add_text(action_group.description)
            # noinspection PyProtectedMember
            formatter.add_arguments(action_group._group_actions)
            formatter.end_section()

        # epilog
        formatter.add_text(self.epilog)

        # determine help from format above
        return formatter.format_help()

    def format_usage(self) -> str:
        """Format the usage message and return it as string."""
        formatter = self._get_formatter()

        # Remove the unwanted arguments from being displayed in usage
        unwanted = [_ for _ in self._actions if _.default == PARSER_IGNORE]
        for action in unwanted:
            self._actions.remove(action)

        formatter.add_usage(self.usage, self._actions,
                            self._mutually_exclusive_groups)
        return formatter.format_help()

    # ===============
    # Exiting methods
    # ===============
    def exit(self, status: int = 0, message: str = None) -> None:
        """Exit with `status`, optionally displaying an error message.

        Parameters
        ----------
        status : int, optional
            The exit status for the program, defaults to 0
        message:
            The message to be displayed upon exit
        """
        if message:
            self._print_message(f'[red]{message}[/red]', _sys.stderr)
        _sys.exit(status)
