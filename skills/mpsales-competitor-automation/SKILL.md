---
name: mpsales-competitor-automation
description: Automate MPSales competitor exclusion checkbox workflow in the web UI using Playwright, including storage_state auth, login-modal handling, pagination, review pass, and optional upload to Kaspi. Use when asked to run or maintain the MPSales competitor selection automation in /Users/adil/Docs/Web_automation.
---

# MPSales Competitor Automation

## Read order (repo context)
1) `/Users/adil/Docs/Oracle/agent-scripts-main/AGENTS.MD`
2) `/Users/adil/Docs/Web_automation/AGENTS.md`
3) `/Users/adil/Docs/Web_automation/Docs/Mpsales_competitor_research_v2.md`
4) `/Users/adil/Docs/Web_automation/execution_plan.md`
5) `/Users/adil/Docs/Web_automation/.claude/OPERATING.md`

## Quick commands
- Generate storage state:
  - `web-auto auth --base-url https://mpsales.kz/price_strategy/ --token-env MPSALES_TOKEN_2 --profile-dir "/Users/<you>/Library/Application Support/Google/Chrome/Profile 7" --out data/storage_state.json --headed`
- Confirm run (headful):
  - `web-auto run mpsales-competitors --config config/tasks/mpsales_competitors.yaml --storage-state data/storage_state.json --account app_2 --store 30361967 --confirm --headed`
- Review + upload only when clean:
  - `web-auto run mpsales-competitors --config config/tasks/mpsales_competitors.yaml --storage-state data/storage_state.json --account app_2 --store 30361967 --confirm --upload-after --headed`
- Resume:
  - `web-auto run mpsales-competitors --config config/tasks/mpsales_competitors.yaml --resume --headed`
- API dry-run (app_1):
  - `web-auto run mpsales-competitors --config config/tasks/mpsales_competitors.yaml --account app_1 --api --dry-run`
- API confirm (app_1):
  - `web-auto run mpsales-competitors --config config/tasks/mpsales_competitors.yaml --account app_1 --api --confirm`
- API confirm + verify (app_1):
  - `web-auto run mpsales-competitors --config config/tasks/mpsales_competitors.yaml --account app_1 --api --api-verify --confirm`

## Safety
- Never commit `.env` or `data/storage_state.json`.
- Upload to Kaspi only after review finds 0 remaining targets (`--upload-after`).
- Headful is default for stability; headless is optional.

## Observability
- Run summary: `runs/mpsales_competitors/<run_id>/summary.json`
- Error log: `runs/mpsales_competitors/<run_id>/errors.jsonl`
- Screenshots/HTML artifacts in the same run folder
