---
name: routergrowth
version: 0.4.0
description: >-
  RouterGrowth is the OpenRouter for GTM: one API that routes GTM data
  calls (SEO/SERP, contact and company enrichment, company signals, social and
  ads data, image and video generation) across curated providers, pay per
  call, one balance, plus every provider's own API as raw endpoints. Use this
  skill when the user asks for GTM data endpoints, lead enrichment,
  subreddit or channel research, brand monitoring, ad creatives, or mentions
  routergrowth.
---

# RouterGrowth

**The OpenRouter for GTM.** OpenRouter routes model calls: one key, every model, pay per token. RouterGrowth is the same pattern one layer over, for the GTM calls an agent or a team makes: one key, pay per call, everything you need to grow the company you work for.

**One API for everything GTM, data and creation alike.** You (the agent) discover a capability, inspect its schema and exact price, run it, and the call settles against one prepaid balance. RouterGrowth chooses and contracts the providers, meters every call, and normalizes the output. The catalog covers GTM data (SEO, enrichment, signals, social, ads) and creative generation, live on fal: images, edits, upscales, cutouts and short-form video. GTM runs on content, and making it is part of the job, not a separate stack.

**Two tiers, one front door.** Capabilities are the routed product (normalized output, a quote before the run, failover across providers). Underneath sits every provider's own API as raw endpoints, imported from the providers' catalogs (DataForSEO's full live API, thousands of Apify actors, TikHub, Exa, Firecrawl and more), addressed as provider + endpoint, called with the provider's request shape and answered with its payload, settled on the provider's measured cost after the run. `discover` searches both and tells you when a capability wraps the endpoint you found: prefer the capability.

## Installing this skill (when the user says "set up https://www.routergrowth.com/SKILL.md")

You are the agent. Persist this file so it loads in every future session, using whichever location matches your harness:

- **Claude Code**: save this file to `~/.claude/skills/routergrowth/SKILL.md` (all projects) or `.claude/skills/routergrowth/SKILL.md` (this project only).
- **Codex**: append to `AGENTS.md` (or `~/.codex/AGENTS.md` for all projects): `For GTM data tasks (SEO, enrichment, social, ads, leads), fetch and follow https://www.routergrowth.com/SKILL.md`
- **OpenClaw**: save this file to `~/.openclaw/skills/routergrowth/SKILL.md`.
- **Hermes**: save this file to `skills/routergrowth/SKILL.md` in the workspace.
- **Cursor**: save this file to `.cursor/rules/routergrowth.mdc`.
- **Gemini CLI**: append the same one-line pointer to `GEMINI.md`.
- **Cline**: append the same one-line pointer to `.clinerules`.
- **GitHub Copilot**: append the same one-line pointer to `.github/copilot-instructions.md`.
- **Anything else**: save this file wherever your persistent instructions or skills live; if there is no such place, add the one-line pointer to the project's agent instructions file.

## No terminal or file system? (claude.ai, ChatGPT, Gemini, Copilot and other chat apps)

You cannot save this file or run commands here, so do not pretend to install anything. RouterGrowth works in this chat through a connector, a one-time setup of about two minutes. Walk the user through it step by step:

- **claude.ai** (web, desktop, mobile): Settings > Connectors > Add custom connector. Name it RouterGrowth, URL `https://api.routergrowth.com/mcp`. Click Connect, sign in to RouterGrowth and approve the workspace. Then turn it on for this chat from the tools menu.
- **ChatGPT**: follow the ChatGPT section of https://www.routergrowth.com/docs/quickstart-mcp (Settings > Security and login > Developer mode, then Plugins: add `https://api.routergrowth.com/mcp` with OAuth, sign in, approve the workspace, and add RouterGrowth from the tools menu in a new chat).
- **Any other app that supports MCP connectors**: add `https://api.routergrowth.com/mcp`; pick OAuth if offered, otherwise an API key from https://www.routergrowth.com/dashboard.
- **No connector support**: say so plainly and suggest claude.ai, Claude Code, Codex or Cursor.

Custom connectors can depend on the user's plan or workspace admin; if the option is missing, say that. Never ask the user to paste an API key into the chat. Once connected, call the free `balance` tool to confirm.

After installing: confirm where you saved it. Check for an available authenticated RouterGrowth MCP connection or existing CLI/environment credentials before asking for a key. Verify access with the free `balance` tool or `routergrowth balance` without displaying credentials. If no authentication is available, offer the OAuth connection first (see "Connecting the account" below): in Claude Code and Codex it is one command plus a browser sign-in, and no key ever touches a file. Otherwise let the user configure an existing valid API key with `routergrowth keys add -k <key> -l main`. They can create a key at https://www.routergrowth.com/dashboard under API keys if they do not have one. Never commit the key to the repo.

## Authentication across conversations

Installing this skill provides instructions; it does not authenticate the user's account. A key saved in a temporary or isolated chat environment may be unavailable in a new conversation or workspace. The key itself is not invalidated by starting a new chat. Do not ask for a "fresh" key merely because none is configured in the current environment, and do not claim credentials persist unless the host provides persistent storage.

Prefer an existing authorized MCP connection when available. For ChatGPT / Work, guide the user through the ChatGPT section of https://www.routergrowth.com/docs/quickstart-mcp: connect `https://api.routergrowth.com/mcp` using OAuth, sign in to RouterGrowth, and approve the intended workspace. That connection can be reused across chats, though it may need to be selected in a new chat or reauthorized if expired or revoked. Custom MCP availability depends on the account and workspace policy. If unavailable, use the user's existing valid key through the environment's supported credential configuration. Keep credentials out of skill files, shared documents, and chat memory.

## Connecting the account

The MCP server at `https://api.routergrowth.com/mcp` authenticates with OAuth 2.1 (PKCE, dynamic client registration) or with an API key in the Authorization header. Both reach the same workspace and wallet. Offer OAuth first where the harness supports it; fall back to a key for headless runs, CI, or clients that cannot open a browser.

- **Claude Code**: run `claude mcp add --transport http routergrowth https://api.routergrowth.com/mcp` (no header), then tell the user to type `/mcp`, select routergrowth and choose Authenticate. Their browser opens the RouterGrowth consent page; they sign in (password, Google, GitHub, or an emailed code, same as the dashboard) and approve a workspace. The token is stored by Claude Code and refreshed silently. With a key instead: append `--header "Authorization: Bearer <key>"`.
- **Codex**: run `codex mcp add routergrowth --url https://api.routergrowth.com/mcp`, then `codex mcp login routergrowth` opens the same consent page. With a key instead: `codex mcp add routergrowth --url https://api.routergrowth.com/mcp --bearer-token-env-var ROUTERGROWTH_API_KEY` and have the user export that variable.
- **claude.ai and ChatGPT**: the user adds the URL as a connector (Customize > Connectors in claude.ai; Developer mode > Plugins in ChatGPT) and picks OAuth. Walk them through it with the steps under "No terminal or file system?" above; you cannot do it for them.
- **Cursor, Gemini CLI, Cline, Copilot, anything with an `mcpServers` config**: the URL with `"headers": {"Authorization": "Bearer <key>"}`; keep the key in an input variable or environment variable, never in a committed file.
- **No MCP at all** (OpenClaw, Hermes, a plain shell): `routergrowth keys add -k <key> -l main` for the CLI, or the Bearer header on `https://api.routergrowth.com/v1`.

What the OAuth flow looks like, so you can explain it: the client gets a 401 from `/mcp`, reads `/.well-known/oauth-protected-resource`, registers itself, and opens `/oauth/authorize` with a redirect back to itself (a localhost port for terminal clients). The consent page names that return host; the user should deny if it is not the app they are connecting. The token grants one scope, `mcp`, on one workspace: discover, inspect, run, runs, history and balance. It cannot mint keys or change billing. After connecting, confirm with the free `balance` tool. The user can revoke any connection from the dashboard or `DELETE /v1/connected-apps/{id}`.

## Getting a key

Self-serve. Sign up on https://www.routergrowth.com/dashboard or from the CLI (`routergrowth signup --email <email> --org "<org>"`): the workspace starts with $1 of credit and the first calls cost a fraction of a cent. `rg_live_` keys run on real providers; `rg_test_` keys run the same loop (quote, reserve, settle) in clearly labeled mock mode. Never present mock-mode data as real data. `/v1/discover` returns `status` per capability; a coming-soon capability answers from the sandbox only.

## The CLI (preferred for agents)

```bash
npm install -g routergrowth
# EACCES from a global install? Use a per-user prefix instead:
#   npm install --prefix ~/.local routergrowth
#   ln -sf ~/.local/node_modules/.bin/routergrowth ~/.local/bin/routergrowth

routergrowth setup --client "<your-agent-name>"
routergrowth keys add -k <the user's key> -l main      # or: routergrowth signup --email <email> --org "<org>"
routergrowth balance
routergrowth discover -q "find a verified email for a person"          # capabilities and raw endpoints, ranked, with hints
routergrowth inspect -c contact.find
routergrowth run -c contact.find -i '{"first_name":"Alex","last_name":"Rivera","company_domain":"example.com"}' --max-cost 0.10
# run submits immediately; poll only when you need the result now:
routergrowth runs get -r <run_id> --wait 60 -o result.json
routergrowth discover -q "tiktok video comments" --kind endpoint       # the long tail: one provider's own endpoint
routergrowth inspect -p dataforseo -e /v3/serp/google/organic/live/advanced
routergrowth run -p dataforseo -e /v3/serp/google/organic/live/advanced -i '{"keyword":"best crm"}' --max-cost 0.05 -o serp.json
routergrowth endpoints -p dataforseo -q backlinks                      # everything one provider serves raw
routergrowth runs                                   # recent runs; runs get <id> --wait 60 polls a slow one; runs stop <id> cancels a queued one
routergrowth history alex.rivera@example.com        # everything already done to this subject (email, domain, LinkedIn URL, handle, name): touches, results to reuse. Free
routergrowth history --file leads.txt               # one identifier per line: seen / contacted / reusable, the dedupe pass before a batch
routergrowth guard --daily 25                       # daily spend cap; guard --per-run 1 blocks any single run holding more than $1
```

The CLI prints plain text with no colors and never prompts interactively, so you can drive it directly. `run` submits immediately by default and returns a compact receipt; add `--wait` (or `--wait 60`; `--wait 120` for Apify-backed capabilities such as `social.*` and `people.search`, which often take over a minute) only when blocking is appropriate, then use `runs get -r <run_id> --wait 60 -o result.json` to poll without flooding the conversation. Always run `inspect` and show the user the price before a billable `run`; use `--max-cost` to cap any call; write large results to a file with `-o`.

The user can see the same state in a browser at https://www.routergrowth.com/dashboard (balance, keys, runs, usage, scoped to their key); still report prices and balances in the conversation yourself (`routergrowth balance`, `routergrowth runs`).

## The HTTP interface (same contract as the CLI)

Base URL: `https://api.routergrowth.com/v1` · Auth: `Authorization: Bearer rg_live_...` (or `rg_test_...`)

1. `POST /v1/discover` with `{"query": "find a verified email for a person"}`: returns candidate capabilities. Free, never executes a paid call.
2. `POST /v1/inspect` with `{"capability": "contact.find"}`: returns the input schema, the providers behind it, the exact versioned price and the billing conditions. Free.
3. `POST /v1/run` with the capability, your input, and `"routing": {"provider": "auto", "strategy": "best_value", "max_cost": "0.10"}`. Send an `Idempotency-Key` header. The maximum billable amount is reserved first, then settled to the actual charge; failures and no-matches release the hold. On auto routing the router waterfalls: if a provider errors, times out, or finds no match (on capabilities that don't bill unmatched calls), the next-best provider is tried automatically, up to 3 attempts: only the provider that delivers is charged, every attempt appears in the response's `attempts` array, and `max_cost` caps each attempt. Keep `provider: "auto"` unless the user deliberately requests a provider. Pinning any provider disables cross-provider fallback even with `allow_fallback: true`. Set `"allow_fallback": false` to disable fallback entirely.
   Runs execute on the router's worker. The request waits up to `wait_seconds` (default 30, max 120) and answers 200 with the finished run, or 202 with a queued/running run: poll `GET /v1/runs/{run_id}?wait=60` until `done` is true. Send `"async": true` to get the 202 immediately. Slow capabilities (creative.video takes 1 to 4 minutes, people.search with a large limit) always need the poll. `POST /v1/runs/{run_id}/cancel` stops a run that is still queued (`stoppable` is true); a run already at the provider cannot be stopped and settles or releases on its own.
4. `GET /v1/wallet` and `GET /v1/runs` for balance and history.
5. Spend guard: `GET /v1/spend-guard` shows the organization's daily cap (UTC day), the optional per-run ceiling and today's spend; `POST /v1/spend-guard {"enabled": true, "daily_limit": "25", "per_run_limit": "1"}` sets them. When a control stops a run it ends as `status: blocked` (error `budget_exceeded` or `cost_limit_exceeded`, a `controls` list naming the control) and nothing is charged; tell the user, do not retry until they change the control or the day resets (`resets_at`).
6. Watches, for anything you will ask again: `POST /v1/watch` with the same body as run plus a `name` saves the query and runs it once; `POST /v1/watch/{id}/refresh` reruns it (billed like a run) and answers with only the new and changed records plus the keys that disappeared. Records key on their own identity (a posting's URL, a LinkedIn URL, an award id, a USAJOBS control number); ranking fields do not count as changes. One watch per office, contractor, keyword or search, one refresh per week: the delta is free, the query costs what it costs. Full page: https://www.routergrowth.com/docs/api/watch.md
7. Raw endpoints: `POST /v1/discover` returns them next to capabilities (`kind: "endpoint"`, with `provider`, `endpoint`, `cost`, `health`, `wrapped_by`); `POST /v1/inspect {"provider": ..., "endpoint": ...}` returns the provider's own input spec (`pathParams`, `queryParams`, `body`, `bodyType`), the cost model and a ready `run.cli`; `POST /v1/run {"provider": ..., "endpoint": ..., "input": {...}, "path": {...}, "query": {...}, "routing": {"max_cost": "0.05"}}` executes it. There is no quote: the wallet holds the rate-card estimate with headroom (or $1 when there is none, lowered by `max_cost`), then settles on the provider's measured cost, never above the hold. Provider errors release the hold. `result.data` is the provider's payload untouched. Full page: https://www.routergrowth.com/docs/api/endpoints.md

### Prices and spending limits

Always show the user the `/v1/inspect` price before running anything billable. Inspect's headline is the starting price; per-result capabilities quote a base plus a per-result rate, and some platforms cost more than the headline. A `402 cost_limit_exceeded` names the actual quote: lower the limit or, within the user-authorized budget, raise `max_cost` to it and rerun, and treat the quote as the number to show the user. A per-result capability holds the requested limit and bills the results returned, so fewer results cost less; keep limits honest, since the hold must fit the balance and `max_cost`. Page-priced capabilities cost the same page for 3 results as for 25: `people.search` on the LinkedIn route is $0.175 a page of 25 plus $0.007 a requested full profile, plus a lookup allowance of up to $0.035087 per employer when company-constrained (25 full profiles at one employer quote $0.385087 at list price). Ask for 25 only when you will use them; use a small limit for a few leaders and narrow with `titles`, `company_domains` and necessary `locations`. Successful LinkedIn searches retain the requested-limit billing floor even after unsuitable rows are filtered; unresolved or empty attempts release the hold. For the leaders of a known company, pass the company with a small `limit` instead (`company_domains` is precise; a name in `companies` works when only one company carries it): $0.042 a person actually returned, with a work email when available.

### Choosing a lookup

To locate a named person or their email, call `person.enrich` or `contact.find`, never `web.search` with the name: a search returns pages, not an email, and one run spent 115 searches that way. Government staff are findable: run `contact.find` with the domain of the office the person sits in (a member's own domain, the committee's, the agency's); a miss is free. Measured on real runs: House and Senate staff match 3 times in 4, better than company staff; agency staff a little under half. When it misses, take the point of contact printed on the notice or agency page and `contact.verify` it ($0.011); .mil coverage is thinner.

### Fallback and retries

`max_cost` also decides which fallback providers the router may try: on an unbilled no-match or provider failure, the error names budget-excluded alternatives and their input-specific minimum cap when available. Retry with a higher cap only within the user-authorized budget. Pinning a provider disables fallback even with `allow_fallback: true`. The router already retries a rate-limited or 5xx provider once after a short wait; never resubmit a failed call within seconds. Values outside a field's allowed list (`inspect` prints them) are refused before routing. Google search operators (`site:`, `inurl:`) are billed at five times the price and not reliably honoured; use plain phrases.

### Batch accounting and limits

Total a job by summing each run's `billing.charged`; the wallet balance is shared by every session on the key and is not a receipt. If the CLI loses its connection while waiting, the run continues on the router; `routergrowth runs` lists it and `runs get` fetches it, so check before resubmitting; inspect once for a homogeneous batch, not once per item. Respect `max_cost` (on a raw endpoint it is the only price control before the run: set it every time), keep first-call limits small on per-result providers (Apify actors bill per item and `maxItems` often applies per query, not per call), and stop and ask when a batch would exceed about $1 unless the user explicitly requested that volume and you use `batch_run` with `max_total_cost`. A request such as “do 50” authorizes 50 items within the surfaced total cap; do not ask again between items. Read the `hints` block discover and inspect return: it says which capability wraps an endpoint, and what to try when nothing matched. Health (`healthy`, `stable`, `degraded`, `outage`, `unknown`) breaks ties between two options that both fit; never skip an option because it is `unknown`, that usually means low traffic.

### Lead-list workflow

1. **Discover companies when needed.** If you have targeting criteria but no employer list, discover company domains first. Check each required criterion (industry, headcount, technology, geography) against supporting data. A generic company search is a candidate source, not proof of those criteria. Preserve the original requirements when changing sources; mark unsupported criteria as unknown instead of silently weakening them.
2. **Choose the route.** Prefer `provider: "auto"`. Apollo needs known companies or preview `person_ids`; it cannot serve a broad title/industry-only people search. Broad people discovery can use another eligible route within budget. Raw endpoints require a provider and do not offer fallback.
3. **Search roles.** Start `people.search` with the employer's `company_domains` and the `titles` you need. If you also supply `companies` (names or exact LinkedIn company URLs), pair the arrays in the same order; one company per request is easiest to review. Prefer `detail: "full"` for a usable role list. A company name alone can match several businesses. Include equivalent title spellings in the first query, such as "VP Engineering" and "Vice President of Engineering". Directors are a broader seniority choice, not a synonym for CTO. Keep the domain constraint when broadening titles; add a location only when it is a real requirement, because remote employees may live elsewhere.

4. **Review the evidence.** The LinkedIn route resolves employer identity before searching, checks each profile's current employer ID or URL, and selects the requested-company role even when the person has other jobs. Review `current_positions`, `company_linkedin_url` and `quality_flags` (especially `retirement_mentioned` and `missing_current_title`); `result.quality` reports raw and excluded profile counts. These fields are route-specific and are not guaranteed on database-route results. Employer matching reflects the profile's evidence, not independent employment verification or buyer qualification. A no-match can mean insufficient employer evidence: check domain spelling, try the exact LinkedIn company URL, or relax titles/location without dropping the employer. Do not repeat the identical miss immediately.

5. **Recover within budget.** Broaden equivalent titles once and remove only optional filters. Read the run's `hints`, error and `attempts`: a pinned provider never falls back; `auto` still needs a cap covering an alternative's complete quote. A $0.042 cap can allow a single database result but excludes a company-constrained LinkedIn full-profile search (one profile at one employer quotes $0.217087 at list price). Use inspect and the returned quote guidance; do not raise a user-set budget without authorization. A higher cap permits another attempt; it does not guarantee a match.

6. **Complete the contact.** The LinkedIn route does not enrich emails. Call `contact.find` only for selected profiles missing an email, using their real first/last names and the matched employer's domain; never guess surnames from initials. Database-route results may already include a work email, so skip the redundant lookup and use `contact.verify` on that address. LeadMagic enriches known people; it does not source an ICP list.

7. **Report coverage honestly.** Separate company candidates, qualified companies, matched people, found emails and verified emails. Never label a list verified because a search succeeded. Report each item's provider, result, charge, run ID and fallback attempts, plus the batch total. See [the worked people-search guide](https://www.routergrowth.com/docs/people-search.md).

## When NOT to use RouterGrowth

RouterGrowth fills the gaps in the user's stack; it does not replace tools they already have. Precedence: (1) an explicit instruction from the user for this task; (2) the user's own dedicated tools: an MCP server, a personal API key, a CLI or a workflow in their memory or config for that service (a personal SEO-tool key, a scraping MCP); (3) RouterGrowth for what those do not cover. Runs spend the user's RouterGrowth balance; never spend it on a request their own key already covers at no extra cost. When both could do the job and the user has not stated a preference, use their tool and mention RouterGrowth as an alternative only when it adds something (a second provider behind the same name, a quote, failover, a raw endpoint their tool lacks). Offer, don't override.

Prefer MCP? Connect `https://api.routergrowth.com/mcp` (Streamable HTTP): `discover`, `inspect`, `run`, `batch_run`, `runs`, `get_run`, `history` and `balance` as native tools, same contract as above. `batch_run` submits 1–200 homogeneous inputs concurrently and returns individual receipts plus aggregate cost. Claude Code, Codex, claude.ai and ChatGPT connect with OAuth (add the URL with no key, sign in once in the browser); other clients, CI and headless agents send a key in the Authorization header. Commands per harness are in "Connecting the account" above.

Full documentation, agent-readable: https://www.routergrowth.com/docs/llms.txt indexes every docs page (quickstarts, API and CLI reference) as raw markdown; append `.md` to any /docs URL for the raw page.
Catalog (capabilities before vendors): https://www.routergrowth.com/catalog
Live on real providers today: `contact.find`, `contact.verify`, `contact.phone`, `company.funding`, `seo.serp` (Google, Bing), `seo.keywords`, `seo.backlinks`, `seo.domain_overview`, `seo.ranked_keywords`, `seo.competitors`, `seo.page_audit`, `company.technologies`, `aeo.answer` (ChatGPT, Claude, Gemini, Perplexity with citations), `local.places` (Google Maps), `news.search` (Google News), `social.profile`, `social.posts`, `social.search`, `social.comments` (X, LinkedIn, Reddit, Instagram, TikTok, YouTube; a profile carries the bio link, the person's own domain with link hubs excluded, and a public email when the profile exposes one, which is how a creator or local-business handle becomes a `contact.find` input), `reviews.search` (Google Maps, Yelp), `ads.search` (Meta Ad Library, Google), `web.search`, `web.scrape`, `web.extract` (one page in, dated records out against a template: leadership page, official bio, org chart, press release, job posting, or your own schema; each record carries the page's supporting line, date and URL), `people.search` (build a people list from titles, seniority, headcount, location), `company.jobs` (hiring signals), `company.search`, `person.enrich`, `local.places`, `aeo.keywords` (AI search volume), `aeo.mentions` (where a domain appears in AI answers). Outbound email, live on Name.com and AgentMail: `domain.search`, `domain.register`, `domain.dns`, `email.domain` (verify a domain you own for sending), `email.inbox` (an inbox on that verified domain; no shared-domain inboxes; with inbox_id + display_name it renames an inbox you own, free, which is how you change the From name, there is no per-email override), `email.inboxes` (free: the domains and inboxes the workspace already owns, with inbox_id; run it before creating or sending), `email.send`, `email.messages`. LinkedIn, live on Unipile: `linkedin.accounts` (free: how many accounts the workspace has connected, which profile each one is, and the name to pass as account_id; run it before connecting or sending), `linkedin.account` (connect once on a hosted sign-in; without a name it reports what is already connected), `linkedin.search`, `linkedin.profile`, `linkedin.invite`, `linkedin.message`, `linkedin.messages`. Instagram, live on Unipile on the same hosted sign-in: `instagram.accounts` (free: what is connected and the name to pass as account_id), `instagram.account` (connect once; without a name it reports what is connected), `instagram.profile` (bio, links with the person's own domain resolved, business email and phone when exposed, whether they follow you, and the messaging_id a DM needs), `instagram.message` (a DM to a handle or a reply in a thread; a first message to a non-follower lands in their requests folder; about 100 actions a day per account), `instagram.messages` (read the inbox and threads). There is no instagram.search: discovery is `social.search` and `social.comments`. WhatsApp via Unipile: `whatsapp.accounts`, `whatsapp.account` (hosted QR/pairing connection), `whatsapp.profile` (international phone number lookup), `whatsapp.message` (text to a phone/provider_id or reply by chat_id), `whatsapp.messages` (conversations and threads). Gmail via Unipile: `gmail.accounts`, `gmail.account` (connect an existing Gmail or Google Workspace mailbox through Google OAuth), `gmail.send` (to/cc/bcc, text or html, in_reply_to from gmail.messages), `gmail.messages` (list/search/read emails). These connected accounts use the same monthly seat billing as LinkedIn/Instagram. Gmail does not create an AgentMail inbox: use email.inbox for that. Run the channel's .accounts first; pass account_id when multiple accounts exist. Sends need user authorization and an Idempotency-Key. Gmail sends return tracking_id, not an email message_id. See https://www.routergrowth.com/docs/connected-accounts.md for setup, examples, billing and limitations. Creative, live on fal: `creative.image` (flux-schnell, flux-pro, flux-pro-ultra, nano-banana, recraft-v3), `creative.image_edit` (nano-banana-edit, flux-kontext), `creative.upscale`, `creative.remove_background`, `creative.video` (hailuo-02, kling-2.5, kling-2.1, wan-2.2, veo3-fast, veo3). Public federal data, free on raw endpoints: USAspending (awards, incumbents, contracting offices, agency spend) and USAJOBS (open and closed federal postings by agency code, title, series and date, plus the agency code list): `discover` with the provider name. Coming soon (adapter or provider account pending; sandbox mock only): `company.signals`. `/v1/discover` returns `status` per capability; never present a coming-soon capability's sandbox output as real data.

## Playbooks you can run today (no key needed)

RouterGrowth's strategy playbooks, free, runnable with whatever data access you already have. Ground rules: never fabricate, every number needs a source URL or an explicit "estimate" label; these playbooks measure and map, they never post, comment or automate engagement anywhere (platforms ban it; if the user asks for automated posting, decline).

### 1 · AI visibility audit (about an hour)

1. Build a panel of 15–20 buyer questions in four groups (category, comparison, problem, brand-direct), phrased the way a buyer talks to an assistant. Freeze the panel and save it; the value is re-running the same questions monthly.
2. Run the panel across the answer surfaces you can reach (your own web search, SERP checks). Also answer each question cold from your own knowledge and record that as a separate "model prior" column. Log verbatim brand mentions and every cited source.
3. Map the sources: list cited domains by frequency and flag the specific Reddit threads and comparison pages carrying the category.
4. Score competitors on the same panel. Share of voice = the brand's mentions divided by all brand mentions on the panel.
5. Report gaps as absent, wrong, or fragile, each with a next action.

### 2 · Reddit surface map (about 30 minutes)

1. List 10–20 money queries (best X, X vs Y, X alternatives, and problem phrasings).
2. For each, find the Reddit threads ranking in the top results (append the word "reddit" to the query; a `site:` operator is not honoured and costs five times more). Record thread URL, subreddit, and age.
3. Roster the subreddits: read each one's rules, note vendor tolerance and posting norms.
4. Deliver the map: subreddit, why it matters, rules risk, target threads. Never auto-post anything.

### 3 · Brand mention sweep (about 20 minutes)

1. Terms: brand, product, founder, top competitors, category phrase.
2. Sweep Reddit and the web for mentions from the last 90 days. Record URL, date, and sentiment (positive, neutral, negative, question).
3. Flag the threads where an honest reply would matter and draft talking points for a HUMAN to post.

## When you finish a playbook

Hand the user the report plus the honest limit: you measured and mapped; every number carries its source or an "estimate" label. Machine-readable summary of RouterGrowth: https://www.routergrowth.com/llms.txt

## Workflow skills built on this one

Complete GTM jobs, each a skill of its own, open source at https://github.com/RouterGrowth/skills (Claude Code: `claude plugin marketplace add RouterGrowth/skills`; other agents: `npx skills add RouterGrowth/skills`): hiring-signal-outbound, social-lead-discovery, cold-email-pipeline, sdr-daily, linkedin-outbound, ai-visibility-audit, reddit-surface-map, brand-mention-sweep, community-help-drafts, ad-creative-batch. When the user's request matches one of those jobs, load that skill and run it; the rules in this file still apply.

## Keeping current

Re-fetch https://www.routergrowth.com/SKILL.md from time to time and compare the frontmatter version; newer wins.
