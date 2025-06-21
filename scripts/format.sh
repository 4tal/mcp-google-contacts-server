#!/bin/bash
# Auto-formatting script for MCP Google Contacts Server
# Automatically fixes most code style issues

set -e  # Exit on any error

echo "🎨 Auto-formatting code..."

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Change to project directory
cd "$PROJECT_ROOT"

# Check if uv is available
if ! command -v uv &> /dev/null; then
    print_error "uv is not installed. Please install uv first: pip install uv"
    exit 1
fi

# Check if dev dependencies are installed
if ! uv run --quiet black --version &> /dev/null; then
    print_status "Dev dependencies not found. Installing..."
    uv sync --dev
fi

# Run isort (fix import sorting)
print_status "Fixing import order with isort..."
uv run isort src/
print_success "Import sorting completed"

# Run Black (fix code formatting)
print_status "Formatting code with Black..."
uv run black src/
print_success "Code formatting completed"

print_success "Auto-formatting completed! 🎉"

# Optionally run a quick check
echo ""
echo "🔍 Running quick check..."
if uv run --quiet flake8 --version &> /dev/null; then
    print_status "Quick flake8 check..."
    if uv run flake8 src/ --count --statistics; then
        print_success "Code looks good!"
    else
        echo ""
        echo "💡 Some issues remain that require manual fixing."
        echo "   Run './scripts/lint.sh' for detailed analysis."
    fi
else
    echo "💡 Run './scripts/lint.sh' to check for remaining issues."
fi 