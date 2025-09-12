"""
Configurazione Sphinx avanzata per documentazione multi-versione
"""

import os
import sys
from datetime import datetime

# Aggiungi il path del progetto
sys.path.insert(0, os.path.abspath(".."))

# -- Informazioni del progetto ------------------------------------------------

project = "errepi-py"
copyright = f"{datetime.now().year}, Errepi Net S.R.L."  # Sostituisci
author = "Valerio Faiuolo"  # Sostituisci

# Versione del progetto
try:
    # Prova a leggere la versione da setup.py o __init__.py
    import importlib.util
    import re

    # Cerca la versione in vari file
    version_files = [
        "../setup.py",
    ]

    version = "unknown"
    for file_path in version_files:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                match = re.search(r'version\s*=\s*["\']([^"\']*)["\']', content)
                if match:
                    version = match.group(1)
                    break

    release = version
except Exception as e:
    print(f"Warning: Could not determine version: {e}")
    version = "latest"
    release = "latest"

# -- Configurazione generale --------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",  # Documentazione automatica dai docstring
    "sphinx.ext.autosummary",  # Riassunti automatici
    "sphinx.ext.viewcode",  # Link al codice sorgente
    "sphinx.ext.napoleon",  # Supporto per docstring Google/NumPy
    "sphinx.ext.intersphinx",  # Link alla documentazione esterna
    "sphinx.ext.todo",  # Supporto per TODO
    "sphinx.ext.coverage",  # Controllo copertura documentazione
    "sphinx.ext.githubpages",  # Supporto GitHub Pages
    "sphinx.ext.mathjax",  # Supporto per formule matematiche
]

# File da escludere
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Lingua
language = "en"  # Cambia in 'en' se preferisci inglese

# -- Opzioni per l'output HTML ------------------------------------------------

html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "canonical_url": "",
    "analytics_id": "",  # Inserisci Google Analytics ID se hai
    "logo_only": False,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "vcs_pageview_mode": "",
    "style_nav_header_background": "#2980B9",
    # Toc options
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
    "version_selector": True,
}


# File CSS/JS personalizzati
html_css_files = [
    "custom.css",  # Crea questo file per personalizzazioni
]

html_js_files = [
    "custom.js",  # Crea questo file per JavaScript personalizzato
]

# Contesto per il template (utile per GitHub Pages)
html_context = {
    "display_github": False,
}

# Configurazione sidebar
html_sidebars = {
    "**": [
        "versions.html",  # Template personalizzato per le versioni
        "navigation.html",
        "relations.html",
        "searchbox.html",
        "donate.html",
    ]
}

# -- Configurazione autodoc ---------------------------------------------------

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

# Configura autosummary
autosummary_generate = True
autosummary_imported_members = True

# -- Configurazione Napoleon --------------------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# -- Configurazione intersphinx -----------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "requests": ("https://requests.readthedocs.io/en/latest/", None),
}

# -- Configurazione TODO ------------------------------------------------------

todo_include_todos = True

# -- Configurazione per GitHub Pages ------------------------------------------

# Disabilita Jekyll per GitHub Pages
html_extra_path = [".nojekyll"]

# -- Messaggio di benvenuto ---------------------------------------------------

print(f"Building documentation for {project} v{version}")
print(f"Theme: {html_theme}")
print("=" * 50)
