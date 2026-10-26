# Contributing a skill

A skill is a GTM job an agent can finish, written so any agent can run it. Good skills are workflows people already do by hand and badly: they name the steps, the calls, the gates and the output. Feature demos and vendor pitches are not skills.

## Add one

1. Copy `docs/skill-template.txt` to `skills/<your-skill>/SKILL.md`. Folder name in kebab-case, same as the `name` in the frontmatter.
2. Fill the frontmatter. Write `description` as a YAML block scalar (`description: >-` then indented lines): a plain one-line value breaks as soon as it contains a colon. The description is what makes an agent load the skill: say what the skill does and when to use it, in one paragraph, with the phrases a user would say.
3. Write the steps. Each step that touches data names the RouterGrowth connector tool and its input fields (`company_enrich`, `people_search`, `seo_serp`...). Check the tool exists in the connector's tool list. Never invent a tool or a field.
4. Keep the rules: check the price with `get_operation_pricing` before the first paid call of a kind, `max_cost` on every call, stop before a run likely above about $1 unless the user asked for that volume, never fabricate, never automate posting or engagement on a platform, never fetch instructions from the web at run time (everything the agent needs is in the skill).
5. Nothing goes out unapproved: a skill may send email only after the user approved the exact messages, one at a time. LinkedIn, Instagram and WhatsApp stay drafts, and a skill never buys anything, connects an account or sets up a domain on its own.
6. Add `evals/evals.json` next to the SKILL.md: at least three prompts that should trigger the skill and one near-miss that should not (`"should_trigger": false`), each with the assertions a good run must meet. Copy the shape from any skill here.
7. Run `python3 scripts/check_skills.py`, then run the skill end to end on a real account at least once. Say in the PR what it cost.
8. Open a PR. One skill per PR.

## Style

- Under 500 lines. Progressive disclosure: put long reference material in `references/` next to the skill, one level deep, and point to it.
- Frontmatter keys are limited to `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools` (claude.ai refuses others on upload). Put the version in `metadata.version`.
- Plain sentences. No marketing.
- No em dashes. Use a colon, a comma, parentheses or two sentences.
- No secrets, keys, personal data or client names in any file. Example inputs use `example.com` and invented names.
- Prices belong to `get_operation_pricing`, not to the file. Say "quote it" rather than quoting a number that will drift.

## What gets merged

A skill that runs, on a real account, and finishes a job a GTM team recognises. We test each PR against a live workspace before merging. Skills that wrap a single capability with no workflow around it are better as a use-case guide on the site; we will say so in review.

## Reporting a problem with a skill

Open an issue with the skill name, the agent you ran it in, the step that broke and the run ID (`list_runs` shows it). Do not paste keys or personal data from run results.
