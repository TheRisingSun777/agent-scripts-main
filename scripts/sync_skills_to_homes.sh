#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_SKILLS="$ROOT_DIR/skills"

DESTS=("$HOME/.codex/skills" "$HOME/.claude/skills")

for dest in "${DESTS[@]}"; do
  mkdir -p "$dest"
  rsync -a --exclude '.system' --exclude '.system/**' "$SRC_SKILLS/" "$dest/"
done
