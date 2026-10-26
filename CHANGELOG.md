# Changelog

## 0.3.1

Fixes from running the six new skills live on a real workspace:

- `list-enrichment`, `icp-lead-list`, `account-research`: strip subdomains (`app.`, `www.`) before looking up emails; take a company domain only from a row whose name matches, since the database also matches descriptions; try a company's second domain once on a miss; quote phones at the high end and flag a number whose country code fits neither the person nor the company.
- `account-research`: read job descriptions for angles; when two sources disagree (a funding database against the company's own posts), show both.
- `competitor-ads-teardown`: check the advertiser on every ad (a shared name returns another brand's ads) and pass the Facebook page URL for a certain match; wait on slow Google searches with `get_run`.
- `seo-competitor-gap`: for a site with few rankings, use the competitors the user names; ranked keywords come sorted by volume, so ask for 200 and keep positions 20 or better; read the AI overview's sources.
- `local-business-leads`: drop map results from another country; use published contacts (booking links, WhatsApp) when no email is found; name the lead the site shows and never guess the owner.

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
