#!/usr/bin/env bash

if [[ "$#" != "1" ]]; then
  echo "Usage: $0 <version>"
  exit 1
fi

if [[ "$(basename "$(pwd)")" != "tools" ]]; then
  echo -e "ERROR\tGo to the tools/ folder and execute from there."
  exit 1
fi

# Files to be updates
SNIFFER_VERSION='../sniffer/__version__.py'
SPHINX_VERSION='../docs/source/conf.py'

PREVIOUS_VERSION="$(grep __version__  $SNIFFER_VERSION | cut -d "'" -f2)"

echo -e "INFO\tUpdating version for sniffer package..."
sed "s/__version__ = '${PREVIOUS_VERSION}'/__version__ = '$1'/" $SNIFFER_VERSION

echo -e "INFO\tUpdating version for Sphinx docs..."
sed "s/release = '${PREVIOUS_VERSION}'/release = '$1'/" $SPHINX_VERSION
