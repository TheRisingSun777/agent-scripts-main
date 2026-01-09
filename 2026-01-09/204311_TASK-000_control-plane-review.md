# Oracle Pack (Offline)

Generated: 2026-01-09T20:43:11
Repo: /Users/adil/Docs/Oracle/agent-scripts-main
Branch: (unknown)
HEAD: (unknown)

## Git status
Status: clean

## Recent commits (7)
- (no commits found)

## Prompt
Review control plane repo context and summarize key governance/skills/oracle tooling structure.

## Included files
- AGENTS.MD
- CHANGELOG.md
- README.md
- scripts/oracle_pack_local.py
- scripts/sync_skills_to_homes.sh
- skills/frontend-design/SKILL.md
- skills/oracle/SKILL.md
- tools.md

## File: AGENTS.MD
```
# AGENTS.md — Orchestrator (agent-scripts-main)

This repo is the **control plane**: shared protocol + tools + skills used across multiple downstream repos.
If you’re working here, you’re improving the toolkit — **not** fixing business logic in downstream projects.

Goal: maximize throughput while keeping safety: atomic commits, reversible diffs, proof-of-fix, no secrets.

---

## Non‑negotiables
- **Atomic commits only.** One commit = one intent.
- **Commit message format:** `scope: action (why)`
  - Example: `oracle: add denylist for secrets (prevent leaks)`
- **Proof required**: commands run + key outputs.
- **No secrets** in commits or Oracle packs: `.env`, tokens, credentials, cookies.
- **No destructive git ops** unless explicitly approved (no history rewrite, no mass deletes).
- **No hardcoded absolute paths** in committed scripts. Prefer env vars + safe defaults.

---

## One‑Take Autonomy Protocol (default for Codex/Opus)
Agents should finish 80–90% in one pass:
1) **Preflight**: `git status`, branch, current head.
2) **Micro‑plan**: 3–7 bullets, acceptance criteria + stop conditions.
3) **Execute** in atomic chunks.
4) **Validate** with the repo’s gates.
5) **Oracle pack** (changed-files-only) + handoff summary.

---

## Repo model (multi‑repo)
- Downstream repos keep their own repo‑local `AGENTS.md` (local contract):
  - entrypoints, gates, safety boundaries, oracle pack wrapper
- This repo provides:
  - shared rules + skills docs (`skills/*/SKILL.md`)
  - reference tooling (committer, oracle patterns)

Downstream repos should add a pointer near the top:
- `Control plane: ${ORCH_HOME:-$HOME/Docs/Oracle/agent-scripts-main}`

---

## Oracle packs (policy)
Oracle packs are **context bundles**, not an LLM.
Default pack type: changed-files-only using a git range (`HEAD~1..HEAD`).

Pack must include:
- metadata (repo, branch, head, commands run)
- diff summary + full diff
- contents of changed files
- high-signal allowlist files (AGENTS, key entrypoints, schema, key docs)
- strict denylist (no secrets, no binaries)

Preferred implementation: **vendored per repo** wrapper script (repo-specific allowlist).
Centralized option is allowed, but must not hardcode paths.

---

## Stop conditions (ask human)
Ask before:
- changing skill folder interfaces used by downstream repos
- adding paid API usage
- adding automation that writes into downstream repos automatically
- any tool that risks including secrets in packs

---

## Templates

### Implementation task template
- Goal (1 sentence):
- Scope boundary (allowed files):
- Commands to verify:
- Done means (checklist):
- Stop conditions:
- Rollback plan:

### Review request template
- Oracle pack path:
- What changed + why:
- Commands run + outputs:
- Risks/edge cases:
```

## File: CHANGELOG.md
```
---
summary: Timeline of guardrail helper changes mirrored from Sweetistics and related repos.
---

# Changelog

## 2025-12-22 — Remove Custom rm Shim
- Dropped `bin/rm` and `scripts/trash.ts`; rely on the system `trash` command for recoverable deletes.

## 2025-12-17 — Remove Runner; Keep Guardrails
- Removed the `runner` wrapper and `scripts/runner.ts` now that modern Codex sessions handle long-running/background work directly.
- Kept the safety-critical bits as standalone shims: `bin/rm` (moves deletes to Trash via `scripts/trash.ts`).
- Dropped the `find -delete` interception and the `bin/sleep` shim.

## 2025-12-02 — Release Preflight Helpers
- Added shared release helpers in `release/sparkle_lib.sh`: clean working-tree check, Sparkle key probe, changelog finalization/notes extraction, and appcast monotonicity guard for version/build.
- Documented the helper functions in `docs/RELEASING-MAC.md` so Trimmy/CodexBar-style release scripts can reuse them.

## 2025-11-18 — Console Log Capture
- Added `console` command to `scripts/browser-tools.ts` for capturing and monitoring Chrome DevTools console output with real-time formatting, type filtering (log, error, warn, etc.), continuous follow mode, and configurable timeouts with automatic object serialization.

## 2025-11-22 — Search & Content Extraction
- Added `search` and `content` commands to `scripts/browser-tools.ts` for Google SERP scraping with optional readable markdown extraction and single-URL readability output, leveraging the existing DevTools-connected Chrome instance.
- `eval` now supports `--pretty-print` to inspect complex objects with indentation and colors.

## 2025-11-15 — Chrome Browser Tools
- Added `scripts/browser-tools.ts`, a DevTools-ready Chrome helper copied from the Oracle repo so agents can inspect, screenshot, and terminate sessions without dragging in the full CLI. The workflow is inspired by Mario Zechner’s [“What if you don’t need MCP?”](https://mariozechner.at/posts/2025-11-02-what-if-you-dont-need-mcp/).
- Documented the new helper in the README so downstream repos know how to run `pnpm tsx scripts/browser-tools.ts --help`.

## 2025-11-16 — Browser Tools Pipe Detection
- Updated `scripts/browser-tools.ts` to enumerate and kill Chrome instances started with `--remote-debugging-pipe` (the default for Peekaboo/Tachikoma) in addition to the classic `--remote-debugging-port`. List/kill now show “debugging pipe” when no port exists and still fetch tab metadata when it does.
- README now notes the optional `NODE_PATH=$(npm root -g)` trick so the helper can run from bare copies of the repo without a local `package.json`.

## 2025-11-14 — Compact Runner Summaries
- The runner's completion log now defaults to a compact `exit <code> in <time>` format so long commands don't repeat the entire input line.
- Added the `RUNNER_SUMMARY_STYLE` env var with `compact` (default), `minimal`, and `verbose` options so agents can pick how much detail they want without editing the script.
- Timeout heuristics now understand both `pnpm` and `bun` invocations automatically, so long-running Bun scripts/tests get the same guardrails without repo-specific patches.
- `sleep` invocations longer than 30 seconds are clamped to the 30s ceiling instead of erroring, which keeps wait hacks working while still honoring the AGENTS.MD limit.

## 2025-11-08 — Sleep Guardrail & Git Shim Refresh
- Runner now rejects any `sleep` argument longer than 30 seconds, mirroring the AGENTS rule and preventing long blocking waits.
- Added `bin/sleep` so plain `sleep` calls automatically route through the runner and inherit the enforcement without extra flags.
- Simplified `bin/git` to delegate directly to the runner + system git, eliminating the bespoke policy checker while keeping consent gates identical.

## 2025-11-08 — Guardrail Sync & Docs Hardening
- Synced guardrail helpers with Sweetistics so downstream repos share the same runner, docs-list helper, and supporting scripts.
- Expanded README guidance around runner usage, portability, and multi-repo sync expectations.
- Added committer lock cleanup, tightened path ignores, and refreshed misc. helper utilities (e.g., `toArray`) to reduce drift across repos.

## 2025-11-08 — Initial Toolkit Import
- Established the repo with the Sweetistics guardrail toolkit (runner, git policy enforcement, docs-list helper, etc.).
- Ported documentation from the main product repo so other projects inherit the identical safety rails and onboarding notes.
```

## File: README.md
```
# Agent Scripts

This folder collects the Sweetistics guardrail helpers so they are easy to reuse in other repos or share during onboarding. Everything here is copied verbatim from `/Users/steipete/Projects/sweetistics` on 2025-11-08 unless otherwise noted.

## Syncing With Other Repos
- Treat this repo as the canonical mirror for the shared guardrail helpers. Whenever you edit `scripts/committer` or `scripts/docs-list.ts` in any repo, copy the change here and then back out to every other repo that carries the same helpers so they stay byte-identical.
- When someone says “sync agent scripts,” pull the latest changes here, ensure downstream repos have the pointer-style `AGENTS.MD`, copy any helper updates into place, and reconcile differences before moving on.
- Keep every file dependency-free and portable: the scripts must run in isolation across repos. Do not add `tsconfig` path aliases, shared source folders, or any other Sweetistics-specific imports—inline tiny helpers or duplicate the minimum code needed so the mirror stays self-contained.

## Pointer-Style AGENTS
- Shared guardrail text now lives only inside this repo: `AGENTS.MD` (shared rules + tool list).
- Every consuming repo’s `AGENTS.MD` is reduced to the pointer line `READ ~/Projects/agent-scripts/AGENTS.MD BEFORE ANYTHING (skip if missing).` Place repo-specific rules **after** that line if they’re truly needed.
- Do **not** copy the `[shared]` or `<tools>` blocks into other repos anymore. Instead, keep this repo updated and have downstream workspaces re-read `AGENTS.MD` when starting work.
- When updating the shared instructions, edit `agent-scripts/AGENTS.MD`, mirror the change into `~/AGENTS.MD` (Codex global), and let downstream repos continue referencing the pointer.

## Committer Helper (`scripts/committer`)
- **What it is:** Bash helper that stages exactly the files you list, enforces non-empty commit messages, and creates the commit.

## Docs Lister (`scripts/docs-list.ts`)
- **What it is:** tsx script that walks `docs/`, enforces front-matter (`summary`, `read_when`), and prints the summaries surfaced by `pnpm run docs:list`. Other repos can wire the same command into their onboarding flow.
- **Binary build:** `bin/docs-list` is the compiled Bun CLI; regenerate it after editing `scripts/docs-list.ts` via `bun build scripts/docs-list.ts --compile --outfile bin/docs-list`.

## Browser Tools (`bin/browser-tools`)
- **What it is:** A standalone Chrome helper inspired by Mario Zechner’s [“What if you don’t need MCP?”](https://mariozechner.at/posts/2025-11-02-what-if-you-dont-need-mcp/) article. It launches/inspects DevTools-enabled Chrome profiles, pastes prompts, captures screenshots, and kills stray helper processes without needing the full Oracle CLI.
- **Usage:** Prefer the compiled binary: `bin/browser-tools --help`. Common commands include `start --profile`, `nav <url>`, `eval '<js>'`, `screenshot`, `search --content "<query>"`, `content <url>`, `inspect`, and `kill --all --force`.
- **Rebuilding:** The binary is not tracked in git. Re-generate it with `bun build scripts/browser-tools.ts --compile --target bun --outfile bin/browser-tools` (requires Bun) and leave transient `node_modules`/`package.json` out of the repo.
- **Portability:** The tool has zero repo-specific imports. Copy the script or the binary into other automation projects as needed and keep this copy in sync with downstream forks. It detects Chrome sessions launched via `--remote-debugging-port` **and** `--remote-debugging-pipe`, so list/kill works for both styles.

## Sync Expectations
- This repository is the canonical mirror for the guardrail helpers used in mcporter and other Sweetistics projects. Whenever you edit `scripts/committer`, `scripts/docs-list.ts`, or related guardrail files in another repo, copy the changes back here immediately (and vice versa) so the code stays byte-identical.
- When someone asks to “sync agent scripts,” update this repo, compare it against the active project, and reconcile differences in both directions before continuing.

## @steipete Agent Instructions (pointer workflow)
- The only full copies of the guardrails are `agent-scripts/AGENTS.MD` and `~/AGENTS.MD`. Downstream repos should contain the pointer line plus any repo-local additions.
- During a sync sweep: pull latest `agent-scripts`, ensure each target repo’s `AGENTS.MD` contains the pointer line at the top, append any repo-local notes beneath it, and update the helper scripts as needed.
- If a repo needs custom instructions, clearly separate them from the pointer so future sweeps don’t overwrite local content.
- For submodules (Peekaboo/*), repeat the pointer check inside each subrepo, push those changes, then bump submodule SHAs in the parent repo.
- Skip experimental repos (e.g., `poltergeist-pitui`) unless explicitly requested.
```

## File: scripts/oracle_pack_local.py
```
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
```

## File: scripts/sync_skills_to_homes.sh
```
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_SKILLS="$ROOT_DIR/skills"

DESTS=("$HOME/.codex/skills" "$HOME/.claude/skills")

for dest in "${DESTS[@]}"; do
  mkdir -p "$dest"
  rsync -a --exclude '.system' --exclude '.system/**' "$SRC_SKILLS/" "$dest/"
done
```

## File: skills/frontend-design/SKILL.md
```
---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, or applications. Generates creative, polished code that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.
```

## File: skills/oracle/SKILL.md
```
---
name: oracle
description: Use the @steipete/oracle CLI to bundle a prompt plus the right files and get a second-model review (API or browser) for debugging, refactors, design checks, or cross-validation.
---

# Oracle (CLI) — best use

Oracle bundles your prompt + selected files into one “one-shot” request so another model can answer with real repo context (API or browser automation). Treat outputs as advisory: verify against the codebase + tests.

## Modes

### Pack mode (offline)

Triggered when the user says **exactly**: "create an oracle pack".

Rules:
- Use the local offline pack generator script (no network, no browser automation).
- If the repo provides `scripts/oracle_pack.sh`, use it as the only entrypoint; otherwise use `scripts/oracle_pack_local.py`.
- **Forbidden:** `npx`, `oracle --engine browser`, or any network access.
- Output is a local markdown bundle only (no API calls).
- Prompt must be plain task instructions only (no role headers like `[SYSTEM]` / `[USER]`).

### Run mode (browser)

Triggered when the user says: "run oracle" or "call a friend".

Rules:
- Use `scripts/oracle_run.sh --confirm` as the only entrypoint (no direct `npx`).
- Uses browser automation with GPT‑5.2 Pro.
- **Requires explicit confirmation** because it uses network + browser automation.
- Prompt must be plain task instructions only (no role headers like `[SYSTEM]` / `[USER]`).

## Main use case (browser, GPT‑5.2 Pro)

Default workflow here: `--engine browser` with GPT‑5.2 Pro in ChatGPT. This is the “human in the loop” path: it can take ~10 minutes to ~1 hour; expect a stored session you can reattach to.

Recommended defaults:
- Engine: browser (`--engine browser`)
- Model: GPT‑5.2 Pro (either `--model gpt-5.2-pro` or a ChatGPT picker label like `--model "5.2 Pro"`)
- Attachments: directories/globs + excludes; avoid secrets.

## Golden path (fast + reliable)

1. Pick a tight file set (fewest files that still contain the truth).
2. Preview what you’re about to send (`--dry-run` + `--files-report` when needed).
3. Run in browser mode for the usual GPT‑5.2 Pro ChatGPT workflow; use API only when you explicitly want it.
4. If the run detaches/timeouts: reattach to the stored session (don’t re-run).

## Commands (preferred)

- Show help (once/session):
  - `npx -y @steipete/oracle --help`

- Preview (no tokens):
  - `npx -y @steipete/oracle --dry-run summary -p "<task>" --file "src/**" --file "!**/*.test.*"`
  - `npx -y @steipete/oracle --dry-run full -p "<task>" --file "src/**"`

