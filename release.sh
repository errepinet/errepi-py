#!/bin/bash

# Release script for Python library
# Usage: ./release.sh <version> [--dry-run]

set -e

# Output colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Utility functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check parameters
if [ $# -eq 0 ]; then
    log_error "Specify the version to release"
    echo "Usage: $0 <version> [--dry-run]"
    echo "Example: $0 1.2.3"
    exit 1
fi

VERSION=$1
DRY_RUN=false

if [ "$2" = "--dry-run" ]; then
    DRY_RUN=true
    log_warning "Modalità DRY RUN attivata - nessuna modifica sarà applicata"
fi

# Validate version format (semantic versioning)
if ! [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    log_error "Invalid version format. Use semver format (e.g.: 1.2.3)"
    exit 1
fi

# Check that we are on main/master branch
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" != "main" && "$CURRENT_BRANCH" != "master" ]]; then
    log_error "You must be on the main/master branch to create a release"
    exit 1
fi

# Check that the repository is clean
if [ -n "$(git status --porcelain)" ]; then
    log_error "The repository has uncommitted changes. Commit or stash changes before continuing."
    exit 1
fi

# Check that we are up to date with remote
log_info "Checking for updates from remote..."
git fetch origin

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/$CURRENT_BRANCH)

if [ $LOCAL != $REMOTE ]; then
    log_error "Local branch is not up to date with remote. Run 'git pull' before continuing."
    exit 1
fi

# Check that the tag does not already exist
if git tag -l | grep -q "^v$VERSION$"; then
    log_error "Tag v$VERSION already exists"
    exit 1
fi

log_info "Preparing release v$VERSION..."

# Find setup.py or pyproject.toml to update the version
UPDATE_VERSION_FILE=""
if [ -f "setup.py" ]; then
    UPDATE_VERSION_FILE="setup.py"
    log_info "Found setup.py"
elif [ -f "pyproject.toml" ]; then
    UPDATE_VERSION_FILE="pyproject.toml"
    log_info "Found pyproject.toml"
else
    log_warning "setup.py or pyproject.toml not found. Version must be updated manually."
fi

# Update the version in the configuration file
if [ -n "$UPDATE_VERSION_FILE" ] && [ "$DRY_RUN" = false ]; then
    log_info "Updating version in $UPDATE_VERSION_FILE..."
    
    if [ "$UPDATE_VERSION_FILE" = "setup.py" ]; then
    # Update setup.py
        sed -i.bak "s/version=['\"][^'\"]*['\"]/version=\"$VERSION\"/g" setup.py
        rm setup.py.bak
    elif [ "$UPDATE_VERSION_FILE" = "pyproject.toml" ]; then
    # Update pyproject.toml
        sed -i.bak "s/version = ['\"][^'\"]*['\"]/version = \"$VERSION\"/g" pyproject.toml
        rm pyproject.toml.bak
    fi
    
    log_success "Version updated to $VERSION in $UPDATE_VERSION_FILE"
fi

# Update CHANGELOG.md if it exists
if [ -f "CHANGELOG.md" ] && [ "$DRY_RUN" = false ]; then
    log_info "Updating CHANGELOG.md..."
    
    # Create a backup
    cp CHANGELOG.md CHANGELOG.md.bak
    
    # Prepare the new entry
    DATE=$(date +%Y-%m-%d)
    TEMP_FILE=$(mktemp)
    
    # Create the new changelog
    echo "# Changelog" > $TEMP_FILE
    echo "" >> $TEMP_FILE
    echo "## [v$VERSION] - $DATE" >> $TEMP_FILE
    echo "" >> $TEMP_FILE
    echo "### Added" >> $TEMP_FILE
    echo "- " >> $TEMP_FILE
    echo "" >> $TEMP_FILE
    echo "### Changed" >> $TEMP_FILE
    echo "- " >> $TEMP_FILE
    echo "" >> $TEMP_FILE
    echo "### Fixed" >> $TEMP_FILE
    echo "- " >> $TEMP_FILE
    echo "" >> $TEMP_FILE
    
    # Add the rest of the existing changelog (skip the first line "# Changelog")
    tail -n +2 CHANGELOG.md >> $TEMP_FILE
    
    mv $TEMP_FILE CHANGELOG.md
    rm CHANGELOG.md.bak
    
    log_success "CHANGELOG.md updated"
    log_warning "REMEMBER to edit CHANGELOG.md with actual changes before committing!"
fi

# Run tests if they exist
if [ -f "pytest.ini" ] || [ -f "tox.ini" ] || [ -d "tests" ]; then
    log_info "Running tests..."
    if [ "$DRY_RUN" = false ]; then
        if command -v pytest &> /dev/null; then
            pytest
        elif command -v python -m pytest &> /dev/null; then
            python -m pytest
        else
            log_warning "pytest not found, skipping tests"
        fi
    else
    log_info "[DRY RUN] Skipping test execution"
    fi
fi

# Commit changes
if [ "$DRY_RUN" = false ]; then
    if [ -n "$(git status --porcelain)" ]; then
    log_info "Committing changes for version $VERSION..."
        git add .
        git commit -m "Bump version to v$VERSION"
    fi
    
    # Create the tag
    log_info "Creating tag v$VERSION..."
    git tag -a "v$VERSION" -m "Release version $VERSION"
    
    # Push branch and tag
    log_info "Pushing changes and tag..."
    git push origin $CURRENT_BRANCH
    git push origin "v$VERSION"
    
    log_success "Release v$VERSION created successfully!"
    log_info "Tag v$VERSION has been pushed to origin"
    log_info "Documentation will be generated automatically via GitHub Actions"
    
else
    log_info "[DRY RUN] The following operations would have been performed:"
    log_info "  - Commit changes with message 'Bump version to v$VERSION'"
    log_info "  - Create tag v$VERSION"
    log_info "  - Push branch $CURRENT_BRANCH"
    log_info "  - Push tag v$VERSION"
fi

echo ""
log_success "Release script completed!"

if [ "$DRY_RUN" = false ]; then
    echo ""
    echo "Next steps:"
    echo "1. Check that the GitHub Actions workflow is active"
    echo "2. Documentation will be available at:"
    echo "   https://$(git config --get remote.origin.url | sed 's/.*github.com[\/\:]//g' | sed 's/.git$//g' | tr '[:upper:]' '[:lower:]' | sed 's/\//.github.io\//g')"
    echo "3. Consider creating a GitHub release with release notes"
fi