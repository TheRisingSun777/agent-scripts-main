#!/usr/bin/env python3
import argparse
import datetime as dt
import os
import re
import subprocess
from pathlib import Path
from typing import Iterable, List, Set

DENY_EXTS = {".db", ".sqlite", ".pdf", ".png", ".jpg", ".jpeg", ".zip", ".xlsx"}
DENY_BASENAMES = {".env"}
DENY_DIRS = {"exports", "excel"}


def run_git(repo: Path, args: List[str]) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(repo), *args], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def detect_task_id(task_id: str | None, branch: str) -> str:
    if task_id:
        return task_id
    match = re.search(r"TASK-\d+", branch)
    return match.group(0) if match else "TASK-000"


def sanitize_slug(slug: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", slug).strip("-")
    return cleaned or "pack"


def ensure_plain_prompt(prompt: str) -> str:
    stripped = prompt.lstrip()
    if not stripped:
        raise SystemExit("Prompt is empty. Provide plain task instructions.")
    lowered = stripped.lower()
    if lowered.startswith("[system]") or lowered.startswith("[user]") or lowered.startswith("[assistant]"):
        raise SystemExit("Prompt must not start with role headers like [SYSTEM]/[USER].")
    if lowered.startswith("system:") or lowered.startswith("user:") or lowered.startswith("assistant:"):
        raise SystemExit("Prompt must not start with role headers like SYSTEM:/USER:.")
    if lowered.startswith("you are oracle"):
        raise SystemExit("Prompt must not start with 'You are Oracle'.")
    return stripped


def is_denied(path: Path, repo: Path) -> bool:
    rel = path.relative_to(repo)
    if rel.name in DENY_BASENAMES or rel.name.startswith(".env"):
        return True
    if rel.suffix.lower() in DENY_EXTS:
        return True
    if any(part in DENY_DIRS for part in rel.parts):
        return True
    return False


def is_binary(path: Path) -> bool:
    try:
        with path.open("rb") as f:
            chunk = f.read(2048)
        return b"\x00" in chunk
    except OSError:
        return True


def expand_paths(repo: Path, inputs: List[str]) -> List[Path]:
    candidates: Set[Path] = set()
    for raw in inputs:
        if any(ch in raw for ch in "*?["):
            for match in repo.glob(raw):
                if match.is_file():
                    candidates.add(match.resolve())
            continue
        path = (repo / raw).resolve() if not os.path.isabs(raw) else Path(raw).resolve()
        if path.is_dir():
            for p in path.rglob("*"):
                if p.is_file():
                    candidates.add(p.resolve())
        elif path.is_file():
            candidates.add(path.resolve())
    return sorted(candidates)


def build_pack(args: argparse.Namespace) -> str:
    repo = Path(args.repo).resolve()
    now = dt.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H%M%S")

    branch = run_git(repo, ["rev-parse", "--abbrev-ref", "HEAD"]) or "(unknown)"
    head = run_git(repo, ["rev-parse", "HEAD"]) or "(unknown)"
    status_raw = run_git(repo, ["status", "--porcelain"])
    status = "clean" if not status_raw else "dirty"

    commits_raw = run_git(
        repo,
        ["log", "-n", "7", "--date=iso", "--pretty=format:%h|%ad|%s"],
    )
    commits = commits_raw.splitlines() if commits_raw else []

    task_id = detect_task_id(args.task_id, branch)
    slug = sanitize_slug(args.slug)

    out_dir = (
        Path(args.out_dir).resolve()
        if args.out_dir
        else Path("/Users/adil/Docs/Oracle") / repo.name / date_str
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{time_str}_{task_id}_{slug}.md"

    prompt_text = ""
    if args.prompt_file:
        prompt_text = Path(args.prompt_file).read_text(encoding="utf-8")
    elif args.prompt:
        prompt_text = args.prompt

    prompt_text = ensure_plain_prompt(prompt_text)

    files = expand_paths(repo, args.file)
    included: List[Path] = []
    for path in files:
        if is_denied(path, repo):
            continue
        if is_binary(path):
            continue
        included.append(path)

    lines: List[str] = []
    lines.append("# Oracle Pack (Offline)")
    lines.append("")
    lines.append(f"Generated: {now.isoformat(timespec='seconds')}")
    lines.append(f"Repo: {repo}")
    lines.append(f"Branch: {branch}")
    lines.append(f"HEAD: {head}")
    lines.append("")
    lines.append("## Git status")
    lines.append(f"Status: {status}")
    lines.append("")
    if status_raw:
        lines.append("```")
        lines.append(status_raw)
        lines.append("```")
        lines.append("")

    lines.append("## Recent commits (7)")
    if commits:
        for entry in commits:
            parts = entry.split("|", 2)
            if len(parts) == 3:
                lines.append(f"- {parts[0]} | {parts[1]} | {parts[2]}")
    else:
        lines.append("- (no commits found)")
    lines.append("")

    lines.append("## Prompt")
    lines.append(prompt_text.rstrip())
    lines.append("")

    lines.append("## Included files")
    if included:
        for path in included:
            rel = path.relative_to(repo)
            lines.append(f"- {rel}")
    else:
        lines.append("- (none)")
    lines.append("")

    for path in included:
        rel = path.relative_to(repo)
        lines.append(f"## File: {rel}")
        lines.append("```")
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            content = "(unreadable)"
        lines.append(content.rstrip())
        lines.append("```")
        lines.append("")

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return str(out_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline oracle pack generator (no network).")
    parser.add_argument("--repo", default=".", help="Target repo path.")
    parser.add_argument("--slug", required=True, help="Short slug for output filename.")
    parser.add_argument("--task-id", default=None, help="TASK-### override; falls back to branch or TASK-000.")
    parser.add_argument("--prompt", default=None, help="Prompt text to include.")
    parser.add_argument("--prompt-file", default=None, help="File containing prompt text.")
    parser.add_argument("--file", action="append", default=[], help="File/dir/glob to include; repeatable.")
    parser.add_argument("--out-dir", default=None, help="Override output directory.")
    args = parser.parse_args()

    if not args.file:
        raise SystemExit("At least one --file is required to build a pack.")

    out_path = build_pack(args)
    print(out_path)


if __name__ == "__main__":
    main()
