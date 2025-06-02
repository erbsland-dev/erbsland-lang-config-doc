#  Copyright (c) 2024. Erbsland DEV. https://erbsland.dev
#  SPDX-License-Identifier: Apache-2.0

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

project = "Erbsland Configuration Language"
copyright = "2025, Erbsland DEV"
author = "Erbsland DEV"
release = "1.0"
extensions = ["sphinx_rtd_theme", "_ext.styles", "sphinx_design"]
templates_path = ["_templates"]
exclude_patterns = ["build", "_build", "Thumbs.db", ".DS_Store"]
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_js_files = ["overlay.js"]
html_context = {
    "banner": "This is a pre-release version of the documentation."
}

def setup(app):
    from _ext.pygments_elcl import ErbslandConfigurationLanguage

    app.add_lexer("erbsland-conf", ErbslandConfigurationLanguage)
