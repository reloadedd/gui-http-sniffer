# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2021-12-14
### Added
- Add instructions on how to build the docs, resources and information about 
the git branching model on `README.md`
- Add `tools/bump_version.sh` Bash script that updates the version on all 
required places.

### Changed
- All tags will be also cryptographically signed (the commits are already) 
with the following key: `DE7E4A0D4C55B4AC` (GPG key ID: `4AEE18F83AFDEB23`)


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


[Unreleased]: https://github.com/reloadedd/gui-http-sniffer/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/reloadedd/gui-http-sniffer/releases/tag/v0.1.0
