---
name: ai-visibility-audit
description: Audit what AI assistants say about a brand and its category with RouterGrowth: a frozen panel of buyer questions run across ChatGPT, Claude, Gemini and Perplexity (aeo.answer), the sources they cite, where the domain already appears (aeo.mentions), the AI search volume behind each prompt (aeo.keywords), paired with the classic SERP (seo.serp). Share of voice against competitors, and the gaps as absent, wrong or fragile. Use when the user asks "what does ChatGPT say about us", wants an AI search or AEO or GEO audit, wants to track AI visibility monthly, or asks which sources the assistants cite for their category.
---

# AI visibility audit

Rank tracking asks where a page sits. This asks what the assistant says, whether the brand is in the answer, and which sources put it there. The value is in re-running the same panel monthly, so the panel is frozen and saved.

## Before you start

- Load the core `routergrowth` skill (https://www.routergrowth.com/SKILL.md) if it is not loaded. Confirm access with the free `balance` tool or `routergrowth balance`.
- Ask for: the brand and domain, the category in the buyer's words, three to five competitors, and the market (country, language).
- Inspect `aeo.answer`, `aeo.mentions`, `aeo.keywords` and `seo.serp` once and show the prices. Quote the audit: N prompts x 4 assistants, plus the mentions and SERP passes. A 20-prompt panel is around a hundred calls; say what that costs before running.

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
routergrowth run -c aeo.answer -i '{"prompt":"best GTM data api for agents","assistant":"chatgpt","location":"United States"}' --max-cost 0.10 --wait 60
```

Run every prompt across `chatgpt`, `claude`, `gemini` and `perplexity`. For each answer record: the assistant, the verbatim brand mentions (yours and competitors'), the position of the first mention, and every cited URL. Answers vary between runs; run the panel once for a baseline and note that a single run is a sample.

### 3. Where the domain already appears

```bash
routergrowth run -c aeo.mentions -i '{"domain":"yourdomain.com","platform":"chatgpt","limit":50}' --max-cost 0.10 --wait 60
```

Lists the prompts where the domain is cited today. The difference between this and the panel is the gap list.

### 4. The citation graph

Aggregate every cited URL across all answers: domain, count, which prompts. The top of that table is the set of pages that decide the category. Flag the Reddit threads, the comparison pages and the review sites in it: those are the places where a change moves the answer.

### 5. Pair with the classic SERP

```bash
routergrowth run -c seo.serp -i '{"keyword":"best GTM data api","location":"United States","engine":"google"}' --max-cost 0.02 --wait 30
```

For the category and comparison prompts, see whether the pages the assistants cite are the pages that rank. When they diverge, the assistant is reading something the SERP does not show, usually a community thread.

### 6. Score

- Share of voice per assistant: the brand's mentions divided by all brand mentions on the panel.
- Per prompt: present (and where), absent, wrong (a false claim about the brand, quoted), fragile (mentioned by one assistant only, or cited from a single source).
- Per competitor: the same, so the user sees who owns which group.

## Rules

- Never fabricate an answer or a citation. Every quote is verbatim from a run and carries the run ID.
- One panel run is a sample; say so in the report. Trends need the same panel run monthly.
- This skill measures. It does not post, comment or seed anything. When the gaps point at a Reddit thread, hand it to a human with talking points.

## Output

`report.md` with: the panel and its version, share of voice per assistant, the citation graph (top 20 domains with counts and the prompts they answer), the gap list as absent / wrong / fragile with a next action for each, and the competitor table. Plus `answers.json` with every raw answer, and the total charged with run IDs. Save both next to `panel.json` so next month's run diffs against them.
