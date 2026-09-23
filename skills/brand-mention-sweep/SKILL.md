---
name: brand-mention-sweep
description: >-
  Sweep every public mention of a brand, product, founder and competitors from
  the last 90 days with RouterGrowth: social platforms (social.search across X,
  Reddit, LinkedIn, TikTok, YouTube, Instagram), news (news.search), the open
  web (web.search) and review sites (reviews.search). Records URL, date,
  platform, sentiment and whether a human reply would matter, and drafts the
  talking points. Use when the user asks "who is talking about us", wants brand
  monitoring, a mention report, competitor mention tracking, or wants to find
  threads where they should reply.
---

# Brand mention sweep

Twenty minutes of calls that replace a monitoring subscription for a brand that does not need one yet. Terms in, a dated mention table out, with the threads where a human reply would matter and the talking points for it.

## Before you start

- Load the core `routergrowth` skill (https://www.routergrowth.com/SKILL.md) if it is not loaded. Confirm access with the free `balance` tool or `routergrowth balance`.
- Ask for: the brand and product names (and the misspellings people use), the founder's name and handles, three to five competitors, the category phrase, and the window (default 90 days).
- Inspect `social.search`, `news.search`, `web.search` and `reviews.search` once and show the prices. Social search is priced per platform: X $0.0006 a post, LinkedIn $0.003, Reddit $0.0021; the hold covers the limit and the charge covers the posts returned. Quote the sweep: terms x platforms, with Reddit counted at $0.021 a term at a limit of 10.

## Steps

### 1. Terms

Brand, product, founder, each competitor, the category phrase. For each, the exact string and the common variants. Save the list; the sweep is worth repeating monthly with the same terms.

### 2. Social

```bash
routergrowth run -c social.search -i '{"platform":"x","query":"RouterGrowth","limit":25}' --max-cost 0.02 --wait 60
routergrowth run -c social.search -i '{"platform":"linkedin","query":"RouterGrowth","limit":10}' --max-cost 0.05 --wait 120
routergrowth run -c social.search -i '{"platform":"reddit","query":"RouterGrowth","limit":10}' --max-cost 0.15 --wait 120
```

Run each term on `x`, `reddit` and `linkedin` first; `tiktok`, `youtube` and `instagram` when the brand has a consumer side. Reddit and LinkedIn runs often pass 60 seconds: poll a still-running receipt with `runs get -r <run_id> --wait 60 -o file`. Quotes in the query are not honoured, so search the bare term and match it in the text yourself. For a generic competitor name (Clay), search the domain or the name with the category word, or the results are pottery. No platform takes a date range: rows carry `created_at` as ISO 8601 UTC, filter on it after the call. Keep: URL, platform, date, `author` (a display name) and `author_handle` when the platform returns one, the sentence with the mention, engagement counts (null on Reddit rows). An empty search comes back as `no_match`, released, not billed.

### 3. News and web

```bash
routergrowth run -c news.search -i '{"query":"RouterGrowth","limit":50}' --max-cost 0.05 --wait 30
routergrowth run -c web.search -i '{"query":"\"RouterGrowth\" -site:routergrowth.com","limit":50}' --max-cost 0.05 --wait 30
```

Web search catches the blog posts, comparison pages, directories and forum threads that social search misses. Search operators are not honoured by the results (`-site:` and quotes are ignored, and a `site:` operator is billed at five times the price), so search the bare term and drop the brand's own domains afterwards. Web rows carry no date; about half the snippets start with one (a date such as "Sep 3, 2026" followed by a dash), parse it when present. A news search with nothing behind it comes back as `no_match`, released, not billed; a `failed` run is a provider fault, retry it once. Ten X posts cost under a cent when this was written.

### 4. Reviews

```bash
routergrowth run -c reviews.search -i '{"place":"<Google Maps URL or place ID (ChIJ...), or a Yelp business URL>","limit":50}' --max-cost 0.20 --wait 120
```

For brands with a physical presence or a Google Business Profile. Skip otherwise. `place` is a Google Maps URL, a place ID or a Yelp business URL, and the platform is inferred from it; a business name fails at the provider. The provider occasionally fails a run outright; a failed run is released, so retry it once before reporting a gap.

### 5. Classify

First split own from third-party: posts and pages by the brand, its founder or its own domains are `own` and are counted separately, so the totals say how many other people talked. For each third-party mention: sentiment (positive, neutral, negative, question), type (recommendation, complaint, comparison, question, news), and whether a human reply would matter (a question with no answer, a wrong claim, a comparison where the brand is missing, a complaint). Filter the window to the last 90 days by the mention's own date, not the crawl date.

### 6. Talking points

For every thread flagged as reply-worthy: what the thread says, what a truthful reply would add, and the disclosure line ("I work at ..."). A human posts, or does not.

## Rules

- Never post, reply, vote or engage anywhere. Draft for a human.
- Every mention carries its URL and date. Sentiment is your reading and is labelled as such; quote the sentence so the user can disagree.
- Do not compile personal information beyond the public mention itself. Handles and names stay as they appear in the public post; nothing is enriched from here.
- Every count is from a run and carries the run ID.

## Output

`mentions-<date>.csv` (run ID, URL, platform, date, author, handle, term matched, own or third-party, sentiment, type, reply-worthy, quote) and `mentions-report-<date>.md`: totals per term and platform with own posts separated, sentiment split, the competitor comparison, the reply-worthy threads with talking points, and the total charged as the sum of every run's `billing.charged` (not a wallet difference: the balance is shared by every session on the key). Date the file names, so next month's sweep diffs against them.
