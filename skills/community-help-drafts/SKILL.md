---
name: community-help-drafts
description: >-
  Find the Reddit and X conversations where the user can answer a real question
  in their field, and draft the reply for them to post, with RouterGrowth doing
  the search (social.search, social.comments, seo.serp) and the agent doing the
  reading and writing. Help first, product mention only when it materially
  improves the answer, affiliation always disclosed, nothing ever posted by the
  agent. Use when the user wants to build presence on Reddit or X without
  spamming, asks "where should I be answering questions", wants a daily list of
  threads to reply to, or wants community marketing drafts.
---

# Community help drafts

A daily list of conversations where an honest, expert answer from the user would be welcome, each with a draft they can post. The agent searches, qualifies, checks the community's rules and writes. The user reads, edits and posts. The agent never posts, replies, votes, follows or messages anyone.

## Before you start

- Load the core `routergrowth` skill (https://www.routergrowth.com/SKILL.md) if it is not loaded. Confirm access with the free `balance` tool or `routergrowth balance`.
- Ask for, once, and keep in `community/config.md`: the user's field of expertise in one line, the product (if any) and the one-sentence disclosure they will use ("I work on X"), the three question groups to search (see below), and the platforms (Reddit, X, or both).
- Keep a local log at `community/log.csv`: permalink, date found, classification, status (drafted, posted by user, skipped, closed), and the draft. Every run reads it first.
- Inspect `social.search`, `social.comments` and `seo.serp` once and show the prices. A daily cycle is small: quote it once and reuse the quote until prices change.

## Daily caps

Per cycle, across both platforms: inspect at most 20 new search results, read at most 10 threads in full, keep at most 5 qualified opportunities, prepare at most 2 drafts, of which at most 1 mentions the product. Stop searching once 2 strong drafts exist. Zero drafts is a valid outcome when nothing fits; say so rather than lowering the bar.

Over any rolling 10 posted contributions, at least 7 should be help-only and at most 3 may mention the product. A community's own rules override that ratio and may require zero mentions.

## Steps

### 1. Monitor first

Before any new search, revisit every thread in the log the user posted in during the last 7 days:

```bash
routergrowth run -c social.comments -i '{"url":"<permalink>","limit":100}' --max-cost 0.05 --wait 60
```

Detect new replies to the user, follow-up questions, moderation, deletion or locking. Draft a response only when someone replied to the user directly, asked a relevant follow-up, a material misunderstanding needs correcting, or a new development makes a short answer useful. Never draft to keep a thread alive. Close a thread after 7 days without activity. If a thread cannot be checked, mark it unknown and say so; unknown is not "no change".

### 2. Search the three question groups

Only high-intent conversations, phrased as questions or problems:

1. Explicit requests for a recommendation in the user's field ("what do you use for", "best tool for", "alternatives to").
2. Explicit complaints about a problem the user knows how to solve.
3. Builders implementing something in the field and asking a concrete implementation question.

```bash
routergrowth run -c social.search -i '{"platform":"reddit","query":"alternatives to clay for enrichment","limit":25}' --max-cost 0.10 --wait 60
routergrowth run -c social.search -i '{"platform":"x","query":"anyone built an AI SDR agent","limit":25}' --max-cost 0.10 --wait 60
```

Recency: X posts from the last 24 hours; Reddit from the last 48 hours, up to 7 days when the thread is still active. Reject generic news, broad commentary, promotional threads, and questions already answered well.

### 3. Qualify

For each candidate, record: platform, permalink, date, the exact excerpt with the question, the community, its visible rules (Reddit: `web.scrape` on the subreddit rules page or your own fetch), whether self-promotion is allowed, and why a reply would add something the thread does not have. Check the log for the same permalink, the same author, or similar wording already used.

Classify: `help_only` (answer, no product), `soft_mention` (answer first, then one disclosed sentence on the product), `direct_fit` (the person asked for exactly what the product does), `reject`.

Reject when self-promotion is banned and the draft would mention the product, the question is already well answered, the thread is political, medical, financial or otherwise sensitive, the reply would need an invented claim, or the user already replied there.

### 4. Draft

Structure: answer the question in the first sentence; one concrete insight, example or workflow; the product only when it materially improves the answer; the disclosure line; a natural ending with no engagement bait.

Do not open with "great question", "I totally agree", "thanks for sharing". Do not end with "thoughts?", "check out my product" or an unneeded link. One link at most, only when the person asked for a resource and the community allows it, never through a shortener.

## Rules

- The agent never publishes anything, anywhere, on any account. The user posts.
- Never hide affiliation, never pose as a customer, never claim the product was found independently, never invent results or testimonials, never attack a competitor, never reuse the same wording across threads.
- Re-read the community's rules before every draft, including follow-ups.
- A moderation warning or a removal is a negative outcome even when the post got traffic. Log it and tighten.

## Output

The daily briefing: threads monitored and what changed, response drafts due, new opportunities kept and rejected with reasons, the 1 or 2 drafts with permalink, classification and the rules note, and the total charged. End with: drafts ready, nothing posted.
