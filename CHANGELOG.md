# Changelog

## 0.3.0

- Six new skills built on what users run most: `icp-lead-list`, `list-enrichment`, `account-research`, `competitor-ads-teardown`, `seo-competitor-gap`, `local-business-leads`.
- Every skill that looks up emails, phones or profiles now passes the waterfall cap (`max_cost_for_all`), so all data providers get to try before a row counts as a miss.
- Install in one line from any agent: `npx skills add RouterGrowth/skills`. Manifests for Codex, Cursor and Gemini CLI, and a cross-agent marketplace file.
- Frontmatter that claude.ai accepts on upload (`version` moved under `metadata`), and one ZIP per skill attached to each release.
- `evals/evals.json` in every skill: prompts that should and should not trigger it, and what a good run must do.
- Skills grouped by job in the README: find leads, enrich, research, messaging.
- The skill template moved to `docs/skill-template.txt`, so installers stop listing it as a skill.

## 0.2.3

- Messaging names for the four outreach skills.
