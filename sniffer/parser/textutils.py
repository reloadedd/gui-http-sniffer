from .. import __version__
from rich.console import Console
import subprocess

console = Console()

version = f'[bold cyan]v{__version__.__version__}[/bold cyan]'
commit_hash = subprocess.run(
    ['git', 'rev-parse', '--short', 'HEAD'],
    capture_output=True).stdout.decode('utf-8').strip()
commit_hash = f'[bold cyan]{commit_hash}[/bold cyan]'

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
