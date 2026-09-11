#!/usr/bin/env python3
"""Query and validate the article-distillation contextual terminology registry."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
import sys


SKILL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_DIR.parents[2]
REGISTRY_PATH = SKILL_DIR / "references" / "terminology.json"


def load_registry() -> dict:
    with REGISTRY_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def normalize(value: object) -> str:
    return str(value).casefold().strip()


def render_term(term: dict, usages: list[dict] | None = None) -> str:
    selected = usages if usages is not None else term["usages"]
    lines = [
        f"[{term['id']}] {' / '.join(term['source_terms'])}",
        f"推荐表达：{term['preferred_zh']}",
        f"概念：{term['definition']}",
        f"范围：{term['scope']}",
    ]
    if term.get("avoid"):
        lines.append("在所列语境中避免：" + "；".join(f"{item['term']}（范围：{item['scope']}；{item['reason']}）" for item in term["avoid"]))
    for usage in selected:
        lines.extend(
            [
                "",
                f"- {usage['article_title']}",
                f"  路径：{usage['article_path']}",
                f"  本地上下文：{usage['article_path']}index.html#{usage['local_anchor']}",
                f"  来源：{usage['source_url']}",
                f"  原文位置：{usage['source_location']}",
                f"  语境含义：{usage['context_meaning']}",
                f"  实际表达：{usage['chosen_zh']}",
                f"  选择理由：{usage['rationale']}",
                f"  核对：原文={usage['review']['source']}；措辞={usage['review']['wording']}",
                f"  核对说明：{usage['review']['note']}",
            ]
        )
    return "\n".join(lines)


def search_term(registry: dict, query: str) -> int:
    needle = normalize(query)
    matches = []
    for term in registry["terms"]:
        haystack = [term["id"], term["preferred_zh"], term["definition"], *term["source_terms"]]
        haystack.extend(usage["chosen_zh"] for usage in term["usages"])
        haystack.extend(item["term"] for item in term.get("avoid", []))
        if any(needle in normalize(value) for value in haystack):
            matches.append(term)
    if not matches:
        print(f"No terminology match for: {query}", file=sys.stderr)
        return 1
    print("\n\n".join(render_term(term) for term in matches))
    return 0


def search_article(registry: dict, query: str) -> int:
    needle = normalize(query)
    matches: list[tuple[dict, list[dict]]] = []
    for term in registry["terms"]:
        usages = [
            usage
            for usage in term["usages"]
            if any(needle in normalize(usage[field]) for field in ("article_title", "article_path", "source_url"))
        ]
        if usages:
            matches.append((term, usages))
    if not matches:
        print(f"No article match for: {query}", file=sys.stderr)
        return 1
    print("\n\n".join(render_term(term, usages) for term, usages in matches))
    return 0


def validate(registry: dict) -> int:
    errors: list[str] = []
    required_term = {"id", "source_terms", "preferred_zh", "definition", "scope", "avoid", "usages"}
    required_usage = {
        "article_title",
        "article_path",
        "source_url",
        "source_location",
        "context_meaning",
        "chosen_zh",
        "rationale",
        "local_anchor",
        "review",
    }
    seen_ids: set[str] = set()
    usage_count = 0
    if registry.get("schema_version") != 2:
        errors.append("unsupported schema_version; expected 2")
    for index, term in enumerate(registry.get("terms", [])):
        missing = required_term - term.keys()
        if missing:
            errors.append(f"terms[{index}] missing: {', '.join(sorted(missing))}")
            continue
        term_id = term["id"]
        if term_id in seen_ids:
            errors.append(f"duplicate term id: {term_id}")
        seen_ids.add(term_id)
        for item in term["avoid"]:
            if not all(isinstance(item.get(key), str) and item[key].strip() for key in ("term", "reason", "scope")):
                errors.append(f"{term_id}: avoid entry needs term, reason and scope")
        if not term["source_terms"] or not term["usages"]:
            errors.append(f"{term_id}: source_terms and usages must not be empty")
        for usage_index, usage in enumerate(term["usages"]):
            usage_count += 1
            missing_usage = required_usage - usage.keys()
            if missing_usage:
                errors.append(f"{term_id}.usages[{usage_index}] missing: {', '.join(sorted(missing_usage))}")
                continue
            article_dir = REPO_ROOT / usage["article_path"]
            for key in required_usage - {"review"}:
                if not isinstance(usage[key], str) or not usage[key].strip():
                    errors.append(f"{term_id}: invalid or empty {key}")
            review = usage["review"]
            if not isinstance(review, dict) or review.get("source") not in {"verified", "pending"} or review.get("wording") not in {"user_confirmed", "reviewed", "pending"} or not review.get("note"):
                errors.append(f"{term_id}: invalid review state or missing note")
            if not article_dir.is_dir():
                errors.append(f"{term_id}: article path does not exist: {usage['article_path']}")
            page = article_dir / "index.html"
            if page.is_file():
                anchors = re.findall(r'''\bid=["']([^"']+)["']''', page.read_text(encoding="utf-8"))
                if usage["local_anchor"] not in anchors:
                    errors.append(f"{term_id}: missing local anchor {usage['local_anchor']}")
            else:
                errors.append(f"{term_id}: missing article index.html")
            if not usage["source_location"].strip() or not usage["context_meaning"].strip():
                errors.append(f"{term_id}: usage lacks contextual location or meaning")
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"Validated {len(seen_ids)} concepts and {usage_count} contextual article usages")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    term_parser = subparsers.add_parser("term", help="find a concept and all of its article contexts")
    term_parser.add_argument("query")
    article_parser = subparsers.add_parser("article", help="find every concept recorded for an article")
    article_parser.add_argument("query")
    subparsers.add_parser("validate", help="validate registry structure and article paths")
    args = parser.parse_args()
    registry = load_registry()
    if args.command == "term":
        return search_term(registry, args.query)
    if args.command == "article":
        return search_article(registry, args.query)
    return validate(registry)


if __name__ == "__main__":
    raise SystemExit(main())
