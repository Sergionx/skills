# skills

Personal, reusable [Claude Code](https://docs.claude.com/claude-code) / [skills.sh](https://www.skills.sh/) skills. Portable across projects — no project-specific hardcoding in the skill body; per-repo config lives in a local `.claude/*.config.json` that each skill reads and, on first run, offers to write.

## Layout

```
skills/
  <skill-name>/
    SKILL.md
    references/   # local docs the skill links to
    assets/       # templates, schemas, fixtures
```

Each `SKILL.md` follows the [Agent Skills](https://github.com/vercel-labs/skills) frontmatter contract (`name`, `description`, `license`, `metadata.author`, `metadata.version`) and the LLM-first style: short, imperative, decision tables over prose.

## Install

Via [skills.sh](https://www.skills.sh/):

```
npx skills add Sergionx/skills jira-mcp-sync
npx skills add Sergionx/skills venezuelan-prescription-pdf-validator
npx skills add Sergionx/skills minuta
npx skills add Sergionx/skills transcribe-whisperx
npx skills add Sergionx/skills smoke-checklist-generator
npx skills add Sergionx/skills jira-done-state-reconciliation
```

Or via the Claude Code plugin marketplace (adds every skill in this repo, auto-updates on pull):

```
/plugin marketplace add Sergionx/skills
/plugin install jira-mcp-sync@sergionx-skills
/plugin install venezuelan-prescription-pdf-validator@sergionx-skills
/plugin install minutas-toolkit@sergionx-skills
/plugin install smoke-checklist-generator@sergionx-skills
/plugin install jira-done-state-reconciliation@sergionx-skills
```

## Skills

| Skill | Trigger |
|---|---|
| [`jira-mcp-sync`](skills/jira-mcp-sync/SKILL.md) | Jira overlap search + task-breakdown-to-ticket diff via the Atlassian MCP server, gated on explicit approval before any write |
| [`venezuelan-prescription-pdf-validator`](skills/venezuelan-prescription-pdf-validator/SKILL.md) | Page-cited completeness screening for Venezuelan medical prescription PDFs, including pediatric and seven-day conditional checks |
| [`minuta`](skills/minuta/SKILL.md) | Generate standardized Spanish meeting minutes (HTML + Confluence-ready Markdown) from a transcript |
| [`transcribe-whisperx`](skills/transcribe-whisperx/SKILL.md) | Run WhisperX on a meeting recording to produce txt/srt/vtt/json/tsv transcripts |
| [`smoke-checklist-generator`](skills/smoke-checklist-generator/SKILL.md) | Manual smoke-testing checklist from spec and tasks, as a human gate between a clean `sdd-verify` and `sdd-archive` |
| [`jira-done-state-reconciliation`](skills/jira-done-state-reconciliation/SKILL.md) | After a clean `sdd-verify`, reconcile Jira ticket status with task completion and propose Done transitions gated on approval |

## License

Apache-2.0 — see [LICENSE](LICENSE).
