import argparse
import sys as _sys
from rich import print as rich_print


class ColoredArgumentParser(argparse.ArgumentParser):
    """Custom argument parser with colored output.

    This class overrides the `argparse.ArgumentParser` from the Python
    Standard Library in order to add color to the help menu.
    """
    # =====================
    # Help-printing methods
    # =====================
    def print_usage(self, file=None):
        """Print the usage message for the script."""
        if file is None:
            file = _sys.stdout
        self._print_message(self.format_usage(), file)

    def print_help(self, file=None):
        """Print the help message, describing the available options."""
        if file is None:
            file = _sys.stdout
        self._print_message(self.format_help(), file)

    def _print_message(self, message, file=None):
        """Display the given message using syntax enhancing."""
        if message:
            if file is None:
                file = _sys.stderr
            rich_print(message, file=file)

    def format_help(self):
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

    # ===============
    # Exiting methods
    # ===============
    def exit(self, status=0, message=None):
        """Exit with `status`, optionally displaying an error message."""
        if message:
            self._print_message(f'[red]{message}[/red]', _sys.stderr)
        _sys.exit(status)
