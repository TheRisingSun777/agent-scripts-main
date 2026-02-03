---
name: onlyfit-catalog-adoption
description: Adapt or convert ONLYFIT prompt catalogs or prompt books from one product to another (e.g., Beli51 <-> Suit61), preserving structure and non-product content while updating product-specific context (bundle count, garments, color scheme, logos, and item lists).
---

# ONLYFIT Catalog Adoption

Use this skill when the user asks to adopt or convert a catalog or prompt set from one product to another (e.g., Suit61 -> Beli51, Beli51 -> Suit61). The goal is to keep the original structure and messaging, but rewrite product-specific context to match the target product.

## Required references

- Source of truth for product deltas:
  `docs/Product_descriptions/beli51_vs_suit61_product_comparison.md`
- Catalog structure and tables:
  `docs/Onlyfit_catalog_generation_rules.md`

If you are ingesting or rebuilding prompt books/catalogs, also use:
- `onlyfit-catalog-adjust`
- `prompt-catalog-ingest`

## Core rules

- Preserve all non-product content and layout instructions.
- Replace only product-specific context (bundle count, garment list, color scheme, logos, item count, and product-specific slides).
- Do NOT introduce new claims or features not present in the target product reference.
- Remove any zipper color mentions. Use only "zip" or "zipper" (no color).
- If target product lacks a wardrobe part present in a prompt (e.g., Tank/Jersey), skip that prompt and note it in the conversion report.
- Update any counts/tables so they match the final prompt set.
- Maintain prompt IDs unless the wardrobe itself changes (e.g., removing TK for Beli51).

## Workflow

1) Identify source and target product
   - Confirm which catalog or prompt set is the source.
   - Confirm the target product and where the output should live.

2) Load product deltas
   - Read the comparison doc listed above.
   - Extract the target-only parameters and source-only parameters.

3) Apply product conversion
   - Update bundle badge (5v1 vs 6v1).
   - Update item count and package contents list.
   - Update color scheme (two-tone vs solid black).
   - Update logo removal list (Nike only vs Nike + PROCOMBAT).
   - Add or remove the Tank/Jersey (Mayka) content based on target.
   - Remove zipper color mentions (keep only "zip" / "zipper").

4) Handle product-specific slides
   - If target does not include Tank/Jersey, remove or repurpose those slides.
   - If target includes Tank/Jersey, add/keep those slides and update numbering.

5) Recalculate catalog tables
   - Update distribution tables, quick-jump tables, and totals.
   - Ensure prompt counts and IDs remain consistent.

6) Validate
   - Scan for source-only tokens that should not appear in target output.
   - Confirm no zipper color mentions remain.

## Directional checklists (summary)

Beli51 -> Suit61
- 5v1 -> 6v1
- 5 items -> 6 items
- two-tone -> solid black
- add Tank/Jersey (Mayka) content
- add PROCOMBAT to logo removal
- remove zipper color mentions (use only "zip" / "zipper")

Suit61 -> Beli51
- 6v1 -> 5v1
- 6 items -> 5 items
- solid black -> two-tone
- remove Tank/Jersey content
- remove PROCOMBAT from logo removal
- remove zipper color mentions (use only "zip" / "zipper")

## Output expectations

- Keep output paths stable and predictable.
- Report any prompts skipped because the target product does not include that wardrobe part.
- Provide a brief summary of changes and a list of removed/added slides.
- If any step is ambiguous, ask before rewriting content.
