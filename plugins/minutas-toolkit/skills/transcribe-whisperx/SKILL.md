---
name: transcribe-whisperx
description: "Trigger: transcribir, transcripción, whisperx, audio a texto, pasar la grabación. Run WhisperX on a meeting recording to produce txt/srt/vtt/json/tsv transcript files."
license: Apache-2.0
metadata:
  author: sergionx-dev
  version: "1.0"
---

## Activation Contract

Load this skill when the user has a raw recording (audio or video) and wants a transcript, before any minuta can be written. Distinct phase from `minuta` — this skill's job ends at producing transcript files; it never writes the minuta itself.

## Hard Rules

- Never run `whisperx` blind — always verify it's on PATH first (see Execution Steps). If missing, do NOT silently fail with a raw shell error and do NOT install anything without explicit user confirmation first.
- Default model: `medium` (good accuracy/speed tradeoff for meeting-length recordings). Only change model if the user asks.
- Default `--language es` unless the recording is clearly in another language or the user overrides.
- Always pass `--output_format all` and `--output_dir "<same meeting folder as the recording>"` so `.txt/.srt/.vtt/.json/.tsv` land together.
- Never delete or move the original recording file.
- If the run fails for a reason other than "not installed" (missing CUDA, OOM, wrong ffmpeg), report the exact error line — don't guess a fix silently; ask before changing model size or falling back to CPU-only flags if that changes output quality.
- Installing WhisperX changes the user's Python environment — never run the install command without them explicitly saying yes first.

## Execution Steps

1. Locate the recording file (audio/video) in the meeting folder given or referenced by the user.
2. Check availability: run `whisperx --help` (or `where whisperx` / `which whisperx`). If it resolves, skip to step 4.
3. If `whisperx` is NOT found:
   - Tell the user plainly it's missing (don't just paste the raw shell error).
   - Explain prerequisites: Python 3.9+, `ffmpeg` on PATH, optionally a CUDA GPU for speed (CPU works, just slower).
   - Ask explicitly: "¿Querés que lo instale ahora?" — do not proceed without a yes.
   - If they confirm, run `pip install whisperx` (and `ffmpeg` via the OS package manager if also missing — ask separately if that requires elevated/admin rights, since this workspace has shown restricted permissions before).
   - Re-run the availability check from step 2 before continuing. If it still fails, report the exact error and stop — don't loop retrying installs.
4. Run: `whisperx "<recording path>" --model medium --language es --output_format all --output_dir "<meeting folder>"`
5. Confirm the 5 output files were created in that folder.
6. Report file paths and total audio duration if shown in the CLI output. Suggest running the `minuta` skill next.

## Output Contract

Return: command executed, output files created, duration transcribed, any warnings from the CLI (e.g. overlapping speech, low-confidence segments) so the `minuta` skill's footnote can cite them.

## References

- `minuta` skill — consumes these transcript files to produce the standardized minuta.
