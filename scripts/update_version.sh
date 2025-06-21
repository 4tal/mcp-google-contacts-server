#!/bin/bash
set -e

# Extract version from tag
VERSION=$1
echo "Updating version to: $VERSION"

# Replace version in setup.py
sed -i "s/version=\"[^\"]*\"/version=\"${VERSION}\"/g" setup.py
