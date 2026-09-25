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
- Keep a local log at `community/log.csv`: permalink, date found, classification, status (drafted, posted by user, skipped, closed), and the draft. Every run reads it first. Both paths are relative to the folder the user names for this work; ask once and record it in the config.
- Inspect `social.search`, `social.comments` and `seo.serp` once and show the prices. X is cents (a 25-post search is $0.0175); Reddit threads are not: a search is $0.0024 a post, but a thread read is $0.07 plus $0.00665 a comment, so ten threads read at a limit of 30 are about $2.70. The hold covers the limit; the charge covers the rows returned, so a limit of 10 that returns 3 bills 3. Quote the cycle once and reuse the quote until prices change.

## Daily caps

Per cycle, across both platforms: at most 6 searches at a limit of 10 (X can take 25), read at most 10 threads at a limit of 30, keep at most 5 qualified opportunities, prepare at most 2 drafts, of which at most 1 mentions the product. Stop searching once 2 strong drafts exist. Zero drafts is a valid outcome when nothing fits; say so rather than lowering the bar. When the strict recency window empties the list, widen it to 7 days once, say so in the briefing, and stop there.

Over any rolling 10 posted contributions, at least 7 should be help-only and at most 3 may mention the product. A community's own rules override that ratio and may require zero mentions.

## Steps

### 1. Monitor first

Before any new search, revisit every thread in the log the user posted in during the last 7 days:

```bash
routergrowth run -c social.comments -i '{"url":"<permalink>","limit":30}' --max-cost 0.30 --wait 120
```

Reddit threads only: `social.comments` does not serve X, and an X URL is refused. For X threads the user posted in, ask them what came back, or read their own handle with `social.posts`. Reddit returns the comments (text, author, upvotes, reply count, time), not the post itself. Detect new replies to the user, follow-up questions, moderation, deletion or locking. Draft a response only when someone replied to the user directly, asked a relevant follow-up, a material misunderstanding needs correcting, or a new development makes a short answer useful. Never draft to keep a thread alive. Close a thread after 7 days without activity. If a thread cannot be checked, mark it unknown and say so; unknown is not "no change".

### 2. Search the three question groups

Only high-intent conversations, phrased as questions or problems:

1. Explicit requests for a recommendation in the user's field ("what do you use for", "best tool for", "alternatives to").
2. Explicit complaints about a problem the user knows how to solve.
3. Builders implementing something in the field and asking a concrete implementation question.

```bash
routergrowth run -c social.search -i '{"platform":"reddit","query":"alternatives to clay for enrichment","limit":10}' --max-cost 0.15 --wait 120
routergrowth run -c social.search -i '{"platform":"x","query":"anyone built an AI SDR agent","limit":25}' --max-cost 0.02 --wait 60
```

Reddit searches often run past 60 seconds: use `--wait 120`, and when the receipt says the run is still running, poll it with `runs get -r <run_id> --wait 60 -o file`. Reddit search matches post text and returns `url`, `text` (the title), `body`, `community`, `author`, `created_at`; expect off-topic rows and a job ad repeated across subreddits, and skip them. Engagement counts are null on Reddit search rows, so activity is judged by reading the thread, not from the row. There is no date parameter on any platform: filter on `created_at` (ISO 8601, UTC) after the call. Recency: X posts from the last 24 hours; Reddit from the last 48 hours, up to 7 days when the thread is still active. Reject generic news, broad commentary, promotional threads, and questions already answered well. Optional: `seo.serp` on a money query with the word "reddit" appended finds the threads that rank (a `site:` operator is not honoured by the results and is billed at five times the price, so do not use one).

### 3. Qualify

For each candidate, record: platform, permalink, date, the exact excerpt with the question, the community, its rules, whether self-promotion is allowed, and why a reply would add something the thread does not have. Reddit blocks crawlers on its rules pages: `web.scrape` comes back as a no-match (released, not billed) and an unauthenticated fetch of `about/rules.json` is refused, so ask the user to paste each subreddit's rules once into `community/config.md` and read them from there. Until the rules of a community are on file, its outcome is `unknown` and a draft for it is help-only with no product mention. Check the log for the same permalink, the same author, or similar wording already used, and run the free `routergrowth history <permalink>` to see whether this workspace already touched the thread.

Classify: `help_only` (answer, no product), `soft_mention` (answer first, then one disclosed sentence on the product), `direct_fit` (the person asked for exactly what the product does), `reject`.

Reject when self-promotion is banned and the draft would mention the product, the question is already well answered, the thread is political, medical, financial or otherwise sensitive, the reply would need an invented claim, or the user already replied there.

### 4. Draft

Structure: answer the question in the first sentence; one concrete insight, example or workflow; the product only when it materially improves the answer; the disclosure line; a natural ending with no engagement bait.

Do not open with "great question", "I totally agree", "thanks for sharing". Do not end with "thoughts?", "check out my product" or an unneeded link. One link at most, only when the person asked for a resource and the community allows it, never through a shortener.

## Rules

- The agent never publishes anything, anywhere, on any account. The user posts.
- Never hide affiliation, never pose as a customer, never claim the product was found independently, never invent results or testimonials, never attack a competitor, never reuse the same wording across threads.
- Re-read the community's rules (from `community/config.md`) before every draft, including follow-ups. Unknown rules mean no product mention.
- A moderation warning or a removal is a negative outcome even when the post got traffic. Log it and tighten.

## Output

The daily briefing: threads monitored and what changed, response drafts due, new opportunities kept and rejected with reasons, the 1 or 2 drafts with permalink, classification and the rules note, and the total charged as the sum of every run's `billing.charged` (not a wallet difference: the balance is shared by every session on the key). End with: drafts ready, nothing posted.
