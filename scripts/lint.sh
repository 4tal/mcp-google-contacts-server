#!/bin/bash
# Linting script for MCP Google Contacts Server
# Runs all code quality checks

set -e  # Exit on any error

echo "🧹 Running code quality checks..."

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SRC_DIR="$PROJECT_ROOT/src"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
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
    print_warning "Dev dependencies not found. Installing..."
    uv sync --dev
fi

# Run Black (code formatting)
print_status "Running Black (code formatter)..."
if uv run black --check --diff src/; then
    print_success "Black formatting check passed"
else
    print_error "Black formatting issues found. Run 'uv run black src/' to fix."
    exit 1
fi

# Run isort (import sorting)
print_status "Running isort (import sorter)..."
if uv run isort --check-only --diff src/; then
    print_success "Import sorting check passed"
else
    print_error "Import sorting issues found. Run 'uv run isort src/' to fix."
    exit 1
fi

# Run flake8 (style and error checking)
print_status "Running flake8 (style checker)..."
if uv run flake8 src/; then
    print_success "Flake8 style check passed"
else
    print_error "Flake8 found style issues"
    exit 1
fi

# Run mypy (type checking)
print_status "Running mypy (type checker)..."
if uv run mypy src/; then
    print_success "MyPy type check passed"
else
    print_warning "MyPy found type issues (non-blocking)"
fi

print_success "All linting checks completed successfully! 🎉"

# Optional: Show quick stats
echo ""
echo "📊 Quick Stats:"
echo "   Lines of Python code: $(find src/ -name '*.py' -exec wc -l {} + | tail -1 | awk '{print $1}')"
echo "   Python files: $(find src/ -name '*.py' | wc -l)"
echo "   Total files in src/: $(find src/ -type f | wc -l)" 