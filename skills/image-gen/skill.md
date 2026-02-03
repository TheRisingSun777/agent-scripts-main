---
name: image-gen
description: Batch organized Nano Banana Pro 2 image generations for wardrobe-combo references + prompts. Fully logged, trackable, with retry/edit support.
---

# Image Generation Workflow — Wardrobe Combos + Prompts

Batch generate images using Nano Banana Pro 2 (Gemini 3 Pro Image) with combo reference images and catalog prompts.

## Trigger Phrases
- "generate images", "generate nano banana pro 2 images"
- "lets generate [orange/studio] ui combos with [catalog] prompts"

## Defaults
- **Resolution:** 1K (unless specified: 2K, 4K)
- **Aspect:** 1:1 square
- **Concurrency:** 3 parallel (respects API limits)

---

## Input Sources

### Combo References (UI + Wardrobe)
```
Content_db_1/Kevin/beli51/Combos/
├── Hoodie_combo/
│   ├── Studio_UI_Combos/   (C-U-000 to C-U-008)
│   └── Orange_UI_Combos/   (C-U-009 to C-U-014)
├── longsleeve_combo/
│   └── [same structure]
└── t-shirt_combo/
    └── [same structure]
```

### Prompts (Distilled Catalogs)
```
Oracle/Content/Prompt_book/beli51/distilled/
├── catalog_v2.2/
├── catalog_v3.2/
├── catalog_v4.2/
└── catalog_v5.6/
```

---

## Combo-Driven Pose Rule
- Use the combo folder as the source of truth for all reference assets (wardrobe, bottom, product, UI, pose).
- Do **not** search outside the combo folder to find straight/full-height poses.
- If a prompt asks for straight/full-height but the combo only has MCU, use the MCU pose from that combo and proceed.

---

## Output Organization

```
Content_db_1/Kevin/beli51/Result_images/
└── {wardrobe}/                    # zip-hoodie, longsleeve, t-shirt
    └── {catalog}/                 # v2.2, v3.2, v4.2, v5.6
        └── {prompt_id}/           # ZH01, LS03_success_story, etc.
            └── {ui_style}/        # Studio, Orange
                └── {combo_id}/    # C-U-000, C-U-013, etc.
                    └── {timestamp}-{prompt_id}-{quality}.png
```

**Example path:**
```
Result_images/zip-hoodie/v3.2/ZH01_unboxing_experience/Studio/C-U-002/2025-01-15-14-30-22-ZH01-1K.png
```

---

## Session Tracking (CRITICAL)

### Session Log File
Create per-batch session log at start:
```
Result_images/.sessions/{timestamp}-session.json
```

### Log Structure
```json
{
  "session_id": "2025-01-15-14-30-00",
  "started": "2025-01-15T14:30:00",
  "config": {
    "wardrobe": "zip-hoodie",
    "catalogs": ["v2.2", "v3.2"],
    "ui_style": "Orange",
    "quality": "1K"
  },
  "jobs": [
    {
      "id": "001",
      "prompt_file": "ZH01_unboxing_experience.md",
      "combo": "C-U-009",
      "status": "completed|pending|failed|retry",
      "attempts": 1,
      "output": "path/to/output.png",
      "error": null,
      "started": "...",
      "completed": "..."
    }
  ],
  "summary": {
    "total": 45,
    "completed": 40,
    "failed": 3,
    "pending": 2
  }
}
```

### Status Values
- `pending` — queued, not started
- `running` — currently generating
- `completed` — success, output saved
- `failed` — error after max retries
- `retry` — failed, will retry

---

## Execution Flow

### 1. Initialize Session
```bash
SESSION_ID=$(date +%Y-%m-%d-%H-%M-%S)
SESSION_LOG="$RESULT_BASE/.sessions/$SESSION_ID-session.json"
mkdir -p "$(dirname $SESSION_LOG)"
```

### 2. Build Job Queue
For each combo × prompt combination:
```python
jobs = []
for combo in combos:
    for prompt in prompts:
        jobs.append({
            "combo_path": combo,
            "prompt_file": prompt,
            "output_dir": build_output_path(...)
        })
```

