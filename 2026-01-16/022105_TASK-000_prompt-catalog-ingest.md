# Oracle Pack (Offline)

Generated: 2026-01-16T02:21:05
Repo: /Users/adil/Docs/Oracle/agent-scripts-main
Branch: main
HEAD: 9d24e928ec2d3142e98d78c259744ab274529434

## Git status
Status: dirty

```
?? skills/image-gen/
?? skills/mpsales-competitor-automation/
```

## Recent commits (7)
- 9d24e92 | 2026-01-16 02:17:51 +0500 | skills: add prompt-catalog-ingest (catalog ingest)
- b086c4c | 2026-01-09 21:46:33 +0500 | Publish control-plane agent scripts

## Prompt
Add prompt-catalog-ingest skill for catalog ingestion.

## Included files
- skills/prompt-catalog-ingest/SKILL.md

## File: skills/prompt-catalog-ingest/SKILL.md
```
---
name: prompt-catalog-ingest
description: Organize/ingest unorganized prompt catalogs into Prompt_book organized and distilled catalogs (split by prompt ID). Use when asked to populate, ingest, or update prompt catalogs from unorganized sources, create distilled variants, or sync new versioned catalogs across models/wardrobes/clothes.
---

# Prompt Catalog Ingest

Use this skill when converting unorganized catalog files into structured Prompt_book catalogs (organized + distilled) without changing prompt wording.

## Workflow (Sequential)

1) **Locate unorganized inputs**
   - Find unorganized catalogs in `docs/Prompt_catalogs_unorganized/<model>/<date>/`.
   - Identify the version(s) to ingest (e.g., `catalog_v2.7.md`, `catalog_v5.7.md`).

2) **Define the mapping**
   - Build a mapping of section titles → prompt IDs (e.g., `"Size Guide" -> "LS01"`).
   - Use existing organized catalogs or model notes as the source of truth for IDs and wardrobe prefixes.
   - Keep the mapping explicit; do not infer IDs when unsure.

3) **Parse sections (preserve text)**
   - Support common formats:
     - `## 1. Title` sections (often with fenced prompt blocks)
     - `1. Title` headings (plain text blocks)
   - Extract the prompt body **exactly as written**, excluding only outer wrappers like code fences.
   - Do **not** rewrite wording, fix typos, translate, or reformat content unless explicitly asked.

4) **Apply allowed normalizations (only if requested)**
   - Remove `1500×1500` mentions when instructed.
   - Add a Style Reference block at top:
     - `## Style Reference`
     - `Use attached image as reference for typography, colors, icons, and overall visual style.`
   - Insert the photography line **before** the Output section:
     - `### Photography Direction - Camera: ARRI Alexa 35 + ZEISS Ultra Prime 50mm, T5.6`
   - Remove navy/navi mentions only when explicitly requested (e.g., v5.7 tasks).

5) **Write organized catalogs**
   - Output path: `Prompt_book/<model>/catalog_<version>/<ID>.md`
   - File format:
     - First line: `# <ID>`
     - Blank line
     - Prompt body (with any requested normalizations applied)

6) **Write distilled catalogs**
   - Output path: `Prompt_book/<model>/distilled/catalog_<version>/<ID>.md`
   - Distill rule: **remove Background sections** (e.g., `### Background` / `### BACKGROUND` blocks) and their content until the next `###` heading.
   - Preserve all other content exactly.

7) **Validate**
   - Count prompt files vs expected mapping entries.
   - Ensure every prompt file starts with `# <ID>`.
   - Ensure no unintended edits (spot check a few prompts).
   - If replacing existing catalogs, confirm with user before deleting old versions.

## Implementation Notes

- Prefer a model-specific ingest script if one exists under `scripts/` (copy and adjust mappings).
- If no script exists, create a minimal ingest script in the repo:
  - Read unorganized files
  - Parse sections
  - Apply allowed normalizations
  - Write organized + distilled outputs
- Keep paths configurable via env vars; avoid hardcoded absolute paths.

## Safety Rules (Non‑Negotiable)

- Do not change prompt wording unless explicitly requested.
- Do not delete images or unrelated prompt catalogs without confirmation.
- If unsure about mappings, ask for clarification instead of guessing.
```
