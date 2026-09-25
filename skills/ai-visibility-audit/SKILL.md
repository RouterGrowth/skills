---
name: ai-visibility-audit
description: >-
  Audit what AI assistants say about a brand and its category with RouterGrowth:
  a frozen panel of buyer questions run across ChatGPT, Claude, Gemini and
  Perplexity (aeo.answer), the sources they cite, where the domain already
  appears (aeo.mentions), the AI search volume behind each prompt
  (aeo.keywords), paired with the classic SERP (seo.serp). Share of voice
  against competitors, and the gaps as absent, wrong or fragile. Use when the
  user asks "what does ChatGPT say about us", wants an AI search or AEO or GEO
  audit, wants to track AI visibility monthly, or asks which sources the
  assistants cite for their category.
---

# AI visibility audit

Rank tracking asks where a page sits. This asks what the assistant says, whether the brand is in the answer, and which sources put it there. The value is in re-running the same panel monthly, so the panel is frozen and saved.

## Before you start

- Load the core `routergrowth` skill (https://www.routergrowth.com/SKILL.md) if it is not loaded. Confirm access with the free `balance` tool or `routergrowth balance`.
- Ask for: the brand and domain, the category in the buyer's words, three to five competitors, and the market (country, language).
- Inspect `aeo.answer`, `aeo.mentions`, `aeo.keywords` and `seo.serp` once and show the prices. `aeo.answer` is priced per assistant (inspect lists them under pricing by platform): perplexity $0.0175, chatgpt $0.07, gemini $0.08925, claude $0.12075 when this was written, so one prompt across the four is about $0.30 and a 20-prompt panel about $5.95 before the mentions and SERP passes. Quote that before running.

## Steps

### 1. Build and freeze the panel

15 to 20 buyer questions in four groups, phrased the way a buyer talks to an assistant:

- category ("best tools for X", "how do teams do X")
- comparison ("A vs B", "alternatives to A")
- problem ("how do I fix X", "why does X happen")
- brand-direct ("is Brand good for X", "Brand pricing")

Save the panel to `panel.json` with a version and a date. Do not change it between runs; add a new version instead.

Optional: `aeo.keywords` with the panel's key phrases returns AI search volume, which tells you which prompts carry weight.

### 2. Capture the answers and their sources

```bash
routergrowth run -c aeo.answer -i '{"prompt":"best GTM data api for agents","assistant":"chatgpt","location":"US"}' --max-cost 0.11 --wait 60
```

Set `max_cost` from the assistant you call: 0.13 covers all four (claude quotes $0.12075; 0.12 rejects every claude call and silently drops one assistant from the audit). `location` is a country code or name and steers the web search on chatgpt, claude and perplexity; gemini's endpoint refuses it, so gemini answers without it. The result carries `answer`, `model` (the model that actually answered, gpt-4o-mini rather than a flagship: say so in the report), `sources` (cited URLs) and `source_domains`. Run every prompt across `chatgpt`, `claude`, `gemini` and `perplexity`, check every run's `status` before aggregating (a refused or failed run leaves a hole, not an answer), and record per answer: the assistant, the verbatim brand mentions (yours and competitors'), the position of the first mention as the sentence index in the answer, and every cited URL. Gemini's sources come back as Google grounding redirect URLs with no readable domain, so the citation graph and the single-source test cover the other three assistants; say so. Answers vary between runs; run the panel once for a baseline and note that a single run is a sample.

### 3. Where the domain already appears

```bash
routergrowth run -c aeo.mentions -i '{"domain":"yourdomain.com","platform":"chatgpt","limit":10}' --max-cost 0.20 --wait 60
```

Lists the prompts where the domain is cited today, on `chatgpt` or on `google` (AI Mode); run both. $0.175 a search plus $0.00175 a row: $0.1925 at a limit of 10, $0.2625 at 50, so `max_cost` 0.20 covers the default and a cap below the quote is refused with a 402 that names it. A `no_match` here is a real finding, not a failure: the domain is not cited anywhere yet, the call is released, not billed, and `result` is null rather than an empty list. The difference between this and the panel is the gap list.

### 4. The citation graph

Aggregate every cited URL across all answers: domain, count, which prompts. The top of that table is the set of pages that decide the category. Flag the Reddit threads, the comparison pages and the review sites in it: those are the places where a change moves the answer.

### 5. Pair with the classic SERP

```bash
routergrowth run -c seo.serp -i '{"keyword":"best GTM data api","location":"United States","engine":"google"}' --max-cost 0.02 --wait 30
```

For the category and comparison prompts, see whether the pages the assistants cite are the pages that rank. When they diverge, the assistant is reading something the SERP does not show, usually a community thread. Rows carry `position`, `title`, `url`, `domain`, `snippet`; `ai_overview_present` and `serp_features` come with the primary provider and are absent when a run fell back to the secondary one, so skip the AI Overview comparison on that prompt rather than reading absence as false.

### 6. Score

- Share of voice per assistant: the brand's mentions divided by all brand mentions on the panel. Report it twice: on the whole panel, and on the category, comparison and problem prompts only. The brand-direct prompts name the brand, so they inflate the first number; the second is the one that says whether anyone finds the brand unprompted.
- Per prompt: present (and where), absent, wrong (a false claim about the brand, quoted), fragile (mentioned by one assistant only, or cited from a single source). A checkable claim is a statement about the product, pricing, company or integrations; mark it wrong only when the brand's own pages contradict it, and quote both.
- Per competitor: the same, so the user sees who owns which group.

## Rules

- Never fabricate an answer or a citation. Every quote is verbatim from a run and carries the run ID.
- One panel run is a sample; say so in the report. Trends need the same panel run monthly.
- This skill measures. It does not post, comment or seed anything. When the gaps point at a Reddit thread, hand it to a human with talking points.

## Output

`report.md` with: the panel and its version, share of voice per assistant (whole panel and unprompted), the citation graph (top 20 domains with counts and the prompts they answer), the gap list as absent / wrong / fragile with a next action for each, and the competitor table. Plus `answers.json` with every raw answer, and the total charged as the sum of every run's `billing.charged` with run IDs (not a wallet difference: the balance is shared by every session on the key). Save both next to `panel.json` so next month's run diffs against them.
