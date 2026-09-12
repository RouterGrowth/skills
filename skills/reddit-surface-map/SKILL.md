---
name: reddit-surface-map
description: Map the Reddit threads and subreddits that own a category with RouterGrowth: the money queries, the threads ranking for them in Google (seo.serp), what Reddit itself surfaces for the same phrases (social.search), what those threads say (social.comments), and each subreddit's rules on vendors (web.scrape). Delivers the map, never posts. Use when the user asks which subreddits matter for their product, wants the Reddit threads ranking for "best X" or "X alternatives", wants to know where buyers discuss the category, or asks about Reddit for SEO or AI visibility.
---

# Reddit surface map

Reddit threads rank for the queries buyers type and get cited by AI assistants. This skill finds the threads and the subreddits behind them, reads what they say, and notes each community's rules, so a human can decide where an honest contribution is welcome. It does not post.

## Before you start

- Load the core `routergrowth` skill (https://www.routergrowth.com/SKILL.md) if it is not loaded. Confirm access with the free `balance` tool or `routergrowth balance`.
- Ask for: the product and category, three to five competitors, and the market (country, language).
- Inspect `seo.serp`, `social.search`, `social.comments` and `web.scrape` once and show the prices. Quote the map: N queries x 1 SERP, N Reddit searches, M threads read.

## Steps

### 1. The money queries

10 to 20 phrases: "best X", "X vs Y", "X alternatives", "X for (audience)", and the problem phrasings ("how to do X without Y"). Save them.

### 2. The threads ranking in Google

```bash
routergrowth run -c seo.serp -i '{"keyword":"best crm for small agencies reddit","location":"United States","engine":"google"}' --max-cost 0.02 --wait 30
```

Run each query, with and without the word "reddit". Keep every reddit.com result: URL, subreddit, position, thread title, and the age if visible. A thread in the top ten for two or more queries is a hub.

### 3. What Reddit surfaces itself

```bash
routergrowth run -c social.search -i '{"platform":"reddit","query":"crm for small agencies","limit":50}' --max-cost 0.10 --wait 60
```

Adds the threads that are active but do not rank yet. Record score, comment count and date. Merge with step 2 on URL.

### 4. Read the hubs

For the top 10 to 15 threads:

```bash
routergrowth run -c social.comments -i '{"url":"https://www.reddit.com/r/.../comments/...","limit":100}' --max-cost 0.10 --wait 60
```

Note which products are recommended and how often, the objections, the questions nobody answered, and whether your brand or competitors are mentioned. Quote verbatim, with the comment URL.

### 5. The subreddit roster

For each subreddit that appears twice or more, fetch its rules and sidebar (`web.scrape` on `https://www.reddit.com/r/<name>/about/rules/`, or your own fetch when you have one). Record: subscriber count, vendor tolerance (self-promotion rule, flair requirements, vendor flair), posting norms, moderation tone. Classify the risk: open, conditional (flair, disclosure), closed.

## Rules

- Never post, comment, vote or message on Reddit. Never suggest sock puppets, seeding or paid mentions. When the map points at a thread where an honest answer would help, write talking points for a human who will disclose who they are.
- Every claim about a thread carries its URL. Every count is from a run and carries the run ID.
- Rules pages change; date the roster.

## Output

`reddit-map.md` with: the query list; the thread table (URL, subreddit, queries it ranks for and where, score, comments, age, brands mentioned); the subreddit roster (name, size, why it matters, rules risk, target threads); the recommendation table (product, how many threads recommend it, the typical reason); and the talking points for a human, per thread, with the disclosure line. Plus the raw JSON and the total charged.
