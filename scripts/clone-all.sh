#!/bin/bash
# Clone all project repositories to tmp/ for analysis
# Usage: ./scripts/clone-all.sh [--update]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
TMP_DIR="$REPO_ROOT/tmp"
PROJECTS_DIR="$REPO_ROOT/projects"

mkdir -p "$TMP_DIR"

UPDATE_MODE=false
if [[ "$1" == "--update" ]]; then
    UPDATE_MODE=true
    echo "Running in update mode..."
fi

# Extract repo URLs from YAML files
for yaml_file in "$PROJECTS_DIR"/*.yaml; do
    if [[ ! -f "$yaml_file" ]]; then
        continue
    fi

    # Extract repo-url from YAML
    repo_url=$(grep -E "^repo-url:" "$yaml_file" | sed 's/repo-url: *["'"'"']\?\([^"'"'"']*\)["'"'"']\?/\1/' | tr -d ' ')

    if [[ -z "$repo_url" ]]; then
        echo "Warning: No repo-url found in $yaml_file"
        continue
    fi

    # Skip non-GitHub URLs (e.g., npmjs.com, crates.io)
    if [[ ! "$repo_url" =~ github\.com ]]; then
        echo "Skipping non-GitHub URL: $repo_url"
        continue
    fi

    # Extract owner/repo from URL
    owner_repo=$(echo "$repo_url" | sed -E 's|https://github\.com/([^/]+/[^/]+).*|\1|')

    if [[ -z "$owner_repo" ]]; then
        echo "Warning: Could not extract owner/repo from $repo_url"
        continue
    fi

    # Create directory name
    dir_name=$(echo "$owner_repo" | tr '/' '--')
    target_dir="$TMP_DIR/$dir_name"

    if [[ -d "$target_dir" ]]; then
        if $UPDATE_MODE; then
            echo "Updating $owner_repo..."
            (cd "$target_dir" && git pull --ff-only 2>/dev/null) || echo "  Failed to update (may have diverged)"
        else
            echo "Already exists: $dir_name"
        fi
    else
        echo "Cloning $owner_repo..."
        git clone --depth 1 "$repo_url" "$target_dir" 2>/dev/null || echo "  Failed to clone $repo_url"
    fi
done

echo ""
echo "Done. Repositories are in: $TMP_DIR"
echo "Total: $(ls -1 "$TMP_DIR" 2>/dev/null | wc -l) repositories"
