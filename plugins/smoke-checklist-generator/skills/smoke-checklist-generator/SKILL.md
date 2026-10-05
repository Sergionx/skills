---
name: smoke-checklist-generator
description: "Trigger: sdd-verify clean, before sdd-archive, smoke checklist, manual test gate. Generate a manual smoke-testing checklist from the change spec and tasks as a human gate before archive."
license: Apache-2.0
metadata:
  author: "sergionx"
  version: "1.0"
---

# Smoke Checklist Generator

## Purpose

Generate manual smoke-testing checklist from change's spec and tasks artifacts, right after `sdd-verify` report clean (no CRITICAL issues), before `sdd-archive` run. Human checkpoint: automated verify pass, but user eyeball real behavior before change close. Skill only produce checklist — never execute app, server, test command, or archive itself.

## Activation Contract

Activate when ALL true:
- `sdd-verify` phase just completed for change AND reported clean (no CRITICAL issues).
- `sdd-archive` not run yet for this change.

Do NOT activate when:
- verify report missing, incomplete, or show CRITICAL issues — say so, stop, no checklist.
- `sdd-archive` already ran for this change — too late, out of scope.
- User ask ad-hoc manual test list unrelated to verify-to-archive gate — handle as normal request, not this skill.
- Spec or tasks artifact missing for change — say so explicitly, do not invent checklist from guesswork.

## Instructions

1. Locate change's spec artifact and tasks artifact (SDD change folder). If either missing, stop and report which one missing — do not fabricate content.
2. Read spec artifact fully. Extract every acceptance criterion and spec scenario (Given/When/Then or equivalent).
3. Read tasks artifact fully. Note which files/areas each task touched — this feed regression-watch section.
4. Classify extracted items into three groups:
   - **Golden path** — main demoable behavior, listed first. One clear flow user would show a stakeholder.
   - **Edge cases** — empty states, errors, permissions/auth boundaries, validation failures. Each gets own explicit step. Never fold into golden-path step.
   - **Regression watch** — existing behavior change could disturb, derived from files tasks touched (not new behavior, prior behavior near touched code).
5. For each step determine how user reach it: dev server URL + route, CLI command, API endpoint + method, or console/script invocation. Pull from spec/design/tasks artifacts or existing project conventions (package.json scripts, README, existing routes) — never invent a URL or command not evidenced in repo.
6. Render numbered Markdown checklist. Format each line exactly:
   `- [ ] N. Step — action — expected result`
   Include reach-instruction (URL/command/endpoint) inline in the action part.
7. Every step must cite the requirement or acceptance criterion it verifies (short parenthetical reference, e.g. "(AC-3)" or spec scenario name) so user can point back to it if it fail. No generic "click around" or "test the feature" filler steps.
8. If change has no user-facing surface (pure backend/internal refactor), say so explicitly in one line, then produce minimal API/CLI-level check (request/command + expected response/exit code) instead of inventing UI steps.
9. End checklist with exact line: `Check each box, then tell the assistant to proceed with sdd-archive.`
10. Present checklist to user. Do not check any box. Do not run sdd-archive. Wait for user confirmation.

PROACTIVE SAVE TRIGGERS (call `mem_save` after):
- Checklist generated for a change (save change name, item counts per group, artifact paths used).
- Skill skip due to missing spec/tasks artifact or CRITICAL issues found (save reason, so future session know gate blocked).
- User confirm checklist passed and requests `sdd-archive` proceed (save confirmation event, timestamp).

## Rules

- Never run `sdd-archive` — this skill only produce checklist, never trigger archive phase itself.
- Never mark any checklist box as passed on user's behalf. User executes and confirms, always.
- Never run the app, dev server, or test command yourself. Checklist for human to run manually.
- Never invent UI steps, URLs, or commands not evidenced in spec/tasks/repo. Backend-only change gets API/CLI check, not fake UI steps.
- Every step must trace to an actual acceptance criterion or spec scenario — no filler.
- Edge cases always separate steps, never merged into golden path.
- If spec or tasks artifact missing, or verify report shows CRITICAL issues, stop and report — do not generate partial/guessed checklist.
- Checklist output format fixed: `- [ ] N. Step — action — expected result`, ending with exact reminder line specified in Instructions step 9.
- Does not replace `sdd-verify` — this is post-verify, pre-archive human gate only. Runs once per change, after verify clean report.

## Interaction with sdd-verify

This skill activate only after `sdd-verify` sub-agent complete and report clean (no CRITICAL issues) for a change. It read the same spec/tasks artifacts `sdd-verify` validated against, but produce human-facing manual checklist rather than automated pass/fail report. `sdd-verify` stays authoritative for automated contract validation (spec/design/tasks alignment); this skill add the manual-eyeball layer on top, strictly between verify-clean and archive-start. If `sdd-verify` reports CRITICAL issues, this skill does not activate — fix loop back to `sdd-apply`/`sdd-verify` first.

## Examples

**Example 1 — user-facing feature, verify clean:**
Verify report clean for change `add-password-reset`. Skill read `spec.md` (3 acceptance criteria: request reset, valid token reset, expired token rejected) and `tasks.md` (touched `auth/reset.ts`, `routes/auth.ts`, `email/templates/reset.html`). Output:

```
- [ ] 1. Golden path: request password reset — go to http://localhost:3000/forgot-password, submit valid registered email — expect confirmation message "check your email" and reset email received (AC-1)
- [ ] 2. Golden path: complete reset with valid token — click reset link from email, set new password on /reset-password?token=... — expect success message and login works with new password (AC-2)
- [ ] 3. Edge case: expired token — visit /reset-password?token=<expired> — expect error "link expired, request a new one", no password change allowed (AC-3)
- [ ] 4. Edge case: unregistered email request — submit forgot-password form with unregistered email — expect same generic confirmation message (no account enumeration) (AC-1)
- [ ] 5. Regression watch: existing login flow — go to /login, sign in with unrelated existing account — expect normal login unaffected (touched routes/auth.ts)

Check each box, then tell the assistant to proceed with sdd-archive.
```

**Example 2 — backend-only refactor:**
Change `refactor-db-connection-pool` touched only `db/pool.ts`, no routes/UI. Spec has 2 acceptance criteria about connection reuse and max-pool-size enforcement. Output:

```
No user-facing surface — this is an internal DB connection-pool refactor. Minimal API/CLI-level check:

- [ ] 1. Golden path: pool reuse — run `npm run db:stats` after issuing 5 concurrent queries via `node scripts/load-test-db.js --concurrency 5` — expect active connections ≤ configured pool max (AC-1)
- [ ] 2. Edge case: pool exhaustion — run `node scripts/load-test-db.js --concurrency 50` (exceeds pool max) — expect queued requests wait, no crash/error thrown (AC-2)
- [ ] 3. Regression watch: existing query paths — run `npm test -- db/pool.test.ts` manually and confirm exit code 0 (touched db/pool.ts)

Check each box, then tell the assistant to proceed with sdd-archive.
```

**Example 3 — trigger condition not met:**
User ask for checklist but `sdd-verify` report shows 1 CRITICAL issue (missing error handling in `payment/charge.ts`). Skill responds: "Verify report shows CRITICAL issue — payment/charge.ts missing error handling. Fix required before smoke checklist. Not generating checklist until verify clean." No checklist produced, no archive suggested.
