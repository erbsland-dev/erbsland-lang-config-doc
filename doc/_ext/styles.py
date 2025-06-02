#  Copyright (c) 2024. Erbsland DEV. https://erbsland.dev
#  SPDX-License-Identifier: Apache-2.0
import unicodedata

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective

from .configuration_tree import ConfigurationTreeDirective

SPECIAL_CHARS = {
    "\n": r"\n",
    "\t": r"\t",
    "\r": r"\r",
    "\f": r"\f",
    "<": r"&lt;",
    ">": r"&gt;",
}
CONTROL_NAMES = {
    "\0": ["NULL"],
    "\x07": ["BELL"],
    "\x08": ["BACKSPACE"],
    "\x09": ["CHARACTER TABULATION", "horizontal tabulation (HT)", "tab"],
    "\x0A": ["LINE FEED (LF)", "new line (NL)", "end of line (EOL)"],
    "\x0B": ["LINE TABULATION", "vertical tabulation (VT)"],
    "\x0C": ["FORM FEED (FF)"],
    "\x0D": ["CARRIAGE RETURN (CR)"],
    "\x1B": ["ESCAPE"],
    "\x7F": ["DELETE"],
}


def js_escape(text) -> str:
    return text.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')


def html_for_char(char) -> str:
    if len(char) != 1:
        raise ValueError("Character must be a single character")
    unicode_name = unicodedata.name(char, "")
    if char in CONTROL_NAMES:
        unicode_name = ", ".join(CONTROL_NAMES[char])
    unicode_category = unicodedata.category(char)
    utf8_bytes = " ".join(f"{b:02X}" for b in char.encode("utf-8"))
    code_point = ord(char)
    if char in SPECIAL_CHARS:
        char = SPECIAL_CHARS[char]
    overlay_data = [js_escape(char), js_escape(unicode_name), unicode_category, f"U+{code_point:>04X}", utf8_bytes]
    js_data = ",".join(f"'{data}'" for data in overlay_data)
    html = f'<code class="literal" onclick="showOverlay({js_data})">' f'<span class="cp-role">{char}</span>' f"</code>"
    return html


def convert_cp(text) -> str:
    """
    Convert the given text in a Unicode character.
    :param text:
    :return:
    """
    if len(text) > 1:
        return chr(int(text, 16))
    return text


def cp(name, rawtext, text, lineno, inliner, options=None, content=None):
    """
    Role to Unicode code points with extra information.
    """
    try:
        if len(text) >= 3 and "-" in text:
            html = " – ".join([html_for_char(convert_cp(cp)) for cp in text.split("-", 1)])
        elif len(text) >= 3 and "&" in text:
            parts = list([html_for_char(convert_cp(cp)) for cp in text.split("&", 1)])
            html = ", ".join(parts[:-1]) + " and " + parts[-1]
        elif len(text) >= 3 and "|" in text:
            parts = list([html_for_char(convert_cp(cp)) for cp in text.split("|", 1)])
            html = ", ".join(parts[:-1]) + " or " + parts[-1]
        else:
            html = html_for_char(convert_cp(text))
        result_nodes = [nodes.raw("", html, format="html")]
        return result_nodes, []
    except ValueError:
        # Handle invalid code points gracefully
        error = inliner.reporter.error(f"Invalid code point: {text}", line=lineno)
        return [inliner.problematic(rawtext, rawtext, error)], [error]


def text_code(name, rawtext, text, lineno, inliner, options=None, content=None):
    html = f'<span class="text-code">{text}</span>'
    result_nodes = [nodes.raw("", html, format="html")]
    return result_nodes, []


class SpecialAdmonitionDirective(SphinxDirective):
    """
    A special admonition directive that uses an additional class for styling.
    """

    has_content = True

    ADMONITION_CLASS = "example"
    ADMONITION_TITLE = "Example"

    def run(self):
        admonition_node = nodes.admonition()
        admonition_node["classes"].append(self.ADMONITION_CLASS)
        title_node = nodes.title(text=self.ADMONITION_TITLE)
        admonition_node += title_node
        self.state.nested_parse(self.content, self.content_offset, admonition_node)
        return [admonition_node]


class DesignRationaleDirective(SpecialAdmonitionDirective):
    """Directive to create a 'Design Rationale' admonition."""

    ADMONITION_CLASS = "design-rationale"
    ADMONITION_TITLE = "Design Rationale"


class MicroParserDirective(SpecialAdmonitionDirective):
    """Directive to create a 'Specification for Micro-Parsers' admonition."""

    ADMONITION_CLASS = "micro-parser-specs"
    ADMONITION_TITLE = "Micro-Parsers"


def setup(app: Sphinx):
    app.add_role("cp", cp)
    app.add_role("text-code", text_code)
    app.add_directive("design-rationale", DesignRationaleDirective)
    app.add_directive("micro-parser", MicroParserDirective)
    app.add_directive("configuration-tree", ConfigurationTreeDirective)

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
