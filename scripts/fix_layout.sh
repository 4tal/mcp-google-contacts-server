#!/bin/bash
set -e

if [ -d "src" ]; then
  echo "Using src layout"
else
  echo "Creating flat layout structure..."
  # Create pyproject.toml to handle the flat layout
  cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
packages = ["mcp_google_contacts_server"]

[tool.setuptools.package-data]
mcp_google_contacts_server = ["*.py"]
EOF
  
  # Create a package directory and copy Python files
  mkdir -p mcp_google_contacts_server
  cp *.py mcp_google_contacts_server/
  # Create an __init__.py file
  touch mcp_google_contacts_server/__init__.py
  echo "Flat layout structure created"
fi
