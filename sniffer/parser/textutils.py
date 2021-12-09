from .. import __version__
import subprocess

version = __version__.__version__
commit_hash = subprocess.run(
    ['git', 'rev-parse', '--short', 'HEAD'],
    capture_output=True).stdout.decode('utf-8').strip()
commit_hash = f'[bold cyan]{commit_hash}[/bold cyan]'

BANNER = f"""\
                     ██████╗ ██╗  ██╗███████╗
                    ██╔════╝ ██║  ██║██╔════╝   [Author: Roșca Ionuț]
                    ██║  ███╗███████║███████╗   [License: GPL-3.0 License]
                    ██║   ██║██╔══██║╚════██║   [Version: {version}]
                    ╚██████╔╝██║  ██║███████║   [Commit: {commit_hash}]
                     ╚═════╝ ╚═╝  ╚═╝╚══════╝
                  ＧＵＩ ＨＴＴＰ ＳＮＩＦＦＥＲ
"""
