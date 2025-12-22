#!/usr/bin/env bash
#
# Setup script - validates all dependencies are installed
#
# Usage:
#   ./scripts/setup.sh
#

set -euo pipefail

echo "Checking dependencies..."
echo ""

errors=0

# Check Python
if command -v python3 &> /dev/null; then
    version=$(python3 --version 2>&1)
    echo "✅ Python: $version"
else
    echo "❌ Python 3 not found"
    echo "   Install: https://www.python.org/downloads/"
    ((errors++)) || true
fi

# Check pip
if command -v pip3 &> /dev/null || command -v pip &> /dev/null; then
    echo "✅ pip: installed"
else
    echo "❌ pip not found"
    echo "   Install: python3 -m ensurepip"
    ((errors++)) || true
fi

# Check PyYAML
if python3 -c "import yaml" 2>/dev/null; then
    echo "✅ PyYAML: installed"
else
    echo "❌ PyYAML not found"
    echo "   Install: pip install pyyaml"
    ((errors++)) || true
fi

# Check yq
if command -v yq &> /dev/null; then
    version=$(yq --version 2>&1 | head -1)
    echo "✅ yq: $version"
else
    echo "❌ yq not found"
    echo "   Install:"
    echo "     brew install yq       # macOS"
    echo "     pacman -S yq          # Arch Linux"
    echo "     apt install yq        # Debian/Ubuntu"
    echo "     pip install yq        # pip"
    ((errors++)) || true
fi

# Check git
if command -v git &> /dev/null; then
    version=$(git --version 2>&1)
    echo "✅ git: $version"
else
    echo "❌ git not found"
    ((errors++)) || true
fi

# Check scripts are executable
echo ""
echo "Checking scripts..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for script in "$SCRIPT_DIR"/*.py "$SCRIPT_DIR"/*.sh; do
    if [ -f "$script" ]; then
        name=$(basename "$script")
        if [ -x "$script" ]; then
            echo "✅ $name: executable"
        else
            echo "⚠️  $name: not executable (fixing...)"
            chmod +x "$script"
            echo "   Fixed!"
        fi
    fi
done

echo ""

if [ $errors -eq 0 ]; then
    echo "========================================="
    echo "✅ All dependencies satisfied!"
    echo "========================================="
    echo ""
    echo "Next steps:"
    echo "  ./scripts/check-yaml.py          # Validate YAML"
    echo "  ./scripts/generate-tables.py     # Generate tables"
    echo "  ./scripts/clone-all.sh --shallow # Clone repos"
    exit 0
else
    echo "========================================="
    echo "❌ $errors dependency issue(s) found"
    echo "========================================="
    echo ""
    echo "Please install missing dependencies and run again."
    exit 1
fi
