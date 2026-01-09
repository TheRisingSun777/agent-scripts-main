# Skill: excel-safe-ops

## Description
Use this skill whenever a task involves reading, writing, generating, or editing Excel workbooks
(.xlsx / .xlsm) or CSVs used as inputs/outputs for automation.
Goal: prevent broken workbooks, corrupted XML, accidental type coercion, and schema drift.

This skill is tool-agnostic and works across projects. It assumes Excel files may be used by humans
in Microsoft Excel and by scripts (Python/Node) and must remain compatible with both.

## Triggers
Use this skill when the task includes any of:
- .xlsx / .xlsm / “Excel workbook” / “spreadsheet”
- openpyxl / pandas / xlwings / xlsxwriter
- “update columns”, “append rows”, “export to Excel”, “sync to Excel”, “import from Excel”
- “Google Drive spreadsheet sync” where the source is an .xlsx

## Non-negotiables (contract rules)
1) Always make a timestamped backup before writing.
2) Never rename sheets that are referenced by automation (unless explicitly part of the task).
3) Never rename/reorder required columns. Add new columns only at the end unless the contract says otherwise.
4) Do not introduce merged cells, grouped columns, or exotic formatting into machine-read sheets.
5) IDs stay TEXT (never numeric): order IDs, SKU IDs, keys, barcodes.
6) Dates stay real dates (not text); store and export consistently.
7) Write operations must be atomic: write to temp → rename/replace.
8) Validate after write: workbook opens in Excel without “repair” prompts AND parsers can re-read it.

## Workflow
### A) When a human edits the workbook
- Use Microsoft Excel (avoid Numbers / Google Sheets roundtrips unless the workflow is explicitly designed for it).
- Keep sheet names stable.
- Do not reorder columns; do not delete headers.
- Keep IDs as text:
  - Pre-format the column as Text, OR
  - Prefix values with a single quote (') if Excel insists on coercing.
- Close Excel before running scripts (Excel can lock files and leave temp "~$" files).

### B) When code reads the workbook
- Read-only passes should not mutate the file.
- Normalize headers:
  - Trim whitespace
  - Normalize repeated spaces
  - Compare using a canonical header map (don’t “best guess” silently).
- Parse types intentionally:
  - IDs: str
  - Money: Decimal or int (define rounding)
  - Dates: datetime/date, with explicit timezone handling if relevant

### C) When code writes to the workbook (safe write pattern)
1) Backup: copy the original to `backups/<name>.<timestamp>.xlsx`
2) Load workbook in a mode that preserves formulas/styles when possible
3) Modify ONLY the intended ranges
4) Save to a temp path
5) Replace the original atomically
6) Validate:
   - Re-open with the same library and verify required sheets/headers exist
   - (Best) Open in Excel and confirm no repair dialog

### D) Generation vs modification (choose the safest option)
- If you must preserve formatting, tables, formulas: MODIFY a known-good template.
- If you only need a data export: Generate a NEW workbook (but ensure consumers expect a new file).

## Common failure modes + preventions
- Excel “repairs” file on open:
  - Avoid rewriting structure; prefer template-based edits
  - Avoid creating/deleting sheets unless required
- IDs become scientific notation:
  - Force text columns; write strings, not numbers
- Dates shift by timezone:
  - Store as date (not datetime) when time-of-day is irrelevant
  - When datetime is required, document timezone explicitly
- Schema drift:
  - Hard-validate required columns before and after writing
  - Never silently auto-create “close enough” columns

## Definition of Done
- Workbook opens in Excel without repair warnings
- Required sheets exist with exact expected names
- Required columns exist with exact expected headers
- A re-read by the parser confirms row/column counts and key fields match expectations
- Backup exists and is referenced in logs/output notes
