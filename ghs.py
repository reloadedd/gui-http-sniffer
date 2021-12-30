#!/usr/bin/env python3

"""
                         ██████╗ ██╗  ██╗███████╗
                        ██╔════╝ ██║  ██║██╔════╝
                        ██║  ███╗███████║███████╗
                        ██║   ██║██╔══██║╚════██║
                        ╚██████╔╝██║  ██║███████║
                         ╚═════╝ ╚═╝  ╚═╝╚══════╝
                        ＧＵＩ ＨＴＴＰ ＳＮＩＦＦＥＲ
                            𝖇𝖞 𝕽𝖔𝖘𝖈𝖆 𝕴𝖔𝖓𝖚𝖙

This is the entry point script for the sniffer package. It imports the package
and then calls its `main()` function, which causes some default code to be
executed.

The package can be called in 3 ways:
    1. Using this script, `./ghs.py -h` and you're good to go
    2. Using Python's module import, `python -m sniffer -h` assuming you are
        in the right folder, relative to the sniffer package.
    3. By importing the whole package and executing the zip file, this will
        cause Python to search the zip for the `__main__.py` file and run it.
        This is how to do it: `python <zip_file>`, where <zip_file> is your zip
"""

import sniffer


def main() -> None:
    """Main driver of the program."""
    sniffer.main()


if __name__ == '__main__':
    main()
