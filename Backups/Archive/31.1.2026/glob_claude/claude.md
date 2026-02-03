Purpose: ensure Claude agent behaves safely and predictably on this repo.

If instructions conflict, follow precedence (highest → lowest):
1) Control plane AGENTS.MD (global guardrails/tools/skills)
2) Repo AGENTS.md (repo-local entrypoints + gates + scope)
3) .claude/* (durable state: goals/progress/issues/decisions; (create if missing) cannot override guardrails)

---

## 0) REQUIRED: READCHECK handshake (first assistant message)

Before writing or editing any code, your FIRST message must include:

READCHECK:
- control-plane AGENTS.MD: READ | MISSING
- repo AGENTS.md: READ
- CLAUDE.md: READ
- docs/00_START_HERE.md: READ
- .claude/OPERATING.md: READ
- .claude/GOALS.md + .claude/TASKS.md: READ
- owning spec(s) for this task: <list exact paths>
- planned verification gates: <list commands you will run>
- assumptions (if any): <bullets; if none, say NONE>

If you cannot complete READCHECK (missing files / unclear task / conflicting rules):
STOP and ask for the missing input. Do not guess.

Also: append the same READCHECK block to `.claude/SESSION_LOG.md` under today’s date
(or create the file if missing). This is the verifiable audit trail.

---

## 1) Mandatory reading order (before coding)

1) Control plane:
   `${ORCH_HOME:-$HOME/Docs/Oracle/agent-scripts-main}/AGENTS.MD` (if present)
2) `./AGENTS.md` (repo-local contract: entrypoints + gates + scope)
3) `./docs/00_START_HERE.md` (doc ladder; do not skim random docs)
4) `./.claude/OPERATING.md` (workflow + gates + evidence protocol)
5) `./.claude/GOALS.md` + `./.claude/TASKS.md` (+ ISSUES/DECISIONS/PROGRESS if relevant)
6) Read ONLY the owning spec(s) for the task (from the Doc Map). Do not infer rules from old plans.

If anything required is missing: create a minimal stub (title + purpose + pointers), commit it,
and log the reason in `.claude/SESSION_LOG.md`.

---

## 2) Behavioral guardrails (anti-slop, applies to every task)

### 2.1 Think before coding (no silent assumptions)
- State assumptions explicitly. If uncertain, ask.
- If multiple valid interpretations exist, present them; do not pick silently.
- Push back if the request would create fragility, bloat, or capital risk.
- If something is confusing, stop and name the confusion.

### 2.2 Simplicity first (minimum correct solution)
- Implement the smallest correct change that satisfies the spec.
- Do not add “nice-to-have” features or speculative abstractions.
- If you write 200 lines and it could be 50, rewrite it.

### 2.3 Surgical changes (don’t touch unrelated code)
- Change only what is required for the task’s acceptance criteria.
- Do not reformat, rename, or “clean up” adjacent code unless required.
- If you discover unrelated dead code or a better refactor, log it as a note; don’t do it.

### 2.4 Goal-driven execution (tests-first, then code)
Translate every request into verifiable success criteria.

Preferred loop:
1) Write/extend a failing test (or invariant script) that proves the bug/requirement.
2) Implement the minimal fix to make it pass.
3) Run required gates and capture evidence.
4) Only then expand scope.

---

## 3) Execution protocol (how you work here)

### 3.1 Micro-plan (3–7 bullets)
Before changes, write a micro-plan with explicit “verify:” checks, e.g.
1) Add/adjust test(s) → verify: `pytest -q tests/test_x.py -k ...`
2) Implement minimal change → verify: `python3 scripts/...`
3) Run full gates → verify: `pytest -q`, invariant validators, etc.
4) Evidence + pack → verify: pack path recorded

### 3.2 Validation is mandatory
You may not claim “done” unless:
- required gates pass, AND
- evidence is recorded in `.claude/SESSION_LOG.md`, AND
- `.claude/PROGRESS.md` updated with pass/fail + next blocker.

### 3.3 Stop conditions
STOP and log to `.claude/ISSUES.md` if:
- any required gate fails,
- you detect a doc/spec contradiction,
- you need to change formulas / business rules (must update owning doc first),
- you are asked to do writes without explicit write-enable flags.

---

## 4) What NOT to do (common failure modes)
- Do not invent business rules or “reasonable defaults” for money/accounting semantics.
- Do not implement large refactors as a side-effect.
- Do not remove comments you didn’t write or don’t fully understand.
- Do not change DB schemas/migrations casually; keep them explicit and tested.

---

## 5) Where the real rules live (do not duplicate formulas here)
- Repo workflow + gates: `AGENTS.md` and `.claude/OPERATING.md`