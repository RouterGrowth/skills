---
name: icp-lead-list
description: >-
  Turn an ideal customer profile into a scored lead list with RouterGrowth:
  agree the ICP in one exchange (industry, size, geography, buyer titles),
  find matching companies (company_search) and the buyers inside them
  (people_search, cheapest lead database first), add company facts only for
  the accounts that make the cut (company_enrich, company_technologies,
  company_funding), then find and verify a work email for the people kept
  (contact_find, contact_verify). Every row says why it fits. Use when the
  user says "build me a lead list", "find companies like X", "find heads of
  growth at Series A SaaS in Europe", "who should I sell to", "find 50
  prospects", or describes their buyer and asks for names.
license: MIT
metadata:
  version: "0.3.1"
  author: RouterGrowth
  homepage: https://www.routergrowth.com/skills/icp-lead-list
---

# ICP lead list

From a description of the buyer to a list of real people at real companies, each with a verified email and one line on why they fit. The list is small and right before it is big: the first pass is 10 to 25 rows the user can judge, then it scales.

## Before you start

- The RouterGrowth tools must be in your tool list. If they are missing, the user connects RouterGrowth (Claude settings, Connectors: sign in, approve a workspace). Confirm with the free `get_workspace_balance`.
- Write the ICP back to the user in one block and get a yes before spending: industry or what the company sells, headcount band, geography, the buyer's titles and seniority, two or three exclusions (agencies, competitors, existing customers). If the user only gave their own website, read it (`web_scrape`, one page) and propose the ICP from it.
- Ask for the size of the first pass (default 20 people) and whether they need emails now or only names.
- Call `get_operation_pricing` (free) once for `people_search`, `company_search`, `contact_find` and `contact_verify`, and any enrichment you will run. Read `waterfall.max_cost_for_all` for each lookup: it is the `max_cost` that lets every provider try, and you pay only for the one that finds. Quote the first pass as a whole and get a yes on anything likely above about $1. When no human is in the loop, the budget the caller set is the approval.
- Call `list_tables` (free). When tables are on, keep the list in a table named after the ICP (for example `seriesa-saas-eu-growth`), resume it if it exists, and say its name once. Otherwise write `out/<name>.csv` (Claude Code) or a markdown table in the chat.

## Steps

### 1. People first when the titles are clear

When the ICP names titles and filters the lead database understands, search people directly; the companies come with them:

```json
{"input": {"titles": ["Head of Growth", "VP Growth"], "industries": ["software"],
  "company_headcount": ["11-50", "51-200"], "locations": ["Germany", "France", "United Kingdom"], "limit": 25},
 "max_cost": "<cap>"}
```

`company_headcount` takes the bands `1-10`, `11-50`, `51-200`, `201-500`, `501-1000`, `1001-5000`, `5001-10000`, `10001+`, contiguous. `seniority` takes `entry`, `senior`, `manager`, `director`, `vp`, `cxo`, `partner`, `owner`. The cheapest route is a lead database: it serves titles or seniority, not both together, so pick one. Its rows carry name, title, company, company domain and LinkedIn URL, without email. Priced per person returned; ask for the number you will use. For the next page, pass `next_cursor` back as `cursor` with the same filters.

### 2. Companies first when the fit is about the company

When the fit is "companies that do X" (a niche, a technology, a business model), find the accounts first:

```json
{"input": {"query": "warehouse robotics", "location": "Netherlands", "limit": 25}, "max_cost": "<cap>"}
```

Keep `name`, `domain`, `employee_count`, `industry`, `linkedin_url`. Drop accounts outside the size band and the exclusions now, before any people search. Then the buyers inside the accounts that remain, two per account at most:

```json
{"input": {"company_domains": ["acme.com", "beta.io"], "titles": ["Head of Operations", "COO"], "limit": 4},
 "max_cost": "<cap>"}
```

Small companies often return nobody: that is a miss, not an error. For a founder-led company, the founder is the buyer: search `seniority: ["owner", "cxo"]` instead.

### 3. Qualify and score (mostly free)

Score each row 1 to 3 against the ICP using what you already have (title, company, size, location), and write one line of reason ("VP Growth at a 60-person fintech in Berlin, matches title and band"). Optional paid signals, only on rows that scored 2 or 3 and only when the user wants a tighter list:

- `company_enrich` `{"domain": ...}`: industry, headcount, founded, funding, competitors.
- `company_technologies` `{"domain": ...}`: running the tool the user replaces or integrates with.
- `company_funding` `{"domain": ...}`: a recent round is budget that must be spent.

These are charged only when data is found. Lookups take `max_cost` at their `max_cost_for_all`.

### 4. Emails for the rows kept

Use the root domain: rows sometimes carry a subdomain (`app.acme.com`); strip it before looking up emails. Free first: `get_subjects_history` on the LinkedIn URLs (reuse what the workspace already found, drop people it already contacted if the user says so) and `list_suppressions` when tables are on. Then `contact_find` per row:

```json
{"input": {"first_name": "Lena", "last_name": "Vogel", "company_domain": "acme.com"}, "max_cost": "<max_cost_for_all>"}
```

Charged only when an email is found. Then `contact_verify` with `{"email": ...}` on every address: keep `valid`, drop `invalid`, flag `catch_all` and `risky` in their own column. A `no_match` saying the person opted out ends it for that person.

## Gate

Show the first pass before scaling: rows by score, emails found and valid, the total spent (from `list_runs` for this job, not a wallet difference), and every row with its reason. Ask what to change in the ICP (titles too junior, wrong size, an industry to exclude). Scale only after a yes, in pages of 25 to 100, reporting the running total.

## Rules

- `max_cost` on every paid call; on lookups, the `waterfall.max_cost_for_all`. Never cap a lookup at the cheapest provider's price.
- Never invent a company, a person, a title or a reason. Every row comes from a result and carries the run id that produced it.
- Search with structured filters (titles, locations, domains), not with a person's name in a web search.
- Collect only the fields the list needs. Emails and profiles come from RouterGrowth's third-party data providers; if anyone asks where a value came from, point to https://www.routergrowth.com/privacy and https://www.routergrowth.com/privacy/opt-out.
- This skill sends nothing. To write to the list, hand the verified rows to `email-list-pipeline` (email after approval) or `linkedin-drafts` (drafts the user sends).
- If a tool fails in a way its error does not explain, offer to report it and call `submit_feedback` only if the user says yes.

## Output

One row per person: `score, reason, first_name, last_name, title, company, domain, employee_count, location, linkedin_url, email, verify_status, signals, run_ids`. Plus the ICP as agreed, the totals (companies, people, emails found, valid, spent) and the rows dropped with the reason.
