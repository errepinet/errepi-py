#!/bin/bash

# Script di release per libreria Python
# Uso: ./release.sh <version> [--dry-run]

set -e

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funzioni di utilità
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

# Verifica parametri
if [ $# -eq 0 ]; then
    log_error "Specifica la versione da rilasciare"
    echo "Uso: $0 <version> [--dry-run]"
    echo "Esempio: $0 1.2.3"
    exit 1
fi

VERSION=$1
DRY_RUN=false

if [ "$2" = "--dry-run" ]; then
    DRY_RUN=true
    log_warning "Modalità DRY RUN attivata - nessuna modifica sarà applicata"
fi

# Validazione formato versione (semantic versioning)
if ! [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    log_error "Formato versione non valido. Usa il formato semver (es: 1.2.3)"
    exit 1
fi

# Verifica che siamo nel branch main/master
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" != "main" && "$CURRENT_BRANCH" != "master" ]]; then
    log_error "Devi essere nel branch main/master per creare una release"
    exit 1
fi

# Verifica che il repository sia pulito
if [ -n "$(git status --porcelain)" ]; then
    log_error "Il repository ha modifiche non committate. Committa o stash le modifiche prima di continuare."
    exit 1
fi

# Verifica che siamo aggiornati con remote
log_info "Verifico aggiornamenti dal remote..."
git fetch origin

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/$CURRENT_BRANCH)

if [ $LOCAL != $REMOTE ]; then
    log_error "Il branch locale non è aggiornato con il remote. Esegui 'git pull' prima di continuare."
    exit 1
fi

# Verifica che il tag non esista già
if git tag -l | grep -q "^v$VERSION$"; then
    log_error "Il tag v$VERSION esiste già"
    exit 1
fi

log_info "Preparazione release v$VERSION..."

# Trova il file setup.py o pyproject.toml per aggiornare la versione
UPDATE_VERSION_FILE=""
if [ -f "setup.py" ]; then
    UPDATE_VERSION_FILE="setup.py"
    log_info "Trovato setup.py"
elif [ -f "pyproject.toml" ]; then
    UPDATE_VERSION_FILE="pyproject.toml"
    log_info "Trovato pyproject.toml"
else
    log_warning "Non trovato setup.py o pyproject.toml. La versione dovrà essere aggiornata manualmente."
fi

# Aggiorna la versione nel file di configurazione
if [ -n "$UPDATE_VERSION_FILE" ] && [ "$DRY_RUN" = false ]; then
    log_info "Aggiornamento versione in $UPDATE_VERSION_FILE..."
    
    if [ "$UPDATE_VERSION_FILE" = "setup.py" ]; then
        # Aggiorna setup.py
        sed -i.bak "s/version=['\"][^'\"]*['\"]/version=\"$VERSION\"/g" setup.py
        rm setup.py.bak
    elif [ "$UPDATE_VERSION_FILE" = "pyproject.toml" ]; then
        # Aggiorna pyproject.toml
        sed -i.bak "s/version = ['\"][^'\"]*['\"]/version = \"$VERSION\"/g" pyproject.toml
        rm pyproject.toml.bak
    fi
    
    log_success "Versione aggiornata a $VERSION in $UPDATE_VERSION_FILE"
fi

# Aggiorna CHANGELOG.md se esiste
if [ -f "CHANGELOG.md" ] && [ "$DRY_RUN" = false ]; then
    log_info "Aggiornamento CHANGELOG.md..."
    
    # Crea un backup
    cp CHANGELOG.md CHANGELOG.md.bak
    
    # Prepara il nuovo entry
    DATE=$(date +%Y-%m-%d)
    TEMP_FILE=$(mktemp)
    
    # Crea il nuovo changelog
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
    
    # Aggiungi il resto del changelog esistente (salta la prima riga "# Changelog")
    tail -n +2 CHANGELOG.md >> $TEMP_FILE
    
    mv $TEMP_FILE CHANGELOG.md
    rm CHANGELOG.md.bak
    
    log_success "CHANGELOG.md aggiornato"
    log_warning "RICORDATI di editare CHANGELOG.md con le modifiche effettive prima del commit!"
fi

# Esegui test se esistono
if [ -f "pytest.ini" ] || [ -f "tox.ini" ] || [ -d "tests" ]; then
    log_info "Esecuzione test..."
    if [ "$DRY_RUN" = false ]; then
        if command -v pytest &> /dev/null; then
            pytest
        elif command -v python -m pytest &> /dev/null; then
            python -m pytest
        else
            log_warning "pytest non trovato, saltando i test"
        fi
    else
        log_info "[DRY RUN] Saltando esecuzione test"
    fi
fi

# Commit delle modifiche
if [ "$DRY_RUN" = false ]; then
    if [ -n "$(git status --porcelain)" ]; then
        log_info "Commit delle modifiche per la versione $VERSION..."
        git add .
        git commit -m "Bump version to v$VERSION"
    fi
    
    # Crea il tag
    log_info "Creazione tag v$VERSION..."
    git tag -a "v$VERSION" -m "Release version $VERSION"
    
    # Push del branch e del tag
    log_info "Push delle modifiche e del tag..."
    git push origin $CURRENT_BRANCH
    git push origin "v$VERSION"
    
    log_success "Release v$VERSION creata con successo!"
    log_info "Il tag v$VERSION è stato pushato su origin"
    log_info "La documentazione sarà generata automaticamente tramite GitHub Actions"
    
else
    log_info "[DRY RUN] Le seguenti operazioni sarebbero state eseguite:"
    log_info "  - Commit delle modifiche con messaggio 'Bump version to v$VERSION'"
    log_info "  - Creazione tag v$VERSION"
    log_info "  - Push del branch $CURRENT_BRANCH"
    log_info "  - Push del tag v$VERSION"
fi

echo ""
log_success "Script di release completato!"

if [ "$DRY_RUN" = false ]; then
    echo ""
    echo "Prossimi passi:"
    echo "1. Verifica che il workflow GitHub Actions sia attivo"
    echo "2. La documentazione sarà disponibile a:"
    echo "   https://$(git config --get remote.origin.url | sed 's/.*github.com[\/:]//g' | sed 's/.git$//g' | tr '[:upper:]' '[:lower:]' | sed 's/\//.github.io\//g')"
    echo "3. Considera di creare una release su GitHub con le note di rilascio"
fi