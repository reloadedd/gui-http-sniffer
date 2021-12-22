from .. import __version__
from ..utils.funcutils import get_commit_hash
from rich.console import Console

# Global object which will be used throughout the whole package
console = Console()

version = f'[bold cyan]v{__version__.__version__}[/bold cyan]'
commit_hash = f'[bold cyan]{get_commit_hash()}[/bold cyan]'

BANNER = f"""\
                     ██████╗ ██╗  ██╗███████╗
                    ██╔════╝ ██║  ██║██╔════╝   [Author: Roșca Ionuț]
                    ██║  ███╗███████║███████╗   [License: GPL-3.0]
                    ██║   ██║██╔══██║╚════██║   [Version: {version}]
                    ╚██████╔╝██║  ██║███████║   [Commit: {commit_hash}]
                     ╚═════╝ ╚═╝  ╚═╝╚══════╝
                  ＧＵＩ ＨＴＴＰ ＳＮＩＦＦＥＲ
"""

EPILOG = "© Copyright 2021-2022, Roșca Ionuț."