- Token/cost sanity:
  - `npx -y @steipete/oracle --dry-run summary --files-report -p "<task>" --file "src/**"`

- Browser run (main path; long-running is normal):
  - `npx -y @steipete/oracle --engine browser --model gpt-5.2-pro -p "<task>" --file "src/**"`

- Manual paste fallback (assemble bundle, copy to clipboard):
  - `npx -y @steipete/oracle --render --copy -p "<task>" --file "src/**"`
  - Note: `--copy` is a hidden alias for `--copy-markdown`.

## Attaching files (`--file`)

`--file` accepts files, directories, and globs. You can pass it multiple times; entries can be comma-separated.

- Include:
  - `--file "src/**"` (directory glob)
  - `--file src/index.ts` (literal file)
  - `--file docs --file README.md` (literal directory + file)

- Exclude (prefix with `!`):
  - `--file "src/**" --file "!src/**/*.test.ts" --file "!**/*.snap"`

- Defaults (important behavior from the implementation):
  - Default-ignored dirs: `node_modules`, `dist`, `coverage`, `.git`, `.turbo`, `.next`, `build`, `tmp` (skipped unless you explicitly pass them as literal dirs/files).
  - Honors `.gitignore` when expanding globs.
  - Does not follow symlinks (glob expansion uses `followSymbolicLinks: false`).
  - Dotfiles are filtered unless you explicitly opt in with a pattern that includes a dot-segment (e.g. `--file ".github/**"`).
  - Hard cap: files > 1 MB are rejected (split files or narrow the match).

