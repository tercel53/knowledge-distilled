#!/usr/bin/env python3
"""Validate structural consistency for one distilled article directory."""

from __future__ import annotations

import argparse
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


def normalize(parts: list[str]) -> str:
    return " ".join("".join(parts).split())


class ArticleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.local_refs: list[tuple[str, str]] = []
        self.hash_refs: list[str] = []
        self.nav_depth = 0
        self.nav_link: dict[str, object] | None = None
        self.nav_links: list[tuple[str, str]] = []
        self.section_stack: list[tuple[str, str | None]] = []
        self.capture: dict[str, object] | None = None
        self.eyebrows: dict[str, str] = {}
        self.headings: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        classes = set((values.get("class") or "").split())
        element_id = values.get("id")
        if element_id:
            self.ids.append(element_id)

        if tag in {"a", "link", "script", "img", "source"}:
            attribute = "href" if tag in {"a", "link"} else "src"
            reference = values.get(attribute)
            if reference:
                self.local_refs.append((attribute, reference))
                if tag == "a" and reference.startswith("#"):
                    self.hash_refs.append(reference[1:])

        if tag == "nav" and ("contents" in classes or values.get("aria-label") == "文章目录"):
            self.nav_depth += 1
        elif self.nav_depth and tag == "nav":
            self.nav_depth += 1

        if self.nav_depth and tag == "a" and (values.get("href") or "").startswith("#"):
            self.nav_link = {"target": values["href"][1:], "text": []}

        if tag in {"section", "article", "header"}:
            self.section_stack.append((tag, element_id))

        section_id = next((item for _, item in reversed(self.section_stack) if item), None)
        if section_id and self.capture is None:
            if classes & {"eyebrow", "thesis-label", "chapter-kicker"}:
                self.capture = {"kind": "eyebrow", "id": section_id, "tag": tag, "text": []}
            elif tag in {"h1", "h2", "h3"} and section_id not in self.headings:
                self.capture = {"kind": "heading", "id": section_id, "tag": tag, "text": []}

    def handle_endtag(self, tag: str) -> None:
        if self.nav_link is not None and tag == "a":
            self.nav_links.append((str(self.nav_link["target"]), normalize(self.nav_link["text"])))
            self.nav_link = None

        if self.capture is not None and tag == self.capture["tag"]:
            target = self.eyebrows if self.capture["kind"] == "eyebrow" else self.headings
            target[str(self.capture["id"])] = normalize(self.capture["text"])
            self.capture = None

        if self.section_stack and tag == self.section_stack[-1][0]:
            self.section_stack.pop()
        if tag == "nav" and self.nav_depth:
            self.nav_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.nav_link is not None:
            self.nav_link["text"].append(data)
        if self.capture is not None:
            self.capture["text"].append(data)


def main() -> int:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("article_dir", type=Path)
    argument_parser.add_argument(
        "--allow-label-differences",
        action="store_true",
        help="Allow deliberately different navigation and eyebrow labels after manual review.",
    )
    args = argument_parser.parse_args()
    article_dir = args.article_dir.resolve()
    html_path = article_dir / "index.html"
    metadata_path = article_dir / "metadata.json"
    errors: list[str] = []

    if not html_path.is_file():
        errors.append(f"missing {html_path}")
    if not metadata_path.is_file():
        errors.append(f"missing {metadata_path}")
    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors), file=sys.stderr)
        return 1

    parser = ArticleParser()
    parser.feed(html_path.read_text(encoding="utf-8"))
    ids = set(parser.ids)
    duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    if duplicates:
        errors.append(f"duplicate HTML ids: {', '.join(duplicates)}")

    for target in parser.hash_refs:
        if target not in ids:
            errors.append(f"hash target #{target} does not exist")

    for target, label in parser.nav_links:
        if target not in ids:
            errors.append(f"navigation target #{target} does not exist")
            continue
        eyebrow = parser.eyebrows.get(target)
        if eyebrow is None:
            errors.append(f"section #{target} has no eyebrow label")
        elif label != eyebrow and not args.allow_label_differences:
            errors.append(f"navigation/eyebrow mismatch for #{target}: {label!r} != {eyebrow!r}")

    for attribute, reference in parser.local_refs:
        parsed = urlsplit(reference)
        if parsed.scheme or parsed.netloc or reference.startswith(("#", "mailto:", "data:")):
            continue
        target_path = (article_dir / parsed.path).resolve()
        if not target_path.exists():
            errors.append(f"missing local {attribute} target: {reference}")

    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid metadata.json: {exc}")
        metadata = {}

    for entry in metadata.get("outline", []):
        section_id = entry.get("id")
        title = entry.get("title")
        if section_id not in ids:
            errors.append(f"metadata outline id #{section_id} does not exist")
        elif parser.headings.get(section_id) != title:
            errors.append(
                f"metadata/heading mismatch for #{section_id}: {title!r} != {parser.headings.get(section_id)!r}"
            )

    for entry in metadata.get("visuals", []):
        visual_id = entry.get("id")
        if visual_id and visual_id not in ids:
            errors.append(f"metadata visual id #{visual_id} does not exist")

    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors), file=sys.stderr)
        return 1

    print(
        f"OK: {article_dir} — {len(ids)} ids, {len(parser.nav_links)} navigation labels, "
        f"{len(metadata.get('outline', []))} outline entries"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
