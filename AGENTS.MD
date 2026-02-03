# AGENTS.md — Orchestrator (agent-scripts-main)

This repo is the control plane: shared protocol + tools + skills used across multiple downstream repos.
Goal: maximize throughput while preserving safety (capital, data integrity, and reversibility).

AGENTS_VERSION: 2026-01-27

---

## 0) Read-check handshake (non-negotiable)

At the start of EVERY task response, include:

Read check: AGENTS_VERSION=2026-01-27

If you cannot find this file, say so explicitly and proceed using the downstream repo’s AGENTS.md.

---

## 1) Anti-Slop Behavioral Contract (applies to Codex + Claude)

These rules exist to prevent the most expensive LLM failure modes: wrong assumptions, overbuilt abstractions, and non-surgical diffs.

### 1.1 Think before coding (no silent assumptions)
- State your assumptions explicitly.
- If multiple interpretations exist, present them. Do not pick silently.
- If something is unclear or contradictory, STOP and ask. Do not “guess and ship”.

### 1.2 Simplicity first (minimum code that solves the task)
- No speculative flexibility/configurability.
- No abstractions for single-use code.
- If you wrote 200 lines and it could be 50, rewrite it.

### 1.3 Surgical changes only (touch what you must)
- Do not refactor, reformat, or “improve” adjacent code/comments unrelated to the task.
- Match existing style and patterns.
- Only remove unused code you created. If you find unrelated dead code, mention it — don’t delete it unless asked.

### 1.4 Goal-driven execution (success criteria + verification)
Convert requests into verifiable goals.
Default pattern:
1) Add/adjust tests or invariants (or a validation script) to encode the requirement.
2) Implement the smallest change that makes tests pass.
3) Run repo gates and report results with commands + key outputs.

Never claim “done” without green gates (or explicitly documented exceptions).

---

## 2) Non-negotiables (global safety)

- Atomic commits only. One commit = one intent.
- Commit message format: `scope: action (why)`
  - Example: `oracle: add denylist for secrets (prevent leaks)`
- Proof required: commands run + key outputs.
- No secrets in commits or Oracle packs: `.env`, tokens, credentials, cookies.
- No destructive git ops unless explicitly approved (no history rewrite, no mass deletes).
- No hardcoded absolute paths in committed scripts. Prefer env vars + safe defaults.
- If the task touches .xlsx/.xlsm/CSV, you MUST use excel-safe-ops skill.

---

## 3) One-Take Autonomy Protocol (default for Codex/Opus)

Target: finish 80–90% in one pass without drifting scope.

1) Preflight: `git status`, branch, current head.
2) Micro-plan: 3–7 bullets with acceptance criteria + stop conditions.
   - Include “Assumptions / Unknowns” explicitly.
3) Execute in atomic chunks.
4) Validate with repo gates.
5) Oracle pack (changed-files-only) + handoff summary.

Stop if:
- gates fail,
- you discover ambiguity that changes business logic meaning,
- you are about to touch more files than the scope boundary.

---

## 4) Repo model (multi-repo)

- Downstream repos keep their own repo-local `AGENTS.md` (local contract):
  - entrypoints, gates, safety boundaries, oracle pack wrapper
- This repo provides:
  - shared rules + skills docs (`skills/*/SKILL.md`)
  - reference tooling (committer, oracle patterns)

Downstream repos should add a pointer near the top:
- `Control plane: ${ORCH_HOME:-$HOME/Docs/Oracle/agent-scripts-main}`

---

## 5) Oracle packs (policy)

Oracle packs are context bundles, not an LLM.
Default pack type: changed-files-only using a git range (`HEAD~1..HEAD`).

Pack must include:
- metadata (repo, branch, head, commands run)
- diff summary + full diff
- contents of changed files
- high-signal allowlist files (AGENTS, key entrypoints, schema, key docs)
- strict denylist (no secrets, no binaries)

Preferred implementation: vendored per repo wrapper script (repo-specific allowlist).
Centralized option allowed, but must not hardcode paths.

---

## 6) Stop conditions (ask human)

Ask before:
- changing skill folder interfaces used by downstream repos
- adding paid API usage
- adding automation that writes into downstream repos automatically
- any tool that risks including secrets in packs

Also ask if:
- requirements are ambiguous and affect money/accounting/capital decisions
- more than one plausible “correct” interpretation exists

---

## 7) Templates

### Implementation task template
- Goal (1 sentence):
- Scope boundary (allowed files):
- Assumptions / Unknowns:
- Commands to verify:
- Done means (checklist):
- Stop conditions:
- Rollback plan:

### Review request template
- Oracle pack path:
- What changed + why:
- Commands run + outputs:
- Risks/edge cases: