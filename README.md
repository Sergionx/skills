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
```

Or via the Claude Code plugin marketplace (adds every skill in this repo, auto-updates on pull):

```
/plugin marketplace add Sergionx/skills
/plugin install jira-mcp-sync@sergionx-skills
```

## Skills

| Skill | Trigger |
|---|---|
| [`jira-mcp-sync`](skills/jira-mcp-sync/SKILL.md) | Jira overlap search + task-breakdown-to-ticket diff via the Atlassian MCP server, gated on explicit approval before any write |

## License

Apache-2.0 — see [LICENSE](LICENSE).
