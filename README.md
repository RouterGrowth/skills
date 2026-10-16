# RouterGrowth skills

[![validate](https://github.com/RouterGrowth/skills/actions/workflows/validate.yml/badge.svg)](https://github.com/RouterGrowth/skills/actions/workflows/validate.yml) [![license: MIT](https://img.shields.io/badge/license-MIT-0c7c59.svg)](LICENSE) [![skills: 11](https://img.shields.io/badge/skills-11-0c7c59.svg)](#the-skills) [![routergrowth.com/skills](https://img.shields.io/badge/site-routergrowth.com%2Fskills-0c7c59.svg)](https://www.routergrowth.com/skills)

GTM research workflows for Claude, on one pay-per-call balance. RouterGrowth gives Claude the data a sales or marketing team usually buys from several vendors: companies and the people in them, verified work emails, hiring and funding signals, live search results and keyword data, what ChatGPT and Perplexity say about a brand, public social posts and comments, maps, reviews and ad libraries. This plugin adds the connector and eleven skills that turn those tools into finished jobs: a qualified lead list, an AI visibility audit, a map of the Reddit threads that own a category, a brand mention sweep, and messages to the people worth contacting, sent by email once you approve them.

You pay per call from a prepaid RouterGrowth balance, with no subscription. Claude checks the price before the first call of a kind, caps every call, and asks before a job likely to cost more than about $1.

## What you can ask

- "Research linear.app: what the company does, its size, its tech stack and any open sales roles."
- "Find 20 heads of sales at fintech companies in London that are hiring SDRs, with verified work emails."
- "Ask ChatGPT and Perplexity what the best email verification tool is, and tell me which brands and sources they cite."
- "Which Reddit threads rank on Google for 'best crm for startups', and what do those communities recommend?"
- "Write a first email to each of these five accounts based on what they posted this month, and send them from my inbox once I approve."

## How it works

1. **Connect.** The plugin registers the RouterGrowth connector at `https://api.routergrowth.com/mcp/claude`. The first time, Claude asks you to sign in to RouterGrowth (OAuth) and approve a workspace. A new workspace gets $1 of credit once its email is verified.
2. **Ask.** A skill loads when your request matches it, and tells Claude which tools to call, in what order, with which checks and human gates.
3. **Pay per result.** Each tool states its billing rule: lookups are charged only when they find something, lists are priced per row returned, and failed calls cost nothing. Every paid call returns a receipt (run id, provider, amount), and `list_runs` reads them back for free.
4. **Keep the work.** With workspace tables turned on, lists persist between conversations, and the do-not-contact list applies to every session.

## The skills

| Skill | Job | Tools it calls |
| --- | --- | --- |
| [routergrowth](skills/routergrowth) | The core skill: the connector's tools, spending rules, privacy rules, when not to use RouterGrowth | all |
| [hiring-signal-leads](skills/hiring-signal-leads) | Companies hiring for the role you sell to, the buyer at each, a verified email, a first email sent after your approval | company_jobs, people_search, contact_find, contact_verify |
| [social-lead-discovery](skills/social-lead-discovery) | Leads from X, Instagram, TikTok and YouTube: who posts about the topic, who asks under a competitor's post, the website and contact on each profile, a drafted opener | social_search, social_comments, social_profile, contact_find, contact_verify |
| [email-list-pipeline](skills/email-list-pipeline) | Research, list, grade, verify, write, send by email after approval. A directives folder holds the ICP and the copy rules | people_search, contact_find, contact_verify, web_scrape, email_send, gmail_send |
| [sdr-daily](skills/sdr-daily) | One day of the loop: new replies, follow-ups due, suppressions, the day's approved emails and a briefing | list_workspace_events, email_messages, email_send, get_subjects_history, workspace tables |
| [linkedin-drafts](skills/linkedin-drafts) | Find and read the profiles you pick, draft the connection note and first message, draft answers to replies | linkedin_search, linkedin_profile, linkedin_messages |
| [intent-messaging](skills/intent-messaging) | From intent signal to a plan per person: LinkedIn drafts and an email follow-up sent after approval, three gates | people_search, social_search, contact_find, contact_verify, email_send, watches and workspace tables |
| [ai-visibility-audit](skills/ai-visibility-audit) | A frozen prompt panel across ChatGPT, Claude, Gemini and Perplexity: mentions, citations, share of voice | aeo_answer, aeo_mentions, aeo_keywords, seo_serp |
| [reddit-surface-map](skills/reddit-surface-map) | The threads ranking for your money queries, the subreddits behind them, their rules | seo_serp, social_search, social_comments, web_scrape |
| [brand-mention-sweep](skills/brand-mention-sweep) | Every mention of the brand, founder and competitors in 90 days, with sentiment and the threads worth a human reply | social_search, news_search, web_search, reviews_search |
| [community-help-drafts](skills/community-help-drafts) | The Reddit and X threads where an honest answer is welcome, qualified against community rules, drafted for you to post | social_search, social_comments, seo_serp, web_scrape |

Prices come from `get_operation_pricing` at run time, never from this repo.

## Messaging

The messaging skills write to people who have a reason to hear from you: customers, inbound leads, event attendees, people who engaged with your content, introductions, or a business contact where you have a legitimate reason and the law allows it.

- **Email** goes out from your RouterGrowth inbox or your Gmail, only after you approve each message exactly as shown (from, to, subject, body), one at a time at the daily pace you set. Suppressed people, people who opted out with RouterGrowth and people already written to recently are blocked by the server, in every workspace.
- **LinkedIn, Instagram and WhatsApp** go out from your personal logins, so the skills keep them as drafts you send yourself. The core skill can send a single message there to someone who already knows you, after you approve it. No connection requests, no sequences.
- Nothing here posts, comments, follows or automates engagement on a platform, and no skill connects an account or sets up a sending domain on its own.

## What this plugin connects to and sends

- **One remote MCP server:** `https://api.routergrowth.com/mcp/claude`, declared in `.mcp.json`, reached over OAuth. When Claude calls one of its tools, the tool's inputs (a domain, a name, a search phrase, an email you approved) go to RouterGrowth, which forwards them to the data provider that serves the call and returns the result to Claude.
- **Nothing else.** The plugin has no hooks, commands, binaries or packages that run on your machine (`scripts/check_skills.py` is a CI check for contributors, never run by the plugin), sends no telemetry and fetches no instructions at run time: everything Claude follows is in the `SKILL.md` files here.
- **Feedback only on request.** The connector has a `submit_feedback` tool that sends a bug report to the RouterGrowth team. The skills call it only when you ask, or after offering and getting your yes, and never include personal data in it.

## Contact data and privacy

- **Sources:** work emails come from LeadMagic, Apollo, Icypeas and Findymail; phone numbers from LeadMagic, Apollo and Findymail; professional profiles and people lists from Icypeas's business contact database, Apollo and public LinkedIn pages; social profiles from the public page on each platform. Every result names its provider.
- **Basis:** business-to-business research about people in their professional role, on legitimate interests. RouterGrowth keeps no shared database of people: a result stays in the workspace that asked for it.
- **Opt-out:** anyone can opt out at https://www.routergrowth.com/privacy/opt-out. Lookups about them then return nothing and messages to them through RouterGrowth are blocked, in every workspace. The skills also check the workspace's suppression list and history before drafting for anyone.
- Details: the [privacy policy](https://www.routergrowth.com/privacy#people-in-lookup-results).

## Install

**Claude apps and Cowork:** add RouterGrowth from the plugin directory, then sign in when Claude asks.

**Claude Code:**

```bash
claude plugin marketplace add RouterGrowth/skills
claude plugin install routergrowth@routergrowth
```

Then run `/mcp` once to sign in with OAuth and approve a workspace.

## Long-running loops

sdr-daily, linkedin-drafts, intent-messaging and community-help-drafts run every day. They share one shape (read new replies before sourcing more, unknown is not "no reply", a reply stops the sequence), written up in [docs/daily-lifecycle.md](docs/daily-lifecycle.md).

## Contributing

Each skill names the tool it calls at every step, checks the price before the first paid call of a kind, caps every call with `max_cost`, has human gates, never fabricates, and sends only what the user approved. Read [CONTRIBUTING.md](CONTRIBUTING.md) to add one. Community skills are listed on https://www.routergrowth.com/skills.

## Support

- Documentation and troubleshooting: https://www.routergrowth.com/docs/claude-connector
- Questions and account help: hello@routergrowth.com
- Security reports: security@routergrowth.com

## License

MIT. Copyright Altria LLC, the company that operates RouterGrowth.
