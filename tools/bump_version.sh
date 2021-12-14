#!/usr/bin/env bash

if [[ "$#" != "1" ]]; then
  echo "Usage: $0 <version>"
  exit 1
fi

if [[ "$(basename "$(pwd)")" != "tools" ]]; then
  echo -e "ERROR\tGo to the tools/ folder and execute from there."
  exit 1
fi

if [[ "${1::1}" == "v" ]]; then
  echo -e "ERROR\tBro, we don't do that here. Cut that 'v' out."
  exit 1
fi

# Files to be updates
SNIFFER_VERSION='../sniffer/__version__.py'
SPHINX_VERSION='../docs/source/conf.py'
CHANGELOG='../CHANGELOG.md'

PREVIOUS_VERSION="$(grep __version__  $SNIFFER_VERSION | cut -d "'" -f2)"

echo -e "INFO\tUpdating version for sniffer package..."
sed -i "s/__version__ = '${PREVIOUS_VERSION}'/__version__ = '$1'/" $SNIFFER_VERSION

echo -e "INFO\tUpdating version for Sphinx docs..."
sed -i "s/release = '${PREVIOUS_VERSION}'/release = '$1'/" $SPHINX_VERSION

echo -e "INFO\tUpdating CHANGELOG version..."
echo -e "[$1]: https://github.com/reloadedd/gui-http-sniffer/releases/tag/v$1" >> $CHANGELOG
sed -i "s_compare/v${PREVIOUS_VERSION}...HEAD_compare/v$1...HEAD_" $CHANGELOG
