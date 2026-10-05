---
name: jira-mcp-sync
description: "Trigger: jira sync, ticket overlap check, task breakdown to jira, sdd jira handoff, sync tickets. Search Jira via MCP for overlapping issues before work starts, and propose CREATE/UPDATE/SUPERSEDE ticket diffs after a task breakdown, gated on explicit approval."
license: Apache-2.0
metadata:
  author: "sergionx"
  version: "1.0"
---

# Jira MCP Sync

## Activation Contract

Load at two points in any planning workflow: (1) before/alongside drafting a proposal or starting new work, to surface overlapping tickets; (2) immediately after a task breakdown is approved, to diff it against Jira.

## Hard Rules

- Never call a Jira write tool (`createJiraIssue`/`editJiraIssue`/`transitionJiraIssue`/`createIssueLink`/`addCommentToJiraIssue`) before the user explicitly approves the rendered diff.
- The start-of-work context search is informational only — never blocks, never auto-supersedes.
- Never hardcode cloudId, project key, issue type, assignee, sprint field, or story-point field. Read them from `.claude/jira-sync.config.json` in the current repo (see `references/config-example.json`). If missing, ask the user once for the values, then offer to write the config file so future runs in this repo don't re-ask.
- No Jira issue-delete tool exists. "Remove" a ticket means: prefix its summary with `[SUPERSEDED BY <key(s)>]` and add an explanatory comment — never attempt deletion.
- Subtasks never get their own sprint field — omit it when issue type is a subtask variant (parent's sprint applies automatically; setting it errors).

## Decision Gates

| Trigger | Action |
|---|---|
| Start of work | JQL search `project = <key>` by 3-5 keywords from the change topic; list matches (key, summary, status) as context, non-blocking |
| Task breakdown approved | Diff computed tickets against existing Jira tickets (search by parent key if known, else keyword); classify CREATE / UPDATE / SUPERSEDE; render diff; get approval; only then write |

## Execution Steps

1. Load `.claude/jira-sync.config.json` from the current repo; if absent, ask for cloudId/project key/issue type/assignee account id/sprint field/story-point field/blocking-link type name once and offer to persist it.
2. **At start of work**: derive keywords from the change summary, call `searchJiraIssuesUsingJql`. Surface hits inline — key, summary, status. Do not gate on this.
3. **At breakdown-approved**: derive one ticket per vertical slice of demoable work. Search Jira for existing tickets under the same parent or by keyword to build the current-state baseline.
4. Classify each computed ticket: no match -> CREATE; matching ticket with changed scope -> UPDATE; existing ticket now covered elsewhere -> SUPERSEDE.
5. Render one diff table: `Key or NEW | Action | Summary | Description delta`. Do not call any write tool yet.
6. Ask for explicit approval (apply all / pick per-row / cancel). Wait for the answer.
7. On approval, apply in order: CREATE -> UPDATE -> SUPERSEDE -> blocking links (confirm exact link-type name via `getIssueLinkTypes` once per session before first use).

## Output Contract

Report the exact set of ticket keys created/updated/superseded/linked, and any diff rows the user declined.

## References

- `references/config-example.json` — shape of the per-repo `.claude/jira-sync.config.json` this skill reads.
