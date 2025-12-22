#!/usr/bin/env bash
#
# Clone all repositories listed in projects/*.yaml to tmp/
#
# Usage:
#   ./scripts/clone-all.sh [OPTIONS]
#
# Options:
#   --shallow    Shallow clone (--depth 1)
#   --update     Update existing clones with git pull
#   --help       Show this help
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TMP_DIR="$PROJECT_ROOT/tmp"

# Check for yq dependency
if ! command -v yq &> /dev/null; then
    echo "❌ Error: yq is required but not installed."
    echo ""
    echo "Install with:"
    echo "  brew install yq       # macOS"
    echo "  pip install yq        # pip"
    echo "  pacman -S yq          # Arch Linux"
    echo "  apt install yq        # Debian/Ubuntu"
    exit 1
fi

# Parse arguments
SHALLOW=false
UPDATE=false

for arg in "$@"; do
    case $arg in
        --shallow)
            SHALLOW=true
            ;;
        --update)
            UPDATE=true
            ;;
        --help)
            head -20 "$0" | grep "^#" | sed 's/^# //' | sed 's/^#//'
            exit 0
            ;;
    esac
done

# Increment helper (works with set -e)
incr() { eval "$1=\$((\$1 + 1))" || true; }

# Create tmp directory
mkdir -p "$TMP_DIR"

# Counters
total=0
cloned=0
updated=0
skip_count=0
failed=0

echo "Scanning projects/*.yaml for repositories..."
echo ""

for yaml_file in "$PROJECT_ROOT"/projects/*.yaml; do
    [ -f "$yaml_file" ] || continue

    # Skip .gitkeep and non-yaml files
    [[ "$yaml_file" == *.yaml ]] || continue

    incr total

    # Extract repo URL
    repo_url=$(yq -r '.repo-url // ""' "$yaml_file" 2>/dev/null || echo "")

    if [ -z "$repo_url" ]; then
        echo "WARN: No repo-url in $yaml_file"
        incr skip_count
        continue
    fi

    # Extract owner and repo from URL
    # Handles: https://github.com/owner/repo or https://github.com/owner/repo.git
    repo_path=$(echo "$repo_url" | sed -E 's|https?://[^/]+/||' | sed 's/\.git$//')
    owner=$(echo "$repo_path" | cut -d'/' -f1)
    repo=$(echo "$repo_path" | cut -d'/' -f2)

    if [ -z "$owner" ] || [ -z "$repo" ]; then
        echo "WARN: Could not parse owner/repo from $repo_url"
        incr skip_count
        continue
    fi

    target_dir="$TMP_DIR/${owner}--${repo}"

    if [ -d "$target_dir" ]; then
        if [ "$UPDATE" = true ]; then
            echo -n "📥 Updating: $owner/$repo ... "
            if (cd "$target_dir" && git pull --quiet 2>/dev/null); then
                commit=$(cd "$target_dir" && git rev-parse --short HEAD 2>/dev/null || echo "???")
                echo "✅ ($commit)"
                incr updated
            else
                echo "❌ failed"
                incr failed
            fi
        else
            echo "⏭️  Skip (exists): $owner/$repo"
            incr skip_count
        fi
    else
        echo -n "📦 Cloning: $owner/$repo ... "

        clone_args=()
        if [ "$SHALLOW" = true ]; then
            clone_args+=(--depth 1)
        fi

        if git clone "${clone_args[@]}" "$repo_url" "$target_dir" 2>/dev/null; then
            commit=$(cd "$target_dir" && git rev-parse --short HEAD 2>/dev/null || echo "???")
            echo "✅ ($commit)"
            incr cloned
        else
            echo "❌ failed"
            incr failed
        fi
    fi
done

echo ""
echo "========================================="
echo "Summary:"
echo "  Total YAML files:  $total"
echo "  Cloned:            $cloned"
echo "  Updated:           $updated"
echo "  Skipped:           $skip_count"
echo "  Failed:            $failed"
echo "========================================="
