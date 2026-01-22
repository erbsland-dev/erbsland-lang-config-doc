#  Copyright (c) 2026. Erbsland DEV. https://erbsland.dev
#  SPDX-License-Identifier: Apache-2.0

"""
Utility to join reStructuredText documents following TOC order.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def strip_initial_comment(lines: list[str]) -> list[str]:
    if not lines:
        return lines
    index = 0
    while index < len(lines) and not lines[index].strip():
        index += 1
    if index >= len(lines):
        return []
    first = lines[index].lstrip()
    if not first.startswith(".."):  # no initial comment
        return lines
    start = index
    index += 1
    while index < len(lines):
        if lines[index].startswith((" ", "\t")):
            index += 1
            continue
        break
    while index < len(lines) and not lines[index].strip():
        index += 1
    return lines[:start] + lines[index:]


def parse_toctree_entries(lines: list[str]) -> list[str]:
    entries: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.lstrip().startswith(".. toctree::"):
            base_indent = len(line) - len(line.lstrip())
            index += 1
            while index < len(lines):
                item = lines[index]
                if not item.strip():
                    index += 1
                    continue
                item_indent = len(item) - len(item.lstrip())
                if item_indent <= base_indent:
                    break
                stripped = item.strip()
                if stripped.startswith(":"):
                    index += 1
                    continue
                entries.append(stripped)
                index += 1
            continue
        index += 1
    return entries


def expand_includes(lines: list[str], source_path: Path) -> list[str]:
    expanded: list[str] = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith(".. include::"):
            indent = line[: len(line) - len(stripped)]
            include_target = stripped.split("::", 1)[1].strip()
            include_path = (source_path.parent / include_target).resolve()
            include_lines = include_path.read_text(encoding="utf-8").splitlines()
            if indent:
                include_lines = [indent + item if item else item for item in include_lines]
            expanded.extend(include_lines)
            continue
        expanded.append(line)
    return expanded


def collect_documents(entry_path: Path, root_dir: Path, seen: set[Path], ordered: list[Path]) -> None:
    path = entry_path.resolve()
    if path in seen:
        return
    seen.add(path)
    ordered.append(path)
    lines = path.read_text(encoding="utf-8").splitlines()
    for entry in parse_toctree_entries(lines):
        if entry.startswith(("http://", "https://")):
            continue
        target = path.parent / entry
        if target.suffix == "":
            target = target.with_suffix(".rst")
        if target.is_dir():
            target = target / "index.rst"
        target = target.resolve()
        if root_dir not in target.parents and target != root_dir:
            continue
        if not target.exists():
            raise FileNotFoundError(f"TOC entry not found: {target}")
        collect_documents(target, root_dir, seen, ordered)


def render_document(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    lines = strip_initial_comment(lines)
    lines = expand_includes(lines, path)
    return lines


def join_documents(source_dir: Path, entry_file: Path, output_file: Path) -> None:
    root_dir = source_dir.resolve()
    entry_path = (root_dir / entry_file).resolve()
    seen: set[Path] = set()
    ordered: list[Path] = []
    collect_documents(entry_path, root_dir, seen, ordered)

    output_lines: list[str] = []
    for document in ordered:
        relative_path = document.relative_to(root_dir)
        output_lines.append(f".. Source: {relative_path.as_posix()}")
        output_lines.append("")
        output_lines.extend(render_document(document))
        output_lines.append("")

    output_path = output_file.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(output_lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", "-s", default="doc", help="Source documentation directory")
    parser.add_argument("--entry", "-e", default="index.rst", help="Entry document within source")
    parser.add_argument("--output", "-o", required=True, help="Output .rst file")
    args = parser.parse_args()

    source_dir = Path(args.source)
    entry_file = Path(args.entry)
    output_file = Path(args.output)

    join_documents(source_dir, entry_file, output_file)


if __name__ == "__main__":
    main()
