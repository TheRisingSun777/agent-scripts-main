---
name: combo-sync
description: Sync combo folders, .env files, and _registry.md entries across wardrobes after a combo set changes (e.g., beli51 Studio/Orange). Use when asked to “sync combos”, “resync registries”, or propagate a changed combo set from one wardrobe to others.
---

# Combo Sync (wardrobe → wardrobe)

Use this skill when the user says a combo set changed (e.g., `Hoodie_combo/Studio_UI_Combos`) and wants the same combo IDs/UIs applied across the other wardrobes and repo registries.

## Required Inputs (ask if missing)
- Model (e.g., `beli51`)
- Combo style / variant (e.g., `Studio_UI_Combos` or `Orange_UI_Combos`)
- Source combo path (e.g., `/Users/.../beli51/Combos/Hoodie_combo/Studio_UI_Combos`)
- Target wardrobes to sync (e.g., longsleeve, t-shirt, product-only)
- Any exclusions (e.g., remove `C-U-000`)

## Workflow (Sequential)

1) **Inventory source combos**
   - Read the source combo folder.
   - Extract combo IDs (e.g., `C-U-003`, `C-U-007`).
   - For each combo ID, list files (UI, bottom, pose, wardrobe).

2) **Sync target wardrobe folders (Content_db_1)**
   - For each target wardrobe combo folder:
     - Create missing combo IDs.
     - Copy UI and other constants from source (UI images).
     - Swap wardrobe file to the target’s wardrobe image (MCU/full body).
     - Keep bottom and pose consistent with source if present.
   - Remove deprecated combo IDs:
     - Prefer moving old combos to `_deprecated/` unless user explicitly asks to delete.

3) **Update Input_images/Combos envs**
   - Regenerate `*.env` for the synced combo set:
     - Ensure correct paths for UI/bottom/pose/wardrobe.
     - Use `product-only` combos to map WARDROBE to product image, no pose.
   - Remove envs that are no longer in the combo list.

4) **Update registries**
   - Update `_registry.md` per wardrobe:
     - Replace old combo ranges with the new list.
     - Update UI source paths to reflect variant (e.g., Orange → `ui_all/Orange/`).
     - Document new combos and deprecations.

5) **Orange/Studio split (when asked)**
   - If product-only or other wardrobes need separate Orange/Studio folders:
     - Create `Orange_UI_Combos/` and `Studio_UI_Combos/` under the combo folder.
     - Ensure matching combo IDs and update envs/registries accordingly.

6) **Verify**
   - Ensure every combo ID has a valid env file.
   - Ensure all referenced files exist on disk.
   - Confirm generation scripts point to the correct combo root for each wardrobe.

## Safety Rules
- Do not delete existing images or combo folders unless explicitly requested.
- Default to moving deprecated combos into `_deprecated/`.
- Never change prompt text unless asked.
- Avoid hardcoded absolute paths in scripts; use env vars when editing scripts.

## Typical Locations
- Source combos (Content_db_1):  
  `/Users/adil/Docs/Business2/Content/Content_db_1/<Model>/Combos/<Wardrobe>_combo/<Variant>`
- Env files (repo):  
  `Input_images/Combos/<model>/<wardrobe>/<Variant>/*.env`
- Registries (repo):  
  `Input_images/Combos/<model>/<wardrobe>/_registry.md`
