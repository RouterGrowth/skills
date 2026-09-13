# RouterGrowth skills

[![validate](https://github.com/RouterGrowth/skills/actions/workflows/validate.yml/badge.svg)](https://github.com/RouterGrowth/skills/actions/workflows/validate.yml) [![license: MIT](https://img.shields.io/badge/license-MIT-0c7c59.svg)](LICENSE) [![skills: 11](https://img.shields.io/badge/skills-11-0c7c59.svg)](#the-skills) [![routergrowth.com/skills](https://img.shields.io/badge/site-routergrowth.com%2Fskills-0c7c59.svg)](https://www.routergrowth.com/skills)

Open-source GTM workflows for agents. Each skill is a `SKILL.md` an agent reads and runs: build a lead list from hiring signals, run a cold email pipeline with human gates, work a LinkedIn outbound loop, audit what ChatGPT and Perplexity say about a brand, map the Reddit threads that own a category, batch ad creative.

Every step that touches data calls a [RouterGrowth](https://www.routergrowth.com) capability: one key, pay per call, one balance, a price quoted before every billable run. The steps that reason (grading, writing, triage) run on the agent. Nothing here posts, comments or automates engagement on a platform.

## Install

**Claude Code** (skills plus the MCP connection, one command):

```bash
claude plugin marketplace add RouterGrowth/skills
claude plugin install routergrowth@routergrowth
```

The plugin registers `https://api.routergrowth.com/mcp`. Run `/mcp` once to sign in with OAuth, or add a key: `claude mcp add --transport http routergrowth https://api.routergrowth.com/mcp --header "Authorization: Bearer rg_live_..."`.

**Any agent that reads Agent Skills** (Codex, Cursor, Gemini CLI, OpenClaw, Hermes, Cline):

```bash
npx skills add RouterGrowth/skills
```

**By hand**: copy any folder under `skills/` into your agent's skills directory (`~/.claude/skills/`, `.cursor/rules/`, `~/.openclaw/skills/`). Each skill is self-contained.

**One line, any agent**: paste `Set up https://www.routergrowth.com/SKILL.md` into the agent. That installs the core skill; the workflows in this repo build on it.

## The skills

| Skill | Job | Capabilities it calls |
| --- | --- | --- |
| [routergrowth](skills/routergrowth) | The core skill: CLI, HTTP and MCP contract, spending rules, when not to use RouterGrowth | all |
| [hiring-signal-outbound](skills/hiring-signal-outbound) | Companies hiring for the role you sell to, the buyer at each, a verified email | company.jobs, people.search, contact.find, contact.verify |
| [social-lead-discovery](skills/social-lead-discovery) | Leads from Instagram, TikTok and YouTube: who posts about the topic, who asks under a competitor's post, the bio link and email on each profile, a verified address, the Instagram DM from your own account behind a gate | social.search, social.comments, social.profile, instagram.profile, contact.find, contact.verify, instagram.message |
| [cold-email-pipeline](skills/cold-email-pipeline) | Research, list, grade, verify, write, send. Two human gates. Directives folder holds the ICP and the copy rules | people.search, contact.find, contact.verify, web.scrape, email.inboxes, email.send |
| [sdr-daily](skills/sdr-daily) | One day of the loop: drip, follow-ups due, reply triage, suppression, briefing | email.messages, email.send, history |
| [linkedin-outbound](skills/linkedin-outbound) | Search, read the profile, invite with a note, message after accept, read replies. Daily caps | linkedin.search, linkedin.profile, linkedin.invite, linkedin.message, linkedin.messages |
| [ai-visibility-audit](skills/ai-visibility-audit) | A frozen prompt panel across ChatGPT, Claude, Gemini and Perplexity: mentions, citations, share of voice | aeo.answer, aeo.mentions, aeo.keywords, seo.serp |
| [reddit-surface-map](skills/reddit-surface-map) | The threads ranking for your money queries, the subreddits behind them, their rules | seo.serp, social.search, social.comments, web.scrape |
| [brand-mention-sweep](skills/brand-mention-sweep) | Every mention of the brand, founder and competitors in 90 days, with sentiment and the threads worth a human reply | social.search, news.search, web.search, reviews.search |
| [community-help-drafts](skills/community-help-drafts) | The Reddit and X threads where an honest answer is welcome, qualified against community rules, drafted for the user to post | social.search, social.comments, seo.serp, web.scrape |
| [ad-creative-batch](skills/ad-creative-batch) | Variants, edits, cutouts, upscales and one video from a brief, priced before generation | creative.image, creative.image_edit, creative.remove_background, creative.upscale, creative.video |

Prices come from `inspect` at run time, never from this repo. The catalog with live prices: https://www.routergrowth.com/catalog.

## Long-running loops

sdr-daily, linkedin-outbound and community-help-drafts run every day. They share one shape (monitor before you source, unknown is not "no reply", an approval covers one exact message, a reply stops the sequence), written up in [docs/daily-lifecycle.md](docs/daily-lifecycle.md).

## How a skill is built

- Frontmatter with `name` and `description` (the description is the trigger: say when to use it).
- The steps, in order, each naming the capability it calls and the input it passes.
- The rules: inspect before any billable run, cap every call with `max_cost`, batch with `max_total_cost`, stop and ask before a batch over about $1 unless the user asked for that volume, never present sandbox output as real data, never fabricate.
- The human gates: where the agent stops and shows its work before anything is sent.
- The output: what the user gets at the end, in what shape.

Read [CONTRIBUTING.md](CONTRIBUTING.md) to add one. Community skills are listed on https://www.routergrowth.com/skills.

## Keys and credit

Sign up on https://www.routergrowth.com/dashboard for a key and $1 of credit, or from the CLI: `npm install -g routergrowth && routergrowth signup --email you@company.com --org "Your company"`. The first calls cost a fraction of a cent.

## License

MIT. Copyright Altria LLC, the company that operates RouterGrowth.
