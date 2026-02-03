---
name: kaspi-offer-creation
description: Create or update Kaspi batch offer XLSM/ZIP uploads (Kaspi catalog import), including packaging images, validating template values, and handling Kaspi result-file comments.
---

# Kaspi Offer Creation (Batch XLSM/ZIP)

Use this skill whenever the user asks to create, update, or troubleshoot Kaspi **batch offer uploads** (XLSM + images ZIP).

## Required prep (always)
1) **Read the blueprint** in the target repo:
   - `docs/kaspi_offer_creations_blueprint.md`
2) **Open the category template** before edits (context, required fields, values):
   - Default templates live in this skill under `templates/`
   - If the user provides a template path, read that instead.
3) **Use excel-safe-ops** for all XLSM edits (backup, no renames, atomic write).

## Quick workflow (minimal)
1) Validate required fields using `attributes` row 1.
2) Validate list-bound fields against `values` sheet.
3) Ensure `merchant_sku` uniqueness per row.
4) Normalize multi-value delimiters to `", "` (comma + space).
5) Package ZIP:
   - XLSM at root
   - `images/` lowercase at root
   - no `__MACOSX`, no extra folders
6) If Kaspi rejects:
   - open returned XLSM and read **cell comments** for error messages.

## Non-negotiables
- `merchant_sku` must be unique per row.
- Multi-value fields must use `", "` delimiter.
- List-bound fields must use values from `values` sheet.
- Keep `family_id` consistent to glue sizes into one product card.

## Common failure modes
- ZIP has top-level folder or `Images/` uppercase.
- `merchant_sku` duplicates for sizes (XL/4XL).
- Semicolon-delimited values rejected.
- Incorrect values not present in `values` sheet.

## Templates (category-specific)
- `templates/Men-thermal-underwear-import-template.xlsm`

## Known success reference
- `docs/offer_creation/ONLYFIT_SUIT61_V10_REFERENCE.xlsm`

Use the blueprint + template as the source of truth for each upload.
