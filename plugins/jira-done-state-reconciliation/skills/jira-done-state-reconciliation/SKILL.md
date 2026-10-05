---
name: jira-done-state-reconciliation
description: "Trigger: sdd-verify clean, before sdd-archive, jira done reconciliation, ticket status check. Confirm Jira tickets for a change reach Done and propose transitions gated on explicit approval."
license: Apache-2.0
metadata:
  author: "sergionx"
  version: "1.0"
---

# Jira Done-State Reconciliation

## Purpose

Run right after `sdd-verify` reports clean (no CRITICAL issues), before `sdd-archive` runs. Confirms every Jira ticket tied to change actually reach Done-equivalent status. Cross-check ticket status against task completion in apply-progress artifact. Propose transitions, never apply without explicit user approval. Complements `sdd-verify` — does not replace or re-run verify logic, only consumes its clean result as gate.

## Activation Contract

Activate when ALL true:
- `sdd-verify` phase just completed for this change AND reported clean (no CRITICAL issues).
- `sdd-archive` has NOT run yet for this change.
- Repo contains `.claude/jira-sync.config.json`.

Do NOT activate when:
- verify report missing, incomplete, or shows CRITICAL issues — say so, do nothing else.
- `.claude/jira-sync.config.json` missing or missing required fields (`cloudId`, `projectKey`) — skip check entirely, say so, no fallback/guess.
- User ask for ad-hoc Jira lookup unrelated to this verify-to-archive gate — go straight to Atlassian MCP tools instead.
- `sdd-archive` already ran for this change — too late, out of scope.

## Instructions

1. Read verify report for this change. If not clean (CRITICAL issues present, or report missing/unreadable), stop. State: verify not clean, check skip, no ticket lookup done.
2. Read `.claude/jira-sync.config.json` in repo root. Require `cloudId` and `projectKey`. If file missing or fields missing, stop. State: config absent/incomplete, check skipped, no guess made.
3. Read tasks artifact and apply-progress artifact for this change. Build ticket set (Jira keys referenced) and per-task completion state.
4. For each ticket key, call `mcp__atlassian__getJiraIssue` (scoped to config's `cloudId`) to get current status.
5. Cross-check ticket status vs matching task completion:
   - Task(s) complete, ticket status NOT Done-equivalent → add row to proposed-transitions table.
   - Task(s) incomplete despite verify clean → do NOT touch ticket. Flag as inconsistency (verify should not have passed with incomplete tasks tied to this change). List separately from proposed-transitions.
6. Render proposed-transitions table: `Key | Current status | Proposed status | Reason`. Render inconsistency list separately if any. STOP here. No write tool call yet.
7. Only proceed to writes if prompt explicitly states user already approved this exact table (not a generic "go ahead" — must reference the specific proposal).
8. On approval, for each approved row: call `mcp__atlassian__getTransitionsForJiraIssue` fresh for that ticket, pick transition that reaches Done-equivalent status. Never hardcode or reuse a transition id from memory or another ticket/project. If no Done-equivalent transition exists, skip that row, report why.
9. Call `mcp__atlassian__transitionJiraIssue` per approved+resolved row. Report final state per ticket.

PROACTIVE SAVE TRIGGERS (call `mem_save`, `capture_prompt: false`):
- Config file found/read outcome (present with valid fields, or missing/incomplete) for this repo.
- Inconsistency flagged (task incomplete + verify clean) — save as bug/discovery, include change name and ticket key.
- Transitions actually applied (ticket keys, from-status, to-status, change name).
- Any Done-equivalent transition not found for a ticket (surface as discovery for future runs).

Reference Engram protocol: after significant work here, call `mem_save`; before saying "done", call `mem_session_summary`.

## Interaction with sdd-verify

This skill does not re-implement or override `sdd-verify` checks. It reads verify's report as a precondition only. `sdd-verify` owns spec/design/task-contract validation; this skill owns Jira-side status reconciliation, strictly gated on verify's clean result. If verify itself is re-run or its result changes, re-evaluate this skill's trigger from scratch — do not cache a stale "clean" state across sessions.

## Rules

- Never hardcode `cloudId` or `projectKey` anywhere — always read from `.claude/jira-sync.config.json` per repo.
- Never fall back to a default/guessed project or cloud id when config missing/incomplete — skip and say so.
- Never call any Jira write tool (`transitionJiraIssue`, `editJiraIssue`, etc.) before explicit user approval of the exact rendered table.
- Never transition a ticket whose matching task is incomplete — flag as inconsistency instead, regardless of approval wording.
- Never guess or hardcode a transition id — always fetch fresh via `getTransitionsForJiraIssue` per ticket per run.
- Never run this check if verify report shows CRITICAL issues or is unavailable.
- Never run after `sdd-archive` has already executed for the change.
- Always render proposed-transitions table and stop before any write, every single run — no exceptions for "small" changes.

## Examples

**Example 1 — clean verify, config present, one ticket needs transition**
Verify reports clean. Config has cloudId + projectKey. Tasks artifact shows TASK-3 (linked to PROJ-101) complete. PROJ-101 status = "In Review". Output:

```
Key      | Current status | Proposed status | Reason
PROJ-101 | In Review       | Done             | Matching task complete, verify clean
```
Stop. Wait for approval.

**Example 2 — inconsistency detected**
Verify clean. TASK-5 (linked to PROJ-104) marked incomplete in apply-progress, but verify passed. Output: flag inconsistency — "TASK-5 incomplete but verify reported clean; PROJ-104 not touched. Resolve task/verify mismatch before archive."

**Example 3 — config missing**
No `.claude/jira-sync.config.json` in repo. Output: "Config absent, Jira reconciliation skipped, no default project assumed."

**Example 4 — approval given**
Prior turn rendered table with PROJ-101. User says "approved, go ahead with PROJ-101 → Done." Fetch transitions for PROJ-101 fresh, find Done-equivalent, apply, report result.

**Example 5 — verify not clean**
Verify report shows 2 CRITICAL issues. Output: "Verify not clean, skip Jira check."
