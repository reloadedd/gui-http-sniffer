# GUI HTTP Sniffer

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg" alt="Made with Python"></a>
  <a href="https://www.sphinx-doc.org/"><img src="https://img.shields.io/badge/Made%20with-Sphinx-1f425f.svg" alt="Made with Sphinx"></a>
  <a href="https://www.python.org/downloads/release/python-3101/"><img src="https://img.shields.io/badge/python-3.10-blue.svg" alt="Python 3.10"></a>
  <a href="https://linux.org/pages/download/"><img src="https://svgshare.com/i/Zhy.svg" alt="Linux"></a>
  <a href="https://opensource.org/licenses/GPL-3.0/"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="GitHub license"></a>
</p>


```

                 *     .--.
                      / /  `
     +               | |
            '         \ \__,
        *          +   '--'  *
          +   /\
+           .'  '.  *    ███████╗        ██╗  ██╗            ███████╗
    *      /======\  +   ██╔════╝        ██║  ██║            ██╔════╝
          ;:.  _   ;     ██║  ███╗       ███████║            ███████╗
          |:. (_)  |     ██║   ██║       ██╔══██║___ ___  __ ╚════██║        ___  ___  ___  __ 
          |:.  _   |     ╚██████╔╝|  | | ██║  ██║ |   |  |__)███████║|\ | | |__  |__  |__  |__)
  +       |:. (_)  |   *  ╚═════╝ \__/ | ╚═╝  ╚═╝ |   |  |   ╚══════╝| \| | |    |    |___ |  \
          ;:.      ;                         🌠 𝖇𝖞 𝕽𝖔𝖘𝖈𝖆 𝕴𝖔𝖓𝖚𝖙
        .' \:.    / `.
       / .-'':._.'`-. \
       |/    /||\    \|
    jgs _..--"""````"""--.._
  _.-'``                    ``'-._
-'                                '-

```

<p align="center">
<i>GUI HTTP Sniffer</i> i.e. <b>GHS</b>, is a layer-7 sniffer, targeting
unencrypted HTTP traffic and is capable of reading and analyzing
that traffic. It also supports, among others, basic traffic filtering and 
sniffing specific network interfaces.
</p>

## Building Documentation
Go to `docs/` directory and run `make html`. A new directory called `build/`
will be created inside the `docs/` directory, and you can open 
`docs/build/html/index.html` with a web browser to view the documentation.

## Git Branching Model
Starting with `v0.1.1`, this repository implements the 
[Gitflow model](https://nvie.com/posts/a-successful-git-branching-model/).
Note that this repository uses `/` instead of `-` for naming branches. 
e.g.: `feature/whatever` instead of `feature-whatever`.

What's important to know:
- If you want to go back in time to a specific version, you can find it's
associated branch: `release/<version>`
- What's in `master` is "production-ready"

## Resources
- RFC 791 - [IP Header Format](https://datatracker.ietf.org/doc/html/rfc791#section-3.1)
- RFC 793 - [TCP Header Format](https://datatracker.ietf.org/doc/html/rfc793#section-3.1)
- Python [struct](https://docs.python.org/3/library/struct.html) module
- Python [socket](https://docs.python.org/3/library/socket.html) module
- rich module's [Read The Docs](https://rich.readthedocs.io/en/stable/)
- rich module's [Github Page](https://github.com/willmcgugan/rich)
- What is the difference between `recv` and `recvfrom`? [Let's find out](https://forums.codeguru.com/showthread.php?218423-What-is-the-difference-between-recv-and-recvfrom)
- Value for the protocol argument in `socket()` call: [htons(0x800)](https://stackoverflow.com/a/46224239)
- Linux cooked-mode capture: [Wireshark docs](https://wiki.wireshark.org/SLL)
- Socket options list: [Shichao's Notes](https://notes.shichao.io/unp/ch7/)
- Async IO in Python: A Complete Walkthrough: [Real Python](https://realpython.com/async-io-python/)
- Auto-Documenting a Python Project Using Sphinx: [BetterProgramming](https://betterprogramming.pub/auto-documenting-a-python-project-using-sphinx-8878f9ddc6e9)

## Changelog
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). In order to view the
changes for each version, please consult the [CHANGELOG](CHANGELOG.md) file.

## License
The `GUI HTTP Sniffer` project is available under the GNU General Public License v3.0 License.
For the full license text please read the [LICENSE](LICENSE) file.
