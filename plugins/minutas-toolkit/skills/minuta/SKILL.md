---
name: minuta
description: "Trigger: minuta, minutas, acta de reunión, resumen de reunión. Generate standardized Spanish meeting-minutes as an HTML (humans) and a companion Confluence-ready Markdown from a transcript."
license: Apache-2.0
metadata:
  author: sergionx-dev
  version: "1.0"
---

## Activation Contract

Load this skill when the user asks to create, generate, or update a "minuta" (meeting minutes) from a transcript or set of raw notes — in this project (`Grabaciones y minutas`) or any project with the same need. This skill does NOT transcribe audio/video — if only a raw recording exists and no transcript file yet, use the `transcribe-whisperx` skill first, then come back here.

## Hard Rules

- Content language is Spanish (professional/neutral register), matching this workspace's institutional context. The skill's own instructions stay in English; only generated minuta content is Spanish.
- Output is a single self-contained HTML file (inline `<style>`, no external assets, no CDN). Must support both light and dark rendering via `@media (prefers-color-scheme: dark)` plus `:root[data-theme]` overrides.
- Before writing the HTML, load the `frontend-design` skill and apply its guidance for typography, color, and layout — `assets/template.html` is a structural starting point (sections/data model), not a fixed final look. Vary visual treatment per minuta instead of reusing identical styling every time.
- Never fabricate names, dates, decisions, or contact data not present in the transcript. If duration/date is inferred from file metadata rather than stated verbally, mark it `(según metadata del archivo)`.
- NEVER add a closing footer/disclaimer paragraph about transcription source, tool/model used, or transcription-limitations/confidence caveats (e.g. "Minuta generada a partir de transcripción automática..."). The user explicitly rejected this boilerplate — omit it entirely, in both `.md` and `.html`, every time. If something genuinely needs flagging (e.g. a low-confidence segment, an unidentified speaker), fold it inline where relevant instead — and only if truly load-bearing, never as a default habit.
- Directorio and Glosario sections are optional — include only when there are 3+ contacts or 3+ acronyms/terms worth listing; drop the section entirely otherwise, don't pad it.
- File names: `minuta-{slug-of-meeting-folder}.html` and `minuta-{slug-of-meeting-folder}.md`, both inside that meeting's own folder (sibling to the transcript files).
- The `.md` carries the SAME facts as the `.html` (never diverge) but in plain Confluence-friendly Markdown: standard `#`/`##` headers, `-` bullets, `**bold**`, pipe tables — no inline HTML, no CSS classes, no custom `<div>` wrappers. This is what gets pasted/imported into Confluence.

## Decision Gates

| Available input | Action |
|---|---|
| `.txt`/`.vtt`/`.srt` transcript present | Read `.txt` for full text; use `.srt`/`.vtt` only if timestamps of specific moments are needed |
| `.json`/`.tsv` (WhisperX word/segment data) present | Use only for speaker attribution or precise timing, not as primary read source |
| No transcript, only raw notes given by user | Use the notes directly as source; do not invent transcript provenance in the footnote |
| Folder already has a `minuta-*.html` | Treat as update: preserve existing facts, add/correct only what changed |

## Execution Steps

1. Locate the meeting folder and its transcript file(s) (prefer `.txt`).
2. Read the transcript. Extract: date/duration (from filename/metadata if not stated), participants, one-line topic, 2-4 sentence summary, topics discussed (grouped, factual bullets), decisions/agreements, pending action items with an owner each.
3. Load the `frontend-design` skill, then build the HTML from `assets/template.html`'s structure (sections/placeholders), filling every `{PLACEHOLDER}` and applying `frontend-design`'s guidance to the actual styling. Remove any optional section left empty (Directorio/Glosario) rather than leaving it blank.
4. Copy `assets/template.md` and fill it with the exact same extracted facts (same sections, same wording where practical) — plain Markdown, no HTML.
5. Write both files as `minuta-{slug}.html` and `minuta-{slug}.md` in the meeting folder.
6. Do not touch or reformat the raw transcript files.

## Output Contract

Report: both file paths written, participant/decision/pending counts, and any transcript segment you excluded as unreliable (call it out explicitly, don't silently drop it).

## References

- `assets/template.html` — fillable HTML skeleton (light/dark aware), for humans reading locally.
- `assets/template.md` — fillable plain-Markdown skeleton, for Confluence import/paste.
- `references/sample-minuta.html` — real minuta from this workspace showing the target level of detail and tone.
