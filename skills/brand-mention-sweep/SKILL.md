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
- Inspect `social.search`, `news.search`, `web.search` and `reviews.search` once and show the prices. Quote the sweep: terms x platforms.

## Steps

### 1. Terms

Brand, product, founder, each competitor, the category phrase. For each, the exact string and the common variants. Save the list; the sweep is worth repeating monthly with the same terms.

### 2. Social

```bash
routergrowth run -c social.search -i '{"platform":"x","query":"\"RouterGrowth\"","limit":50}' --max-cost 0.10 --wait 60
```

Run each term on `x`, `reddit` and `linkedin` first; `tiktok`, `youtube` and `instagram` when the brand has a consumer side. Keep: URL, platform, date, author handle, the sentence with the mention, engagement counts.

### 3. News and web

```bash
routergrowth run -c news.search -i '{"query":"RouterGrowth","limit":50}' --max-cost 0.05 --wait 30
routergrowth run -c web.search -i '{"query":"\"RouterGrowth\" -site:routergrowth.com","limit":50}' --max-cost 0.05 --wait 30
```

Web search catches the blog posts, comparison pages, directories and forum threads that social search misses. Drop the brand's own domains.

### 4. Reviews

```bash
routergrowth run -c reviews.search -i '{"place":"<business name, city>","platform":"google","limit":50}' --max-cost 0.10 --wait 60
```

For brands with a physical presence or a Google Business Profile. Skip otherwise.

### 5. Classify

For each mention: sentiment (positive, neutral, negative, question), type (recommendation, complaint, comparison, question, news), and whether a human reply would matter (a question with no answer, a wrong claim, a comparison where the brand is missing, a complaint). Filter the window to the last 90 days by the mention's own date, not the crawl date.

### 6. Talking points

For every thread flagged as reply-worthy: what the thread says, what a truthful reply would add, and the disclosure line ("I work at ..."). A human posts, or does not.

## Rules

- Never post, reply, vote or engage anywhere. Draft for a human.
- Every mention carries its URL and date. Sentiment is your reading and is labelled as such; quote the sentence so the user can disagree.
- Do not compile personal information beyond the public mention itself. Handles and names stay as they appear in the public post; nothing is enriched from here.
- Every count is from a run and carries the run ID.

## Output

`mentions.csv` (URL, platform, date, author, term matched, sentiment, type, reply-worthy, quote) and `mentions-report.md`: totals per term and platform, sentiment split, the competitor comparison, the reply-worthy threads with talking points, and the total charged. Save both dated, so next month's sweep diffs against them.
