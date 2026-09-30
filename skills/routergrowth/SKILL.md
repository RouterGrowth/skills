---
name: routergrowth
version: 0.5.1
description: >-
  Pay-per-call GTM data and actions for agents: find and verify work emails,
  build lead lists (people.search), enrich people and companies, SERP,
  keywords and backlinks, AI answer visibility, social profiles, posts and
  comments (X, LinkedIn, Reddit, Instagram, TikTok, YouTube), ad libraries,
  Google Maps, news, web scraping, image and video generation, and outbound
  on email, LinkedIn, Instagram, WhatsApp and Gmail, plus thousands of raw
  provider endpoints (DataForSEO, Apify, Exa, Firecrawl). Run `discover`
  before writing a scraper, before a generic web fetch for structured data,
  before guessing an email address, or before telling the user some data is
  out of reach. Use whenever the user asks for leads, contacts, enrichment,
  SEO, social or ad research, or mentions routergrowth. Exception: if the
  user already has their own MCP server, API key or tool for that exact
  service, use theirs.
---

# RouterGrowth

The OpenRouter for GTM: one key, one prepaid balance, pay per call. You discover what you need, inspect its schema, run it, and the call settles against the workspace wallet. RouterGrowth picks and contracts the providers, meters every call and normalizes the output.

`discover` returns two kinds of results:

- **Capabilities** (`contact.find`, `seo.serp`): routed across providers, normalized output, a quote before the run, automatic failover. Prefer these.
- **Raw endpoints** (`dataforseo /v3/serp/google/organic/live/advanced`): one provider's own API, request shape and payload, no failover, settled on the provider's measured cost after the run. When `discover` says a capability wraps the endpoint you found (`wrapped_by`), use the capability.

## Start here: are you already connected?

