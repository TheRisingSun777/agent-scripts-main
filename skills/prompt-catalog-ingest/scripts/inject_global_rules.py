#!/usr/bin/env python3
"""Inject global catalog rules block into each prompt file.

Usage:
  python3 inject_global_rules.py --catalog <unorganized.md> --prompt-dir <prompt_book_dir> [--dry-run]

- Detects a single global rules block before the first prompt section.
- Prepends it to each prompt file (after the #ID line) if not already present.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


PROMPT_START_RE = re.compile(r"^##\s+\d+\.\s+|^###\s+HERO-", re.M)
RULE_MARKERS = [
    "## Visual Style Reference",
    "### Environment Specifications",
    "ENVIRONMENT:",
    "CAMERA:",
    "TYPOGRAPHY",
    "Background Specifications",
    "## Shot Type Rules",
    "## Prefix Convention",
    "## Distribution Check",
    "## Wardrobe Distribution",
]


def extract_global_rules(text: str) -> str:
    m = PROMPT_START_RE.search(text)
    if not m:
        return ""
    preamble = text[: m.start()].strip()
    if not preamble:
        return ""
    indices = [preamble.find(marker) for marker in RULE_MARKERS if marker in preamble]
    if not indices:
        return ""
    start = min(indices)
    block = preamble[start:].strip()
    return block


def has_global_block(prompt_text: str) -> bool:
    lowered = prompt_text.lower()
    return any(marker.lower() in lowered for marker in RULE_MARKERS)


def inject_block(prompt_text: str, block: str) -> str:
    lines = prompt_text.splitlines()
    if not lines:
        return prompt_text
    header = lines[0].rstrip()
    body = "\n".join(lines[1:]).lstrip("\n")
    return f"{header}\n\n{block}\n\n{body}".rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True, help="Path to unorganized catalog .md")
    parser.add_argument("--prompt-dir", required=True, help="Prompt_book catalog directory (contains *.md prompts)")
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing")
    args = parser.parse_args()

    catalog_path = Path(args.catalog)
    prompt_dir = Path(args.prompt_dir)

    if not catalog_path.exists():
        raise SystemExit(f"Catalog not found: {catalog_path}")
    if not prompt_dir.exists():
        raise SystemExit(f"Prompt dir not found: {prompt_dir}")

    text = catalog_path.read_text(errors="replace")
    block = extract_global_rules(text)
    if not block:
        print("No global rules block detected.")
        return 0

    changed = 0
    skipped = 0
    for p in sorted(prompt_dir.glob("*.md")):
        prompt_text = p.read_text(errors="replace")
        if has_global_block(prompt_text):
            skipped += 1
            continue
        new_text = inject_block(prompt_text, block)
        if not args.dry_run:
            p.write_text(new_text)
        changed += 1

    print(f"Global rules block detected ({len(block.splitlines())} lines).")
    print(f"Updated: {changed}, skipped (already had block): {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
