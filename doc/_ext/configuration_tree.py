#  Copyright (c) 2024. Erbsland DEV. https://erbsland.dev
#  SPDX-License-Identifier: Apache-2.0
import html
import re
from pathlib import Path
from typing import Tuple

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective, logger

from .pygments_elcl import ErbslandConfigurationLanguage, DocumentError, Value


class ConfigurationTreeDirective(SphinxDirective):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    has_content = False
    option_spec = {"highlight-path": directives.unchanged, "hide-content": directives.flag}

    lexer = ErbslandConfigurationLanguage()

    RE_SPLIT_TYPE = re.compile(r"^(\w+)\((.*)\)$")

    @staticmethod
    def _split_highlight_path(path_str: str) -> list[str]:
        token_pattern = re.compile(r'"[^"]*"|\[[^\]]+\]|[^.\[\]]+')
        return [""] + token_pattern.findall(path_str)

    @staticmethod
    def _join_highlight_path(path: list[str]) -> str:
        result = ""
        for index, token in enumerate(path[1:]):
            if token.startswith("["):
                result += token
            else:
                if index > 0:
                    result += "."
                result += token
        return result

    def run(self):
        path = self._resolve_path(self.arguments[0])

        highlight_path = None
        if highlight_path_str := str(self.options.get("highlight-path", "")).strip():
            highlight_path = self._split_highlight_path(highlight_path_str)
        is_hide_content = "hide-content" in self.options
        html_content = self.create_html_for_file(path, highlight_path=highlight_path, is_hide_content=is_hide_content)
        raw_html = nodes.raw("", html_content, format="html")
        return [raw_html]

    def create_html_for_file(self, path: Path, *, highlight_path: list[str], is_hide_content=False) -> str:
        if not path.is_file():
            logger.error(f"File not found: {path}")
            return ""
        try:
            text = path.read_text(encoding="utf-8")
            root = self.lexer.get_value_tree(text)
        except DocumentError as e:
            logger.error(f"Failed to parse file {path}: {e}")
            return ""
        highlight_class = " highlight-path" if highlight_path else ""
        result = '<div class="highlight-erbsland-conf notranslate">'
        result += f'<div class="highlight value-tree{highlight_class}"><pre>\n'
        if highlight_path:
            result += f'Path: <span class="path">{self._join_highlight_path(highlight_path)}</span>\n\n'
        html_content, _ = self.visualize_value_tree(
            root, highlight_path=highlight_path, is_hide_content=is_hide_content
        )
        result += html_content
        result += "</pre></div></div>"
        return result

    def visualize_value_tree(
        self,
        value: Value,
        *,
        indent: str = "",
        indent_level: int = 0,
        last: bool = True,
        highlight_path: list[str] = None,
        is_hide_content=False,
    ) -> Tuple[str, bool]:
        """
        Recursively generates an ASCII tree representation of the `Value` structure.

        :param value: The `Value` object to visualize.
        :param indent: The current indentation level.
        :param last: Whether this node is the last child of its parent.
        :param highlight_path: The path to highlight. Must start with empty string for the root node.
            `None` if this node isn't in a path anymore.
        :return: A string representing the ASCII tree, and if this node matched the path.
        """
        result = []

        # Determine the connector based on whether this is the last child
        current_highlight_name = highlight_path[0] if highlight_path else ""
        if current_highlight_name.startswith("["):
            current_highlight_name = current_highlight_name[1:-1]
        if value.parent and value.parent.is_list():
            if current_highlight_name and not current_highlight_name[0].isdigit():
                current_highlight_name = f"{len(value.parent.children)-1}"
                highlight_path = [current_highlight_name, *highlight_path]
        is_highlight = highlight_path and current_highlight_name == value.name

        is_path_continues_vertically = False
        connector_class = " path" if is_highlight else ""
        if value.is_root():
            connector = ""
        elif last:
            connector = "┗━━ " if is_highlight else "└── "
        elif is_highlight:
            connector = "┡━━ "
        elif highlight_path:
            connector = "┠── "
            is_path_continues_vertically = True
        else:
            connector = "├── "

        # Build the current node's line
        name = "● " if value.is_root() else ""
        name += html.escape(value.get_name_visualization())
        line_class = " highlight" if is_highlight else ""
        if value.is_section():
            line_class += " section"
        line = f'<span class="line{line_class}">'
        line += indent
        if is_path_continues_vertically:
            line += f'<span class="connector path">{connector[0]}</span>'
            line += f'<span class="connector">{connector[1:]}</span>'
        else:
            line += f'<span class="connector{connector_class}">{connector}</span>'
        if value.is_root():
            line += f'<span class="connector{connector_class}">{name[:2]}</span><span class="name">{name[2:]}</span>'
        else:
            line += f'<span class="name">{name}</span>'
        if not is_hide_content:
            spaces = len(indent) + 28
            line += f'<span class="indent">'
            line += " " * (spaces - len(indent + connector + name))
            line += "</span>"
            line += f'<span class="arrow"><==</span> '
            line += f'<span class="content">'
            if match := self.RE_SPLIT_TYPE.match(str(value)):
                line += f'<span class="content_type">{match.group(1)}</span>'
                line += f'<span class="content_bracket"> ( </span>'
                line += f'<span class="content_text">{match.group(2)}</span>'
                line += f'<span class="content_bracket"> ) </span>'
            else:
                line += str(value)
            line += "</span>"
        line += "</span>"
        result.append(line)
        if is_highlight:
            path_tail = highlight_path[1:]
        else:
            path_tail = []
        children = value.children_sorted_for_display()
        child_indent = indent
        if value.is_root():
            pass
        elif last:
            child_indent += "    "
        elif is_path_continues_vertically:
            child_indent += '<span class="connector path">┃   </span>'
        else:
            child_indent += '<span class="connector">│   </span>'
        for i, child_value in enumerate(children):
            is_last_child = i == len(children) - 1
            content, child_is_highlight = self.visualize_value_tree(
                child_value,
                indent=child_indent,
                indent_level=indent_level + 1,
                last=is_last_child,
                highlight_path=path_tail,
                is_hide_content=is_hide_content,
            )
            if child_is_highlight:
                path_tail = None
            result.append(content)

        return "\n".join(result), is_highlight

    def _resolve_path(self, filename: str) -> Path:
        """
        Resolve the given filename to an absolute path. This supports:
        - Absolute paths.
        - Paths relative to the source directory (where conf.py is located).
        """
        env = self.state.document.settings.env
        # If the filename starts with '/', assume it's relative to the documentation root
        if filename.startswith("/"):
            path = Path(env.srcdir) / filename[1:]  # Skip leading '/'
        else:
            # Otherwise, treat it as relative to the current document's directory
            source_dir = Path(env.docname).parent
            path = Path(env.srcdir) / source_dir / filename
        return path


def test_visualize_value_tree():
    # Local test
    class TestStateMachine:
        def __init__(self):
            self.reporter = None

    re_remove_tags = re.compile(r"<.*?>")

    directive = ConfigurationTreeDirective("", [], {}, "", 0, 0, "", None, TestStateMachine())
    path = Path(__file__).parent.parent / "documents" / "reference" / "name-paths.elcl"
    html = directive.create_html_for_file(path, highlight_path=["", "server", "connection", "port"])
    html = re_remove_tags.sub("", html)
    print(html)


if __name__ == "__main__":
    test_visualize_value_tree()