## Budget + observability

- Target: keep total input under ~196k tokens.
- Use `--files-report` (and/or `--dry-run json`) to spot the token hogs before spending.
- If you need hidden/advanced knobs: `npx -y @steipete/oracle --help --verbose`.

## Engines (API vs browser)

- Auto-pick: uses `api` when `OPENAI_API_KEY` is set, otherwise `browser`.
- Browser engine supports GPT + Gemini only; use `--engine api` for Claude/Grok/Codex or multi-model runs.
- **API runs require explicit user consent** before starting because they incur usage costs.
- Browser attachments:
  - `--browser-attachments auto|never|always` (auto pastes inline up to ~60k chars then uploads).
- Remote browser host (signed-in machine runs automation):
  - Host: `oracle serve --host 0.0.0.0 --port 9473 --token <secret>`
  - Client: `oracle --engine browser --remote-host <host:port> --remote-token <secret> -p "<task>" --file "src/**"`

## Sessions + slugs (don’t lose work)

- Stored under `~/.oracle/sessions` (override with `ORACLE_HOME_DIR`).
- Runs may detach or take a long time (browser + GPT‑5.2 Pro often does). If the CLI times out: don’t re-run; reattach.
  - List: `oracle status --hours 72`
  - Attach: `oracle session <id> --render`
