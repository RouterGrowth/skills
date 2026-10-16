# RouterGrowth skills

[![validate](https://github.com/RouterGrowth/skills/actions/workflows/validate.yml/badge.svg)](https://github.com/RouterGrowth/skills/actions/workflows/validate.yml) [![license: MIT](https://img.shields.io/badge/license-MIT-0c7c59.svg)](LICENSE) [![skills: 11](https://img.shields.io/badge/skills-11-0c7c59.svg)](#the-skills) [![routergrowth.com/skills](https://img.shields.io/badge/site-routergrowth.com%2Fskills-0c7c59.svg)](https://www.routergrowth.com/skills)

Open-source GTM workflows for Claude. Each skill is a `SKILL.md` the agent reads and follows: build a lead list from hiring signals, find the people discussing your category on X, Instagram, TikTok and YouTube, audit what ChatGPT and Perplexity say about a brand, map the Reddit threads that own a category, and draft the messages for the people worth contacting.

Every step that touches data calls a tool on the [RouterGrowth](https://www.routergrowth.com) connector: pay per call from one prepaid balance, with the price available before every paid call. The steps that reason (grading, writing, triage) run on the agent.

**The outreach workflows draft; you send.** No skill in this plugin sends an email, a LinkedIn invitation or a direct message. They research, qualify and write drafts for people who have a reason to hear from you, and you review and send them from your own tools. Nothing here posts, comments or automates engagement on a platform.

## Install

**Claude Code**:

```bash
claude plugin marketplace add RouterGrowth/skills
claude plugin install routergrowth@routergrowth
```

The plugin registers the RouterGrowth connector at `https://api.routergrowth.com/mcp/claude`. Run `/mcp` once to sign in with OAuth and approve a workspace. A new workspace gets $1 of credit once its email is verified.

**Claude apps**: add RouterGrowth from the connector directory under **Customize → Connectors**, then upload any skill folder under `skills/` as a skill.

## The skills

| Skill | Job | Tools it calls |
| --- | --- | --- |
| [routergrowth](skills/routergrowth) | The core skill: the connector's tools, spending rules, privacy rules, when not to use RouterGrowth | all |
| [hiring-signal-outbound](skills/hiring-signal-outbound) | Companies hiring for the role you sell to, the buyer at each, a verified email, a drafted first message | company_jobs, people_search, contact_find, contact_verify |
| [social-lead-discovery](skills/social-lead-discovery) | Leads from X, Instagram, TikTok and YouTube: who posts about the topic, who asks under a competitor's post, the website and contact on each profile, a drafted opener | social_search, social_comments, social_profile, contact_find, contact_verify |
| [cold-email-pipeline](skills/cold-email-pipeline) | Research, list, grade, verify, draft. Two human gates. A directives folder holds the ICP and the copy rules | people_search, contact_find, contact_verify, web_scrape |
| [sdr-daily](skills/sdr-daily) | One day of the loop: new replies, follow-ups due, suppressions, the day's drafts and a briefing | list_workspace_events, email_messages, get_subjects_history, workspace tables |
| [linkedin-outbound](skills/linkedin-outbound) | Find and read the profiles you pick, draft the connection note and first message, draft answers to replies | linkedin_search, linkedin_profile, linkedin_messages |
| [multichannel-intent-outbound](skills/multichannel-intent-outbound) | From intent signal to a drafted sequence across LinkedIn and email, one plan per person, three gates | people_search, social_search, linkedin_search, linkedin_profile, contact_find, contact_verify, watches and workspace tables |
| [ai-visibility-audit](skills/ai-visibility-audit) | A frozen prompt panel across ChatGPT, Claude, Gemini and Perplexity: mentions, citations, share of voice | aeo_answer, aeo_mentions, aeo_keywords, seo_serp |
| [reddit-surface-map](skills/reddit-surface-map) | The threads ranking for your money queries, the subreddits behind them, their rules | seo_serp, social_search, social_comments, web_scrape |
| [brand-mention-sweep](skills/brand-mention-sweep) | Every mention of the brand, founder and competitors in 90 days, with sentiment and the threads worth a human reply | social_search, news_search, web_search, reviews_search |
| [community-help-drafts](skills/community-help-drafts) | The Reddit and X threads where an honest answer is welcome, qualified against community rules, drafted for you to post | social_search, social_comments, seo_serp, web_scrape |

Prices come from `get_operation_pricing` at run time, never from this repo.

## Contact data and privacy

Contact lookups return business contact data from the providers listed in RouterGrowth's [privacy policy](https://www.routergrowth.com/privacy#people-in-lookup-results), which also explains the basis for processing it. Anyone can opt out at https://www.routergrowth.com/privacy/opt-out: lookups about them then return nothing and messages to them through RouterGrowth are blocked, in every workspace. The skills check the workspace's suppression list and history before drafting for anyone.

## Long-running loops

sdr-daily, linkedin-outbound, multichannel-intent-outbound and community-help-drafts run every day. They share one shape (read new replies before sourcing more, unknown is not "no reply", a reply stops the sequence), written up in [docs/daily-lifecycle.md](docs/daily-lifecycle.md).

## How a skill is built

- Frontmatter with `name` and `description` (the description is the trigger: say when to use it).
- The steps, in order, each naming the tool it calls and the input it passes.
- The rules: check the price before the first paid call of a kind, cap every call with `max_cost`, stop and ask before a run likely above about $1 unless the user set that budget, never present sandbox output as real data, never fabricate, and draft rather than send.
- The human gates: where the agent stops and shows its work.
- The output: what the user gets at the end, in what shape.

Read [CONTRIBUTING.md](CONTRIBUTING.md) to add one. Community skills are listed on https://www.routergrowth.com/skills.

## License

MIT. Copyright Altria LLC, the company that operates RouterGrowth.
