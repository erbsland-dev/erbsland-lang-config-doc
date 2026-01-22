#  Copyright (c) 2024-2025 Tobias Erbsland - Erbsland DEV. https://erbsland.dev
#  SPDX-License-Identifier: Apache-2.0

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# -- Project information -----------------------------------------------------
project = "Erbsland Configuration Language"
copyright = "2025, Erbsland DEV"
author = "Erbsland DEV"
release = "1.0"

# -- General configuration ---------------------------------------------------
extensions = ["sphinx_rtd_theme", "sphinx_design", "sphinx_copybutton", "_ext.styles"]
templates_path = ["_templates"]
exclude_patterns = ["build", "_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = [
    "custom.css",
]
html_js_files = [
    "overlay.js",
    "https://erbsland.dev/ext/fa7/js/all.min.js",
]


def setup(app):
    from _ext.pygments_elcl import ErbslandConfigurationLanguage

    app.add_lexer("erbsland-conf", ErbslandConfigurationLanguage)