- Use `--slug "<3-5 words>"` to keep session IDs readable.
- Duplicate prompt guard exists; use `--force` only when you truly want a fresh run.

## Prompt template (high signal)

Oracle starts with **zero** project knowledge. Assume the model cannot infer your stack, build tooling, conventions, or “obvious” paths. Include:
- Project briefing (stack + build/test commands + platform constraints).
- “Where things live” (key directories, entrypoints, config files, dependency boundaries).
- Exact question + what you tried + the error text (verbatim).
- Constraints (“don’t change X”, “must keep public API”, “perf budget”, etc).
- Desired output (“return patch plan + tests”, “list risky assumptions”, “give 3 options with tradeoffs”).

### “Exhaustive prompt” pattern (for later restoration)

When you know this will be a long investigation, write a prompt that can stand alone later:
- Top: 6–30 sentence project briefing + current goal.
- Middle: concrete repro steps + exact errors + what you already tried.
- Bottom: attach *all* context files needed so a fresh model can fully understand (entrypoints, configs, key modules, docs).

If you need to reproduce the same context later, re-run with the same prompt + `--file …` set (Oracle runs are one-shot; the model doesn’t remember prior runs).

## Safety

- Don’t attach secrets by default (`.env`, key files, auth tokens). Redact aggressively; share only what’s required.
- Prefer “just enough context”: fewer files + better prompt beats whole-repo dumps.
```

## File: tools.md
```
# Tools Reference