### 3. Execute with Concurrency Control
```python
MAX_CONCURRENT = 3
RETRY_LIMIT = 3
RETRY_DELAY = [5, 15, 30]  # exponential backoff seconds

async def process_job(job):
    for attempt in range(RETRY_LIMIT):
        try:
            result = await generate_image(job)
            update_session_log(job, "completed", result)
            return
        except RateLimitError:
            await asyncio.sleep(RETRY_DELAY[attempt])
        except TimeoutError:
            await asyncio.sleep(RETRY_DELAY[attempt])
        except APIError as e:
            if attempt == RETRY_LIMIT - 1:
                update_session_log(job, "failed", error=str(e))
```

### 4. Generation Command
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "$FULL_PROMPT" \
  --filename "$OUTPUT_PATH" \
  --input-image "$COMBO_REF_IMAGE" \
  --resolution 1K
```

**Prompt construction:**
```
[Prompt from catalog .md file]

Reference image shows: UI layout, composition, background, lighting.
Keep exact: layout structure, text positions, color scheme, typography style.
Replace model wardrobe with: [wardrobe description from combo]
```

---

## API Handling

### Rate Limits
- **Quota:** ~60 requests/minute (Google default)
- **Concurrency:** Max 3 parallel requests
- **Cooldown:** 1 second between requests minimum

### Error Handling
| Error | Action |
|-------|--------|
| 429 Rate Limit | Wait 30s, retry |
| 500 Server Error | Wait 15s, retry up to 3x |
| 403 Forbidden | Stop batch, check API key |
| Timeout (>60s) | Cancel, retry with backoff |
| Image rejected | Log, skip, continue |

### Timeout Gates
```bash
timeout 90s uv run ... || echo "TIMEOUT"
```

---

## CLI Commands

### Start Batch Generation
```bash
# Example: Orange UI combos with catalog v3.2 prompts
./image-gen.sh \
  --wardrobe zip-hoodie \
  --ui-style Orange \
  --catalogs "v3.2,v4.2" \
  --quality 1K \
  --output /path/to/Result_images
```

### Resume Failed Jobs
```bash
./image-gen.sh --resume $SESSION_ID
```

### Retry Specific Job
```bash
./image-gen.sh --retry $SESSION_ID --job 015
```

### View Session Status
```bash
./image-gen.sh --status $SESSION_ID
```

---

## Progress Display

```
[Session: 2025-01-15-14-30-00]
Wardrobe: zip-hoodie | UI: Orange | Quality: 1K
Catalogs: v3.2, v4.2

Progress: [████████████░░░░░░░░] 60% (27/45)
Running:  3 | Completed: 24 | Failed: 0 | Pending: 18

Current:
  → [026] ZH02_travel_ready + C-U-011 (attempt 1)
  → [027] ZH03_quality_control + C-U-011 (attempt 1)
  → [028] ZH04_lifestyle_beyond_gym + C-U-011 (attempt 1)

Recent:
  ✓ [025] ZH01_unboxing_experience + C-U-011 → saved
  ✓ [024] ZH01_unboxing_experience + C-U-010 → saved
```

---

## Post-Generation

### Review Failed Jobs
```bash
cat $SESSION_LOG | jq '.jobs[] | select(.status=="failed")'
```

### Regenerate Single Image
```bash
./image-gen.sh --single \
  --combo "C-U-013" \
  --prompt "catalog_v3.2/ZH01_unboxing_experience.md" \
  --wardrobe zip-hoodie \
  --quality 2K
```

### Batch Quality Upgrade
```bash
# Upgrade completed 1K to 4K
./image-gen.sh --upgrade $SESSION_ID --to-quality 4K
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Generate Orange UI batch | `--ui-style Orange --catalogs "v3.2,v4.2"` |
| Generate Studio UI batch | `--ui-style Studio --catalogs "v2.2,v5.6"` |
| Resume session | `--resume SESSION_ID` |
| Check status | `--status SESSION_ID` |
| Retry failed | `--retry SESSION_ID` |
| Single regenerate | `--single --combo X --prompt Y` |

---

## Notes

- Always check session log before starting new batch
- Failed jobs auto-logged with error details for debugging
- Use `--dry-run` to preview job queue without executing
- Combo images are used as `--input-image` reference (image-to-image)
- Prompt text from .md files merged with combo context
