# Agent Scripts (Control Plane)

This repository is a portable toolbox for agent workflows:
- shared guardrails (`AGENTS.MD`)
- reusable skills (`skills/*/SKILL.md`)
- small, dependency-light helper scripts (`scripts/*`, `bin/*`)

It is designed to be copied or referenced by other repositories without pulling in project-specific code.

## Quick start

### Recommended location
Default location:
- `$HOME/Docs/Oracle/agent-scripts-main`

Optional environment variable (used by pointer-style repos):
- `ORCH_HOME=$HOME/Docs/Oracle/agent-scripts-main`

### “Pointer-style” AGENTS in downstream repos
Downstream repositories should keep their own local `AGENTS.MD`, but **start it with a pointer** to this control plane
so shared rules don’t get duplicated.

Recommended pointer line:
- `Control plane: ${ORCH_HOME:-$HOME/Docs/Oracle/agent-scripts-main}`

Then include only repo-local rules beneath that pointer.

## Sync expectations

- Treat this repo as the canonical source for shared guardrails + skills.
- Keep scripts portable:
  - avoid repo-specific imports
  - avoid hardcoded absolute paths where possible
  - prefer small self-contained utilities over complex frameworks
- When updating a shared helper script, update it here first, then propagate to any downstream copies as needed.

## Contents

### Guardrails
- `AGENTS.MD` — shared operating rules for agents and tooling.

### Skills
- `skills/*/SKILL.md` — skill definitions discovered/used by agent runtimes.
- Skills should be project-agnostic unless explicitly marked as project-specific.

### Committer Helper (`scripts/committer`)
- Bash helper that stages exactly the files you list, enforces non-empty commit messages, and creates the commit.

### Docs Lister (`scripts/docs-list.ts`)
- tsx script that walks `docs/`, enforces front-matter (`summary`, `read_when`), and prints summaries.
- Optional compiled binary:
  - `bun build scripts/docs-list.ts --compile --outfile bin/docs-list`

### Browser Tools (`bin/browser-tools`)
- Standalone Chrome helper for DevTools-enabled inspection/screenshot/search workflows.
- Prefer the compiled binary if available: `bin/browser-tools --help`
- If rebuilding is needed:
  - `bun build scripts/browser-tools.ts --compile --target bun --outfile bin/browser-tools`
- Note: keep binaries out of git unless you intentionally version them.

## Security
- Do not commit secrets, tokens, cookies, or local machine dumps.
- If a tool generates session files/logs, ensure they are gitignored unless explicitly required.
