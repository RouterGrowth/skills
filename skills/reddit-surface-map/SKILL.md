---
name: reddit-surface-map
description: >-
  Map the Reddit threads and subreddits that own a category with RouterGrowth:
  the money queries, the threads ranking for them in Google (seo.serp), what
  Reddit itself surfaces for the same phrases (social.search), what those
  threads say (social.comments), and each subreddit's rules on vendors
  (web.scrape). Delivers the map, never posts. Use when the user asks which
  subreddits matter for their product, wants the Reddit threads ranking for
  "best X" or "X alternatives", wants to know where buyers discuss the category,
  or asks about Reddit for SEO or AI visibility.
---

# Reddit surface map

Reddit threads rank for the queries buyers type and get cited by AI assistants. This skill finds the threads and the subreddits behind them, reads what they say, and notes each community's rules, so a human can decide where an honest contribution is welcome. It does not post.

## Before you start

- Load the core `routergrowth` skill (https://www.routergrowth.com/SKILL.md) if it is not loaded. Confirm access with the free `balance` tool or `routergrowth balance`.
- Ask for: the product and category, three to five competitors, and the market (country, language).
- Inspect `seo.serp`, `social.search` and `social.comments` once and show the prices: $0.0035 a SERP, $0.0024 a post for a Reddit search, $0.07 plus $0.00665 a comment for a thread read. Quote the map: N queries x 2 SERPs, N Reddit searches at a limit of 10 ($0.024 each), M threads at a limit of 30 ($0.2695 each). Reading 10 threads is about $2.70, above the core skill's ask-first line, so get a yes on the read pass before it starts.

## Steps

### 1. The money queries

10 to 20 phrases: "best X", "X vs Y", "X alternatives", "X for (audience)", and the problem phrasings ("how to do X without Y"). Save them.

### 2. The threads ranking in Google

```bash
routergrowth run -c seo.serp -i '{"keyword":"best crm for small agencies reddit","location":"United States","engine":"google"}' --max-cost 0.02 --wait 60
```

Run each query, with and without the word "reddit", one after another or through `batch_run`. Do not use a `site:reddit.com` operator: the results do not honour it and the provider bills it at five times the price. Rows carry `position`, `title`, `url`, `domain`, `snippet` and no date. Keep every reddit.com result: URL, subreddit, position, thread title. A thread in the top ten for two or more queries is a hub. A run that ends `interrupted` (the router restarted under it, for instance during a deploy) charged nothing: resubmit it.

### 3. What Reddit surfaces itself

```bash
routergrowth run -c social.search -i '{"platform":"reddit","query":"crm for small agencies","limit":10}' --max-cost 0.15 --wait 120
```

$0.0024 a post: a limit of 10 quotes $0.024 (set `max_cost` 0.03), a limit of 50 quotes $0.12, and fewer posts than the limit bill fewer. Reddit searches often run past 60 seconds; poll a still-running receipt with `runs get -r <run_id> --wait 60 -o file`. The search matches post text (it is a Reddit search page, sorted by relevance) and returns post rows only: `url`, `text` (the title), `body`, `community`, `author`, `created_at` (ISO 8601, UTC). Engagement counts are null on these rows. Expect some off-topic rows. Adds the threads that are active but do not rank yet. Merge with step 2 on URL.

### 4. Read the hubs

For the top 10 to 15 threads:

```bash
routergrowth run -c social.comments -i '{"url":"https://www.reddit.com/r/.../comments/...","limit":30}' --max-cost 0.30 --wait 120
```

$0.07 a thread plus $0.00665 a comment: 15 comments quote $0.16975 (set `max_cost` 0.20), 30 quote $0.2695 (set 0.30), 100 quote $0.735, so read the top 15 to 30 of a thread unless the user wants more. The post itself is not returned, only comment rows: `text`, `author`, `likes` (upvotes, may be null), `replies`, `created_at`, `url`, with HTML entities already decoded. Note which products are recommended and how often, the objections, the questions nobody answered, and whether your brand or competitors are mentioned. Quote verbatim, with the comment URL.

### 5. The subreddit roster

For each subreddit that appears twice or more, the rules are a human step: Reddit blocks crawlers on its rules pages (`web.scrape` on `/about/rules/` comes back as a no-match, released, not billed; unauthenticated fetches of `rules.json` and `about.json` are refused; agent browsers are usually barred from reddit.com), so ask the user to open `https://www.reddit.com/r/<name>/about/rules/` and paste the rules and the member count. Record: subscriber count, vendor tolerance (self-promotion rule, flair requirements, vendor flair), posting norms, moderation tone. Classify the risk: open, conditional (flair, disclosure), closed, or unknown until the rules are on file.

## Rules

- Never post, comment, vote or message on Reddit. Never suggest sock puppets, seeding or paid mentions. When the map points at a thread where an honest answer would help, write talking points for a human who will disclose who they are.
- Every claim about a thread carries its URL. Every count is from a run and carries the run ID.
- Rules pages change; date the roster.

## Output

`reddit-map.md` with: the query list with run IDs; the thread table (URL, subreddit, queries it ranks for and where, post date when a search returned it, brands mentioned; there is no thread score or comment count in any of these calls, so leave those out rather than guess); the subreddit roster (name, size and rules when the user supplied them, why it matters, rules risk, target threads); the recommendation table (product, how many threads recommend it, the typical reason); and the talking points for a human, per thread, with the disclosure line. Plus the raw JSON and the total charged as the sum of every run's `billing.charged` (not a wallet difference: the balance is shared by every session on the key).
