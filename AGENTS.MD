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
- **If the task touches .xlsx/.xlsm/CSV, you MUST use excel-safe-ops skill.

---

## Skill triggers (additions)
- Use **combo-sync** when the user asks to sync/propagate combo changes across wardrobes or to resync combo registries/envs after a combo folder was updated.

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
