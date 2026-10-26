---
name: seo-competitor-gap
description: >-
  Find the search traffic competitors win and the user does not, with
  RouterGrowth: the domains that compete in search (seo_competitors), each
  side's traffic and keyword count (seo_domain_overview), the keywords each
  competitor ranks for (seo_ranked_keywords) against the user's own, volume
  and difficulty for the gaps (seo_keywords), who links to competitors and not
  to the user (seo_backlinks), and the live results page for the best targets
  (seo_serp). Ends with a prioritised list of pages to write or fix. Use when
  the user asks "what keywords do my competitors rank for", "keyword gap",
  "content gap", "why do they outrank us", "SEO competitor analysis", or wants
  an SEO plan built on data.
license: MIT
metadata:
  version: "0.3.1"
  author: RouterGrowth
  homepage: https://www.routergrowth.com/skills/seo-competitor-gap
---

# SEO competitor gap

The keywords that already send buyers to competitors, minus the ones the user already ranks for, sorted by what they are worth and how winnable they are. The output is a page plan, not a data dump.

## Before you start

- The RouterGrowth tools must be in your tool list. If they are missing, the user connects RouterGrowth (Claude settings, Connectors: sign in, approve a workspace). Confirm with the free `get_workspace_balance`.
- Get the user's domain, the country and language that matter (default: the user's main market), and two to four competitors. If the user has none in mind, step 1 finds them.
- `get_operation_pricing` (free) once for each SEO tool. A gap analysis is roughly ten calls: quote it as one number and go ahead when under about $1. Priced per search or lookup; an empty result costs nothing.

## Steps

### 1. Who competes in search

```json
{"input": {"domain": "acme.com", "location": "United States", "language": "en", "limit": 10}, "max_cost": "<cap>"}
```

`seo_competitors` returns the domains that share the most keywords with the user's. Drop marketplaces, media sites and directories (they rank for everything) unless the user competes with them. When the user's domain ranks for very few keywords (step 2 shows fewer than about 50), this list is built on almost nothing and is mostly noise: use the competitors the user names instead. Confirm the final two to four with the user.

### 2. Size each side

`seo_domain_overview` `{"domain": ..., "location": ...}` for the user and each competitor: organic traffic, keyword count, paid presence. One table, so the user sees the size of the gap before the detail.

### 3. What each side ranks for

`seo_ranked_keywords` per domain, the same location and language:

```json
{"input": {"domain": "competitor.com", "location": "United States", "language": "en", "limit": 200}, "max_cost": "<cap>"}
```

Rows come back sorted by search volume, not by position, so a small limit returns big keywords where the competitor ranks on page 5. Ask for 200 or more and keep the rows at position 20 or better before comparing. Keep keyword, position, search volume, the ranking URL. Run it on the user's domain too. Then compute, without paying:

- **Gap**: keywords where a competitor ranks in the top 10 and the user is absent or below 20.
- **Weak**: keywords where the user ranks 11 to 30 and a competitor is in the top 5.
- **Shared wins**: keywords the user already leads (to protect, not to chase).

Drop branded keywords (a competitor's own name) and keywords with no buying intent for the user's product.

### 4. Price and difficulty for the best gaps

For the 10 to 20 gap keywords with the most volume and the clearest intent, `seo_keywords` `{"keyword": ..., "location": ..., "language": ...}` returns volume, CPC (what advertisers pay, a proxy for commercial value), competition, and related ideas. Group close variants under one page.

### 5. Read the results page for the top targets

`seo_serp` on the five best targets: who ranks, what kind of page wins (a guide, a comparison, a tool, a list), whether an AI overview sits on top and which pages it cites (`ai_overview_sources`), and the forums or videos in the results. A page type mismatch is the most common reason a good page does not rank.

### 6. Links (optional)

`seo_backlinks` `{"domain": "competitor.com", "limit": 100}` for each competitor: referring domains that link to two or more competitors and not to the user are outreach targets. List them with the page they link to.

## Rules

- `max_cost` on every paid call.
- Every number comes from a result for the stated country and language, with the date of the run. Never estimate traffic from volume and position as if it were measured; label any estimate.
- Volumes are monthly averages from the provider's index, not exact counts; small keywords can read zero.
- This skill writes the plan and can draft outlines; it publishes nothing.
- If a tool fails in a way its error does not explain, offer to report it and call `submit_feedback` only if the user says yes.

## Output

1. The overview table (traffic and keywords per domain).
2. The page plan, 10 to 20 rows sorted by priority: `target keyword, monthly volume, CPC, page type that wins, competitor ranking and its URL, user's current position, new page or fix existing URL, why`.
3. The weak keywords to fix, with the user's URL.
4. Link targets, if step 6 ran.
5. The calls made and the total spent from `list_runs`.