CLI tools available on Peter's machines. Use these for agentic tasks.

## bird 🐦
Twitter/X CLI for posting, replying, reading tweets.

**Location**: `~/Projects/bird/bird`

**Commands**:
```bash
bird tweet "<text>"                    # Post a tweet
bird reply <tweet-id-or-url> "<text>"  # Reply to a tweet
bird read <tweet-id-or-url>            # Fetch tweet content
bird replies <tweet-id-or-url>         # List replies to a tweet
bird thread <tweet-id-or-url>          # Show full conversation thread
bird search "<query>" [-n count]       # Search tweets
bird mentions [-n count]               # Find tweets mentioning @clawdbot
bird whoami                            # Show logged-in account
bird check                             # Show credential sources
```

**Auth**: Uses Firefox cookies by default. Pass `--firefox-profile <name>` to switch.

---

## sonoscli 🔊
Control Sonos speakers over local network (UPnP/SOAP).

**Location**: `~/Projects/sonoscli/bin/sonos`

**Commands**:
```bash
sonos discover                         # Find speakers on network
sonos status --name "Room"             # Current playback status
sonos play/pause/stop --name "Room"    # Playback control
sonos next/prev --name "Room"          # Track navigation
sonos volume get/set --name "Room" 25  # Volume control
sonos mute get/toggle --name "Room"    # Mute control

# Grouping
sonos group status                     # Show current groups
sonos group join --name "A" --to "B"   # Join A into B's group
sonos group unjoin --name "Room"       # Make standalone
sonos group party --to "Room"          # Join all to one group

# Spotify (via SMAPI)
sonos smapi search --service "Spotify" --category tracks "query"
sonos open --name "Room" spotify:track:<id>
```

