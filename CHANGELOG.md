# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.3] - 2021-12-31
### Added
- Add a new reference in `README.md`

### Changed
- Update Sphinx configuration files to reflect the documentation up-to-date

## [0.5.2] - 2021-12-31
### Added
- Add missing docstrings

### Changed
- Put the text in the side panel into 2 separate panels
- Fixed incomplete docstrings

## [0.5.1] - 2021-12-30
### Added
- Implement `-f/--filter` option with the following filters:
  - `ip.src = <ip>`: Matches the source IP
  - `ip.dst = <ip>`: Matches the destination IP
  - `http.method = <method>`: Matches only the HTTP requests with the
specified method (GET, POST etc.)
  - `http.type = <type>`: Matches only the specified types of packets 
(`request` or `response`)

### Changed
- Replace or'ed types, i.e. `str | None`, with `typing.Any` because they
break compatibility with Python < 3.10
- Sniffing won't be available on Windows because of technical complications
(sorry Windows users)

### Security
- Fix crash caused by specially crafting packets that contained rich tags,
we'll consider this an RCE because it had the ability to alter program's
rendering of colors and ultimately, crash it

## [0.5.0] - 2021-12-30
### Added
- Add `-c/--count` option which allow for a fixed number of packets to be
captured by the sniffer
- Add `-o/--output` option which give the user the possibility to save the
output from sniffed packets to a file for later reviewing
- Improve the UI by displaying the HTTP packets formatted properly and stylish
  - The packets will fit in a panel and only take the required space to be
displayed, nothing more, nothing less

### Changed
- Rename the footer bar from **Information** to **Status**

## [0.4.0] - 2021-12-28
### Added
- Counters for total packets and HTTP packets inside the Sniffer Engine
- Make the `run` function async (main is just the caller of the `run` function,
kind of like a wrapper). This marks the beginning of the performance 
improvements that the Sniffer will receive.
- Integrate the sniffing engine with the rich display, showing packets as they
are captured in a nice screen mimicking a GUI

### Changed
- Capture all traffic and filter for HTTP packets instead of capturing only
IP packets, which misses some packets

### Removed
- Remove Layer 2 class because we are no longer sniffing the data link layer 
(remember, we are here only for HTTP)

### Fixed
- Fix positional arguments not showing in help menu

## [0.3.1] - 2021-12-22
### Added
- Create the Text User Interface (TUI) containing multiple columns, each one
with its own unique purpose
- Create the intro animation (in case you're wondering, it's from Watch Dogs)

### Fixed
- Fix docstrings and Sphinx files (those `.rst` files)

## [0.3.0] - 2021-12-22
### Added
- Create a new class for Layer 7 of OSI Model.
- Add banner in `README.md` file
- Create a new exception, `UninterestingPacketException`
- Add command-line argument for specifying the desired network interface,
`-i/--interface`
- Create `decorators.py` file inside `utils` package that will contain, you've
guessed it: decorators. Also, created the first decorator, `require_root` that
will exit if the user running the script isn't **root**
- Implement `-l/--list-interfaces` option, which will list all interfaces
present in the system together with their MAC address + IPv4/6 address

### Changed
- Update Sniffer's description in `README.md` file

### Fixed
- Fix Layer 4 header size being (wrongly) too broad

## [0.2.0] - 2021-12-19
### Added
- Implement Sniffer Engine, alpha version
- Together with the Sniffer Engine, create the Packet Analyzer
- A new package named `exceptions` has been created that will hold all
exceptions related to sniffer's components
- A class has been created for each OSI layer needed (Layers: 2, 3 and 4)

## [0.1.1] - 2021-12-14
### Added
- Add instructions on how to build the docs, resources and information about 
the git branching model on `README.md`
- Add `tools/bump_version.sh` Bash script that updates the version on all 
required places.

### Changed
- All tags will be also cryptographically signed (the commits are already) 
with the following key: `DE7E4A0D4C55B4AC`


## [0.1.0] - 2021-12-14
### Added
- Add this changelog
- Create the `sniffer` package, together with its sub-packages: `network`,
`utils` and `parser`
  - The `network` package contain code for actually sniffing traffic
  - The `parser` package is busy with appearance and text formatiing
  - The `utils` package provide helpers for various tasks
- Create custom parser, based on
[argparse.ArgumentParser](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser), 
which re-arranges the layout and adds coloring 🌠
- Add [Sphinx](https://www.sphinx-doc.org/en/master/) for auto-documenting code
- Add a cool banner on the help menu of the script, that also keeps track of
the version number and Git commit


[Unreleased]: https://github.com/reloadedd/gui-http-sniffer/compare/v0.5.3...HEAD
[0.1.0]: https://github.com/reloadedd/gui-http-sniffer/releases/tag/v0.1.0
[0.1.1]: https://github.com/reloadedd/gui-http-sniffer/releases/tag/v0.1.1
[0.2.0]: https://github.com/reloadedd/gui-http-sniffer/releases/tag/v0.2.0
[0.1.1]: https://github.com/reloadedd/gui-http-sniffer/releases/tag/v0.1.1
[0.2.0]: https://github.com/reloadedd/gui-http-sniffer/releases/tag/v0.2.0
[0.3.0]: https://github.com/reloadedd/gui-http-sniffer/releases/tag/v0.3.0
[0.3.1]: https://github.com/reloadedd/gui-http-sniffer/releases/tag/v0.3.1
[0.4.0]: https://github.com/reloadedd/gui-http-sniffer/releases/tag/v0.4.0
[0.5.0]: https://github.com/reloadedd/gui-http-sniffer/releases/tag/v0.5.0
[0.5.1]: https://github.com/reloadedd/gui-http-sniffer/releases/tag/v0.5.1
[0.5.2]: https://github.com/reloadedd/gui-http-sniffer/releases/tag/v0.5.2
[0.5.3]: https://github.com/reloadedd/gui-http-sniffer/releases/tag/v0.5.3
