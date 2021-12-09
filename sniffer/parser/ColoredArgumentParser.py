import argparse
from argparse import HelpFormatter
import sys as _sys
from gettext import gettext

from rich import print as rich_print


class ColoredArgumentParser(argparse.ArgumentParser):
    """Custom argument parser with colored output.

    This class overrides the `argparse.ArgumentParser` from the Python
    Standard Library in order to add color to the help menu.

    Methods
    -------
    print_usage(file=None)
        Print the usage message for the script.
    print_help(file=None)
        Print the help message, describing the available options.
    """
    # =====================
    # Help-printing methods
    # =====================
    def print_usage(self, file=None):
        if file is None:
            file = _sys.stdout
        self._print_message(self.format_usage(), file)

    def print_help(self, file=None):
        if file is None:
            file = _sys.stdout
        self._print_message(self.format_help(), file)

    def _print_message(self, message, file=None):
        if message:
            if file is None:
                file = _sys.stderr
            # file.write(message)
            rich_print(message, file=file)

    # ===============
    # Exiting methods
    # ===============
    def exit(self, status=0, message=None):
        if message:
            self._print_message(f'[red]{message}[/red]', _sys.stderr)
        _sys.exit(status)
