#  Copyright (c) 2025. Erbsland DEV. https://erbsland.dev
#  SPDX-License-Identifier: Apache-2.0

"""
Utility to build Sphinx documentation, convert HTML to compact Markdown, and generate an index.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

import html2text

def build_html(source_dir: Path | str, build_dir: Path | str) -> None:
    """Build Sphinx documentation into HTML."""
    src = Path(source_dir)
    out = Path(build_dir)
    out.mkdir(parents=True, exist_ok=True)
    cmd = ["sphinx-build", str(src), str(out)]
    subprocess.run(cmd, check=True)

def convert_html_to_markdown(html_dir: Path | str, md_dir: Path | str) -> None:
    """Convert HTML files to compact Markdown using html2text."""
    converter = html2text.HTML2Text()
    # Simplify output by removing images and links, and avoid internal link markers
    converter.ignore_images = True
    converter.ignore_links = True
    converter.skip_internal_links = True
    converter.body_width = 0

    html_root = Path(html_dir)
    md_root = Path(md_dir)

    for html_path in html_root.rglob("*.html"):
        rel_path = html_path.relative_to(html_root)
        md_path = md_root / rel_path.with_suffix(".md")
        md_path.parent.mkdir(parents=True, exist_ok=True)
        html = html_path.read_text(encoding="utf-8")
        # strip the sidebar navigation (built-in TOC), page-level TOC block, and footer
        html = re.sub(r'<nav[^>]*wy-nav-side[^>]*>[\s\S]*?</nav>', '', html, flags=re.I)
        html = re.sub(r'<section id="table-of-contents">[\s\S]*?</section>', '', html, flags=re.I)
        html = re.sub(r'<div class="toctree-wrapper compound">[\s\S]*?</div>', '', html, flags=re.I)
        html = re.sub(r'<footer[\s\S]*?</footer>', '', html, flags=re.I)
        # remove everything before the main header to start document at the title
        html = re.sub(r'^[\s\S]*?(<h1[^>]*>)', r"\1", html, flags=re.I)
        md = converter.handle(html)
        # remove unwanted anchor icons from link markers
        md = md.replace('\uf0c1', '')
        # remove consecutive blank lines
        lines = [line.rstrip() for line in md.splitlines()]
        cleaned = []
        blank = False
        for line in lines:
            if not line:
                if not blank:
                    cleaned.append(line)
                blank = True
            else:
                cleaned.append(line)
                blank = False
        md_path.write_text("\n".join(cleaned), encoding="utf-8")

def generate_index(md_dir: Path | str, index_file: Path | str) -> None:
    """Generate a JSON index mapping document titles to Markdown paths."""
    index: list[dict[str, str]] = []
    md_root = Path(md_dir)
    for md_path in md_root.rglob("*.md"):
        rel_path = md_path.relative_to(md_root)
        title = md_path.name
        for line in md_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("#"):
                title = line.lstrip("# ").strip()
                break
        index.append({"title": title, "path": str(rel_path)})
    index_path = Path(index_file)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(index, indent=2), encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", "-s", default="doc", help="Sphinx source directory")
    parser.add_argument("--build-dir", "-b", default="build/html", help="HTML build directory")
    parser.add_argument("--md-dir", "-m", default="docs_md", help="Output Markdown directory")
    parser.add_argument("--index-file", "-i", default="docs_md/index.json", help="Output index file")
    parser.add_argument("--no-build", action="store_true", help="Skip building HTML documentation")
    args = parser.parse_args()

    source = Path(args.source)
    build_dir = Path(args.build_dir)
    md_dir = Path(args.md_dir)
    index_file = Path(args.index_file)

    if not args.no_build:
        print(f"Building HTML documentation: {source} -> {build_dir}")
        build_html(source, build_dir)
    print(f"Converting HTML to Markdown: {build_dir} -> {md_dir}")
    convert_html_to_markdown(build_dir, md_dir)
    print(f"Generating index file: {index_file}")
    generate_index(md_dir, index_file)
    print("Done.")

if __name__ == "__main__":
    main()
