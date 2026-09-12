# Contributing a skill

A skill is a GTM job an agent can finish, written so any agent can run it. Good skills are workflows people already do by hand and badly: they name the steps, the calls, the gates and the output. Feature demos and vendor pitches are not skills.

## Add one

1. Copy `templates/SKILL.md` to `skills/<your-skill>/SKILL.md`. Folder name in kebab-case, same as the `name` in the frontmatter.
2. Fill the frontmatter. The `description` is what makes an agent load the skill: say what the skill does and when to use it, in one paragraph, with the phrases a user would say.
3. Write the steps. Each step that touches data names the RouterGrowth capability and the input fields. Check the capability exists and is live: `routergrowth discover -q "..."` or https://www.routergrowth.com/catalog. Never invent a capability or a field.
4. Keep the rules: quote before a billable run, `max_cost` on every call, `max_total_cost` on a batch, stop before a batch over about $1 unless the user asked for that volume, never fabricate, never automate posting or engagement on a platform.
5. Put a human gate before anything that leaves the workspace: an email, an invite, a message, a purchase.
6. Run it end to end on a real account at least once. Say in the PR what it cost.
7. Open a PR. One skill per PR.

## Style

- Under 300 lines. Progressive disclosure: put long reference material in `reference.md` next to the skill and point to it.
- Plain sentences. No marketing.
- No em dashes. Use a colon, a comma, parentheses or two sentences.
- No secrets, keys, personal data or client names in any file. Example inputs use `example.com` and invented names.
- Prices belong to `inspect`, not to the file. Say "quote it" rather than quoting a number that will drift.

## What gets merged

A skill that runs, on a real account, and finishes a job a GTM team recognises. We test each PR against a live workspace before merging. Skills that wrap a single capability with no workflow around it are better as a use-case guide on the site; we will say so in review.

## Reporting a problem with a skill

Open an issue with the skill name, the agent you ran it in, the step that broke and the run ID (`routergrowth runs` prints it). Do not paste keys or personal data from run results.