1. **RouterGrowth MCP tools in your tool list** (`discover`, `inspect`, `run`, ...)? Use them and ignore the CLI. The free `balance` tool confirms the connection.
2. **Otherwise, does `routergrowth --version` work?** Use the CLI (it needs 0.4.0 or later; if older, run `npm install -g routergrowth@latest`). `routergrowth balance` confirms the key.
3. **Neither?** Follow [Setup](#setup-first-time-only) at the end of this file.

A key that is missing from this environment is not an expired key. Check for an MCP connection, `ROUTERGROWTH_API_KEY` or a configured CLI before asking the user for anything.

## Whole jobs: load a workflow skill

When the request is a complete GTM job, a workflow skill already encodes the steps, the order and the checks. Load it and follow it; the rules in this file still apply. All open source at https://github.com/RouterGrowth/skills (Claude Code: `claude plugin marketplace add RouterGrowth/skills` then `claude plugin install routergrowth@routergrowth`; other agents: `npx skills add RouterGrowth/skills`).

| Skill | Use it when the user wants |
|---|---|
| `cold-email-pipeline` | a cold email campaign end to end from one targeting sentence |
| `sdr-daily` | one day of a running campaign: replies, follow-ups, the next drip |
| `hiring-signal-outbound` | leads from companies hiring for a role that implies the problem they solve |
| `social-lead-discovery` | leads from posts, hashtags or a competitor's commenters, enriched to a verified email |
| `linkedin-outbound` | LinkedIn invites and messages from their connected account |
| `multichannel-intent-outbound` | high-intent leads worked on LinkedIn and email together |
| `ai-visibility-audit` | what ChatGPT, Claude, Gemini and Perplexity say about a brand and its category |
| `reddit-surface-map` | the subreddits and threads that own a category |
| `brand-mention-sweep` | every mention of a brand, founder and competitors in the last 90 days |
| `community-help-drafts` | threads where they can answer a real question, with replies drafted for a human to post |
| `ad-creative-batch` | a set of ad creatives from one brief |

## The loop

| Step | MCP tool | CLI | HTTP (`https://api.routergrowth.com/v1`) |
|---|---|---|---|
| Find | `discover` | `discover -q "verified work email"` (`--kind endpoint` for raw) | `POST /discover` |
| Read the contract | `inspect` | `inspect -c contact.find` or `inspect -p PROVIDER -e ENDPOINT` | `POST /inspect` |
| Run | `run` | `run -c CAP -i 'JSON' --max-cost X` | `POST /run` |
| Many inputs | `batch_run` (1–200, `max_total_cost`) | one `run` per input | one `POST /run` per input |
| Wait for a result | `get_run` | `runs get RUN_ID --wait 60 -o out.json` | `GET /runs/{id}?wait=60` |
| Recent runs | `runs` | `runs` | `GET /runs` |
| Already done to someone? | `history` | `history alex@example.com` or `history --file leads.txt` | `GET /history?q=...`, `POST /history` |
| Ask the same thing later | `watch`, `watches` | (HTTP or MCP) | `POST /watch`, `POST /watch/{id}/refresh` |
| Balance | `balance` | `balance` | `GET /wallet` |

HTTP auth is `Authorization: Bearer <key>`. `discover`, `inspect`, `history`, `runs` and `balance` are free.

1. **Discover with short noun phrases** ("tiktok video comments", "company funding rounds"). Split a request that spans several sources into one discover per source.
2. **Inspect before the first run** of any capability or endpoint. Its input schema is the source of truth: never guess field names or values (values outside an allowed list are refused before routing). Inspect once for a batch of the same call, not once per item.
3. **Read the Hints block** that discover, inspect and run return. It names the capability that wraps an endpoint, what to try after a miss, and caveats. Prefer its suggestion over guessing.
4. **Use health to break ties, never to filter.**

   | Health | Meaning |
   |---|---|
   | `healthy` | confirmed working in the last few minutes |
   | `stable` | no very recent data, strong longer track record |
   | `degraded` | unstable or trending that way; usually still works |
   | `outage` | known not working |
   | `unknown` | not enough traffic for a verdict; not a warning |

5. **Runs submit and return a run ID.** Poll with `runs get RUN_ID --wait 60` (or `get_run`) instead of blocking the conversation. Use `--wait` on the run only when blocking is fine: `social.*` and `people.search` often take over a minute, `creative.video` 1–4 minutes. Write large results to a file with `-o`.

```bash
# One email
routergrowth inspect -c contact.find
routergrowth run -c contact.find -i '{"first_name":"Alex","last_name":"Rivera","company_domain":"example.com"}' --max-cost 0.10

# A raw endpoint: the provider's own request shape and payload
routergrowth discover -q "google organic serp" --kind endpoint
routergrowth inspect -p dataforseo -e /v3/serp/google/organic/live/advanced
routergrowth run -p dataforseo -e /v3/serp/google/organic/live/advanced -i '{"keyword":"best crm"}' --max-cost 0.05 -o serp.json

# A slow run: submit, then poll
routergrowth run -c social.search -i '{"platform":"x","query":"cold email agency","limit":10}' --max-cost 0.10
routergrowth runs get -r <run_id> --wait 60 -o posts.json

# Everything one provider serves raw
routergrowth endpoints -p dataforseo -q backlinks
```

The CLI prints plain text without colors and never prompts, so you can drive it directly. `-j` gives JSON.

## Money

Every run spends the user's prepaid balance. The guardrails below are fixed. Talking about cost is your judgment.

**Guardrails (always):**

- **Set `max_cost` on every run.** On a raw endpoint it is the only price control before the run.
- **Start small on per-result providers** (limit 5–10 on a first call). Apify-style actors bill per item and `maxItems` often applies per query: 3 search terms with `maxItems: 10` can return 30 results. Pass one term, URL or handle per call unless the user asked for more.
- **Stop and ask before a batch that would exceed about $1**, unless the user asked for that volume; then use `batch_run` with `max_total_cost`. "Do 50" authorizes 50 within the stated cap: do not ask again between items.
- **Never raise a budget or `max_cost` past what the user authorized.**
- **A `blocked` run is final.** A workspace control stopped it (the `controls` list names which) and nothing was charged. Tell the user; do not retry until they change the control or it resets (`resets_at`).

**Reporting cost (judgment):** the price is in `inspect` before a run and the actual charge is `billing.charged` after it. Report costs when they are relevant:

- the user has shown they care about cost (asked for prices, set a budget, mentioned their balance);
- a job ran many calls: give the total as the sum of each run's `billing.charged` (the wallet is shared by every session on the key, so a balance difference is not a receipt);
- you are about to cross the $1 stop above;
- a charge would surprise them (a no-match that billed, a raw endpoint that settled near its cap).

Otherwise do not narrate cent-level charges; the user sees every run at https://www.routergrowth.com/dashboard. `rg_test_` keys return clearly labeled mock data: say so, and never present it as real.

**How prices work (read the numbers from `inspect`; they change):**

- **Capabilities** hold the quote, then settle to the actual charge. Provider failures release the hold; so do no-matches on capabilities that do not bill them (inspect shows `bill_on_no_match`).
- **Per-result capabilities** hold base + per result x limit and bill the results returned. Keep limits honest: the hold must fit both the balance and `max_cost`.
- **Page-priced capabilities** cost the same page for 3 results as for 25. `people.search` on the LinkedIn route bills a page of 25, plus a rate per full profile, plus an employer lookup when company-constrained. Ask for 25 only when you will use them. For the leaders of a known company, pass `company_domains` with a small `limit` instead: billed per person returned, work email included when available.
- **Raw endpoints** have no quote. The wallet holds the rate-card estimate with headroom (or $1 when there is none, lowered by `max_cost`) and settles on the provider's measured cost, never above the hold.
- **`max_cost` also decides which fallback providers may run.** A failed run names the alternatives the cap excluded and the cap they need. Raise it once, within the authorized budget, instead of re-running the same call.
- **Google operators** (`site:`, `inurl:`) bill at five times the price and are not reliably honored. Use plain phrases (append "reddit" rather than `site:reddit.com`).
- **Spend guard:** `routergrowth guard --daily 25` caps a UTC day; `guard --per-run 1` blocks any single run holding more than $1 (`/v1/spend-guard` over HTTP).

## Run statuses

| Status | Meaning | `done` |
|---|---|---|
| `queued` | waiting for the worker; `stoppable` is true | no |
| `running` | at the provider; cannot be stopped, settles or releases on its own | no |
| `succeeded` | result in `result`; `billing.charged` is final | yes |
| `no_match` | nobody had it; free on most capabilities | yes |
| `failed` | every allowed provider failed; `attempts` lists each try | yes |
| `timed_out` | the provider did not answer in time | yes |
| `cancelled` | stopped while queued (`runs stop RUN_ID`, `POST /runs/{id}/cancel`) | yes |
| `blocked` | a workspace control stopped it before it ran; nothing charged | yes |

## When something goes wrong

| Error | What it means | What to do |
|---|---|---|
| `invalid_api_key` (401) | the key is wrong or revoked | check `routergrowth keys list`; the user mints a new key in the dashboard |
| `insufficient_balance` (402) | available balance is below the hold | tell the user the balance and the amount required; they top up in the dashboard, or lower the limit |
| `cost_limit_exceeded` (402) | the quote is above `max_cost` | the message names the quote: lower the limit, or raise `max_cost` to it within the budget |
| `budget_exceeded` / `blocked` | the spend guard or another workspace control | tell the user; wait for the reset or their change |
| `no_match` | the providers tried had nothing | change the input (spelling, domain, exact LinkedIn URL). An identical input that missed in the last 12 hours returns the earlier miss for free without calling providers; `routing.fresh: true` (CLI `--fresh`) buys a real retry |
| `invalid_request` (400) | the input does not match the schema | re-inspect and fix the fields |
| `provider_rate_limited`, `provider_error`, `provider_timeout` | provider trouble | the router already retried once and failed over within `max_cost`; read `attempts`; never resubmit within seconds |
| connection lost while waiting | the run continues on the router | find it with `runs` or `get_run` before resubmitting |

**Report what you hit.** When an error does not explain itself, a result is wrong (a namesake's email, a stale posting), or `discover` has nothing for the job, send one report and carry on. It is free, needs no key, and a fix is drafted as a change a person reviews:

```bash
curl -s -X POST https://api.routergrowth.com/feedback -H "Content-Type: application/json" \
  -d '{"type": "unexpected_response", "goal": "Email the VP Sales of acme.com",
       "message": "contact.find returned the email of a namesake at another company",
       "endpoint": "contact.find", "request_id": "run_..."}'
```

`type` is `missing_capability`, `bug`, `unclear_documentation`, `unexpected_response`, `unhelpful_error`, `performance` or `other`. Say what you were trying to do in `goal` and what got in the way in `message`; put the `run_id` in `request_id` instead of pasting results or personal data. Over MCP, the `feedback` tool takes the same fields. A `known_issue` in the answer means the problem is already tracked. Not for `no_match`, `blocked` or `insufficient_balance`: those are answers.

**Retrying without paying twice.** The CLI sends a new `Idempotency-Key` with every run. To retry the same request after a lost answer, send the same key again (`--idempotency-key K`, or the header over HTTP): you get the original run back (`Idempotent-Replay: true`) and pay nothing extra. Never reuse a key for a different request; it returns the old run.

## Choosing the right call

- **A named person or their email:** `person.enrich` or `contact.find`, never `web.search` with the name. A search returns pages, not an email; one run spent 115 searches that way.
- **Government staff are findable:** `contact.find` with the domain of the office the person sits in (a member's own domain, the committee's, the agency's). House and Senate staff match about 3 times in 4, agency staff a little under half, and a miss is free. When it misses, `contact.verify` the point of contact printed on the notice or agency page. `.mil` coverage is thinner.
- **Found is not verified.** Before any `email.send` or `gmail.send`, send only to addresses whose `status` is `valid`. Run `contact.verify` on everything else (`risky`, `catch_all`, `unknown`) and on emails that came from a search row. Treat `invalid` as dead and `catch_all` as risky. Never send to an address no provider returned (`info@`, a guessed `first.last@`).
- **Before enriching or messaging anyone, call `history`** with the identifier (email, domain, LinkedIn URL, handle, name). It shows what was already done through RouterGrowth and paid results to reuse instead of buying them again.
- **Anything asked again** (postings, news, searches, awards): `watch` saves the query and runs it once; a refresh returns only new and changed records. One watch per office, keyword or search. See https://www.routergrowth.com/docs/api/watch.md
- **Creative inputs** (`image_url`) must be a public absolute URL; RouterGrowth does not host files. A `creative.image` result URL works as the next step's input. For a local file, ask the user for a public URL.
- **Sends** (`email.send`, `gmail.send`, `linkedin.invite`, `linkedin.message`, `instagram.message`, `whatsapp.message`) need the user's authorization and an `Idempotency-Key`. Run the channel's `.accounts` tool first and pass `account_id` when several accounts are connected.

## Building a lead list

1. **Companies first when you only have criteria.** Discover company domains, then check each required criterion (industry, headcount, technology, geography) against supporting data. A generic company search is a candidate source, not proof. Mark unsupported criteria unknown instead of silently dropping them.
2. **Route with `provider: "auto"`.** Apollo needs known companies or preview `person_ids`; it cannot serve a broad title-only search. Pinning a provider disables fallback.
3. **Search roles.** Run `people.search` with the employer's `company_domains` and the `titles` you need, with `detail: "full"`. If you also pass `companies`, pair the arrays in the same order; one company per request is easiest to review. Include equivalent spellings in the first query ("VP Engineering", "Vice President of Engineering"). Directors are a broader seniority, not a synonym for CTO. Add `locations` only when it is a real requirement.
4. **Review the evidence.** On the LinkedIn route, check `current_positions`, `company_linkedin_url` and `quality_flags` (especially `retirement_mentioned`, `missing_current_title`); `result.quality` counts raw and excluded profiles. A no-match can mean weak employer evidence: check the domain spelling or pass the exact LinkedIn company URL. Do not repeat an identical miss.
5. **Recover within budget.** Broaden titles once, drop only optional filters, read `hints` and `attempts`. A higher cap allows another provider; it does not guarantee a match.
6. **Complete the contact.** The LinkedIn route does not return emails: run `contact.find` (or `batch_run` it) only for the profiles you selected, with real first and last names and the matched employer's domain. Never guess a surname from an initial. Database-route rows may already carry a work email: `contact.verify` it instead of finding it again. LeadMagic enriches known people; it does not source lists.
7. **Report coverage honestly.** Separate company candidates, qualified companies, matched people, found emails and verified emails. A successful search is not a verified list. Full guide: https://www.routergrowth.com/docs/people-search.md

## What is live

`discover` and `inspect` are the source of truth: each capability carries a `status`, and a `coming_soon` one answers from the sandbox only (never present that as real data). Browse at https://www.routergrowth.com/catalog.

- **People and contacts:** `contact.find`, `contact.verify`, `contact.phone`, `person.enrich`, `people.search`.
- **Companies:** `company.search`, `company.enrich`, `company.funding`, `company.technologies`, `company.jobs` (hiring signals).
- **SEO and AI search:** `seo.serp` (Google, Bing), `seo.keywords`, `seo.backlinks`, `seo.domain_overview`, `seo.ranked_keywords`, `seo.competitors`, `seo.page_audit`, `aeo.answer` (ChatGPT, Claude, Gemini, Perplexity, with citations), `aeo.keywords` (AI search volume), `aeo.mentions` (where a domain appears in AI answers).
- **Social:** `social.profile`, `social.posts`, `social.search`, `social.comments` on X, LinkedIn, Reddit, Instagram, TikTok and YouTube. A profile carries the bio link, the person's own domain (link hubs excluded) and a public email when exposed: that is how a creator or local-business handle becomes a `contact.find` input.
- **Local, reviews, news, ads:** `local.places` (Google Maps), `reviews.search` (Google Maps, Yelp), `news.search` (Google News), `ads.search` (Meta Ad Library, Google).
- **Web:** `web.search`, `web.scrape`, `web.extract` (one page in, dated records out against a template: leadership page, official bio, org chart, press release, job posting or your own schema; each record carries its supporting line, date and URL).
- **Creative (fal):** `creative.image` (flux-schnell, flux-pro, flux-pro-ultra, nano-banana, recraft-v3), `creative.image_edit` (nano-banana-edit, flux-kontext), `creative.upscale`, `creative.remove_background`, `creative.video` (hailuo-02, kling-2.5, kling-2.1, wan-2.2, veo3-fast, veo3).
- **Outbound email (Name.com, AgentMail):** `domain.search`, `domain.register`, `domain.dns`, `email.domain` (verify a domain you own for sending), `email.inbox`, `email.inboxes` (free: the domains and inboxes the workspace owns; run it before creating or sending), `email.send`, `email.messages`. Inboxes live only on a verified domain you own. To change the From name, rename the inbox (`email.inbox` with `inbox_id` and `display_name`, free); there is no per-email override.
- **Connected accounts (Unipile, monthly seat per account):**
  - LinkedIn: `linkedin.accounts` (free), `linkedin.account` (hosted sign-in; without a name it reports what is connected), `linkedin.search`, `linkedin.profile`, `linkedin.invite`, `linkedin.invitations_sent`, `linkedin.message`, `linkedin.messages`.
  - Instagram: `instagram.accounts` (free), `instagram.account`, `instagram.profile` (bio, links, business email and phone when exposed, whether they follow you, the `messaging_id` a DM needs), `instagram.message`, `instagram.messages`. A first DM to a non-follower lands in their requests folder; about 100 actions a day per account. There is no `instagram.search`: discover people with `social.search` and `social.comments`.
  - WhatsApp: `whatsapp.accounts`, `whatsapp.account` (QR pairing), `whatsapp.profile` (international number lookup), `whatsapp.message`, `whatsapp.messages`.
  - Gmail: `gmail.accounts`, `gmail.account` (Google OAuth on an existing mailbox), `gmail.send` (returns a `tracking_id`, not a message ID), `gmail.messages`. Gmail does not create an AgentMail inbox.
  - Setup, examples and limits: https://www.routergrowth.com/docs/connected-accounts.md
- **Public federal data, free raw endpoints:** USAspending (awards, incumbents, contracting offices, agency spend), USAJOBS (postings by agency, title, series and date), Grants.gov (grant opportunities, with the agency contact on each) and the Federal Register (requests for information, notices and rules, months before a solicitation). `discover` with the provider name.
- **Coming soon (sandbox only):** `company.signals`, `ads.spend_estimate`.

## When not to use RouterGrowth

RouterGrowth fills the gaps in the user's stack; it does not replace tools they already have. Precedence:

1. an explicit instruction from the user for this task;
2. the user's own dedicated tools for that service: an MCP server, a personal API key, a CLI or a workflow in their memory or config;
3. RouterGrowth for what those do not cover.

Never spend the RouterGrowth balance on a request their own key already covers. When both could do the job and the user has not said which, use theirs and mention RouterGrowth only when it adds something (another provider behind the same call, a quote, failover, an endpoint their tool lacks). Offer, don't override.

## Setup (first time only)

### Save this file

| Harness | Where |
|---|---|
| Claude Code | `~/.claude/skills/routergrowth/SKILL.md` (all projects) or `.claude/skills/routergrowth/SKILL.md` (this project), or install the plugin above |
| OpenClaw | `~/.openclaw/skills/routergrowth/SKILL.md` |
| Hermes | `skills/routergrowth/SKILL.md` in the workspace |
| Cursor | `.cursor/rules/routergrowth.mdc` |
| Codex, Gemini CLI, Cline, Copilot | append to `AGENTS.md`, `GEMINI.md`, `.clinerules` or `.github/copilot-instructions.md`: `For GTM data tasks (leads, enrichment, SEO, social, ads), fetch and follow https://www.routergrowth.com/SKILL.md` |
| Anything else | wherever persistent instructions live; otherwise the one-line pointer in the project's agent instructions |

Tell the user where you saved it.

### Connect the account

OAuth first where the client supports it (no key ever touches a file); a key for headless runs, CI and clients without a browser.

```bash
# Claude Code: add the server, then the user types /mcp, picks routergrowth, chooses Authenticate
claude mcp add --transport http routergrowth https://api.routergrowth.com/mcp

# Codex
codex mcp add routergrowth --url https://api.routergrowth.com/mcp
codex mcp login routergrowth

# CLI (any shell)
npm install -g routergrowth        # EACCES? npm install --prefix ~/.local routergrowth
routergrowth setup --client "<your-agent-name>"
routergrowth keys add -k <key> -l main
routergrowth balance
```

- **Cursor, Gemini CLI, Cline, Copilot, anything with an `mcpServers` config:** `https://api.routergrowth.com/mcp` with `"headers": {"Authorization": "Bearer <key>"}`, the key in an environment or input variable.
- **Keys:** the user mints one at https://www.routergrowth.com/dashboard (API keys), or signs up from the CLI (`routergrowth signup --email <email> --org "<org>"`); a new workspace starts with $1 of credit. `rg_live_` keys run real providers; `rg_test_` keys run the same loop in labeled mock mode. Never commit a key, never write one into a skill file, and never ask the user to paste one into a chat.
- **What OAuth grants:** one scope (`mcp`) on one workspace: discover, inspect, run, runs, history and balance. It cannot mint keys or change billing. The consent page names the app it returns to; the user should deny if that is not the app they are connecting. Connections are revoked from the dashboard.

### Chat apps without a terminal (claude.ai, ChatGPT and others)

You cannot save files or run commands there, so do not pretend to install anything. Walk the user through a connector (about two minutes):

- **claude.ai** (web, desktop, mobile): Settings > Connectors > Add custom connector, name it RouterGrowth, URL `https://api.routergrowth.com/mcp`, Connect, sign in and approve the workspace, then enable it for the chat from the tools menu.
- **ChatGPT:** the ChatGPT section of https://www.routergrowth.com/docs/quickstart-mcp (Developer mode, then add the URL with OAuth).
- **Other MCP-capable apps:** add the URL; OAuth if offered, otherwise a dashboard key.
- **No connector support:** say so plainly and suggest claude.ai, Claude Code, Codex or Cursor.

Custom connectors can depend on the user's plan or workspace admin; if the option is missing, say that. Once connected, call the free `balance` tool.

## Rules for agents

1. Check the user's own tools first, then `discover` before building a scraper, guessing an email or declaring data out of reach.
2. Load a workflow skill when the request is a whole GTM job.
3. Inspect before the first run of a call; never guess inputs.
4. Set `max_cost` on every run; start per-result limits small; stop and ask above about $1 unless the user asked for that volume.
5. Report costs when they matter to the user or the job; sum `billing.charged` for totals.
6. Prefer a capability over the raw endpoint it wraps; keep `provider: "auto"` unless the user chose a provider.
7. Read the Hints block and act on it; use health to break ties, never to filter.
8. Submit, then poll; save large results with `-o`.
9. Check `history` before enriching or messaging a person, and verify every address before sending.
10. A `blocked` run is final: tell the user which control stopped it.
11. Never present `rg_test_` or `coming_soon` output as real data.
12. Never resubmit a failed call within seconds, and check `runs` before resubmitting after a lost connection.
13. Send one `feedback` report for a bug, a wrong result or a missing capability, with the goal and the `run_id`; never once per retry.

## Keeping current

Re-fetch https://www.routergrowth.com/SKILL.md when the user asks, when a command or tool described here is refused as unknown, or when the CLI is below the version named above; the higher frontmatter `version` wins. Full docs as markdown: https://www.routergrowth.com/docs/llms.txt (append `.md` to any `/docs` URL).