**Known issues**:
- SSDP multicast may fail; use `--ip <speaker-ip>` as fallback
- Default HTTP keep-alives can cause timeouts (fix pending: DisableKeepAlives)

---

## peekaboo 👀
Screenshot, screen inspection, and click automation.

**Location**: `~/Projects/Peekaboo`

**Commands**:
```bash
peekaboo capture                       # Take screenshot
peekaboo see                           # Describe what's on screen (OCR)
peekaboo click                         # Click at coordinates
peekaboo list                          # List windows/apps
peekaboo tools                         # Show available tools
peekaboo permissions status            # Check TCC permissions
```

**Requirements**: Screen Recording + Accessibility permissions.

**Docs**: `~/Projects/Peekaboo/docs/commands/`

---

## sweetistics 📊
Twitter/X analytics desktop app (Tauri).

**Location**: `~/Projects/sweetistics`

Use for deeper Twitter data analysis beyond what `bird` provides.

---

## clawdis 📡
WhatsApp/Telegram messaging gateway and agent interface.

**Location**: `~/Projects/clawdis`

**Commands**:
```bash
clawdis login                          # Link WhatsApp via QR
clawdis send --to <number> --message "text"  # Send message
clawdis agent --message "text"         # Talk to agent directly
clawdis gateway                        # Run WebSocket gateway
clawdis status                         # Session health
```

---

## oracle 🧿
Hand prompts + files to other AIs (GPT-5 Pro, etc.).

**Usage**: `npx -y @steipete/oracle --help` (run once per session to learn syntax)

---

## gh
GitHub CLI for PRs, issues, CI, releases.

**Usage**: `gh help`

When someone shares a GitHub URL, use `gh` to read it:
```bash
gh issue view <url> --comments
gh pr view <url> --comments --files
gh run list / gh run view <id>
```

---

## mcporter
MCP server launcher for browser automation, web scraping.

**Usage**: `npx mcporter --help`

Common servers: `iterm`, `firecrawl`, `XcodeBuildMCP`
```
