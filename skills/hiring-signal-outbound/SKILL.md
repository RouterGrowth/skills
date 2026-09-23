---
name: hiring-signal-outbound
description: >-
  Build a lead list from hiring signals with RouterGrowth. Find companies that
  just posted the role that implies the problem you solve (company.jobs), find
  the person who owns the budget at each (people.search), get a work email
  (contact.find) and verify it before it touches a sender (contact.verify). Use
  when the user wants a lead list, wants to know who is hiring for a role, wants
  to turn job postings into accounts, asks for high-intent leads, or says
  "companies hiring X", "build me a list", "who should we reach out to".
---

# Hiring-signal outbound

A job posting is a company saying in public that it has budget, a gap and a manager who admitted the gap in writing. This skill turns that into a verified contact list in four calls, and releases the calls that find nothing instead of billing them.

## Before you start

- Load the core `routergrowth` skill (https://www.routergrowth.com/SKILL.md) if it is not loaded. Confirm access with the free `balance` tool or `routergrowth balance`, without printing credentials.
- Ask for three things if the user did not give them: the role that implies the problem (the title you would search for), the geography, and the buyer persona (the title and seniority that signs).
- Inspect the five capabilities once and show the prices before the first billable run: `routergrowth inspect -c company.jobs`, then `company.search`, `people.search`, `contact.find`, `contact.verify` (inspect lists every input field with its allowed values). Quote the list as a whole: N accounts, roughly N buyers, roughly N contact lookups. Get a yes on the total. When no human is in the loop (a scheduled or delegated run), the budget the caller set is the approval: stop at it and report.

## Steps

### 1. Accounts from postings

Search postings by title and location, not by company. The account list is the side effect.

```bash
routergrowth run -c company.jobs -i '{"query":"growth engineer","location":"United States","posted_within":"month","limit":30}' --max-cost 0.30 --wait 120 -o jobs.json
```

`posted_within` is `24h`, `week` or `month`; the API refuses anything else. $0.0015 a search plus $0.0015 a posting: the hold covers the requested limit and the charge covers the postings returned (6 back on a limit of 20 bill $0.0105), and no postings at all releases the hold. Keep the first limit at 30 or below. Rows carry `company`, `company_url` (the LinkedIn company URL, no trailing slash), `title`, `location`, `posted_at`, `url` and the description: no headcount, no industry, no web domain. The title match is loose (a "growth engineer" search returns crystal growth engineers and Marketo developers), so drop every row whose title is not the role before spending on it, and drop rows with an empty `company_url`. Dedupe on `company_url`. Sort by date: newest posting first is the queue.

### 2. Size the account and get its domain

Postings cannot be filtered on headcount or industry, and `contact.find` needs a web domain. One `company.search` per account gives both:

```bash
routergrowth run -c company.search -i '{"query":"Acme","location":"San Francisco","limit":5}' --max-cost 0.05 --wait 60
```

Pass the posting's city or country as `location`: a bare name matches homonyms worldwide (a grocer in the Netherlands for "Stuut", an agency in Mexico for "Oscilar"), and with the location a limit of 5 finds the company four times out of five. $0.0015 a search plus $0.006 a company at the requested limit: $0.0315 at a limit of 5 (set `max_cost` 0.05). Pick the row whose `linkedin_url` equals the posting's `company_url` (same shape, no trailing slash); take `domain`, `employee_count`, `industry`. Apply the user's size and industry filter here, before step 3, so the people search is not spent on accounts that get cut. `employee_count` is LinkedIn's member count and `employee_range` the company's declared bracket; they disagree often, so filter on the count.

Optional stacking signals, only when the user wants a tighter list: `company.funding` (a round inside 90 days is budget that must be spent) and `company.technologies` (running the tool you replace, or the one you integrate with). Run them on the deduped domains and score: hiring plus funded plus running the tool is not a cold lead.

### 3. The buyer at each account

The hiring manager is rarely the buyer. Search by seniority and function inside each company:

```bash
routergrowth run -c people.search -i '{"company_domains":["acme.com"],"titles":["Founder","CEO","VP Marketing"],"seniority":["cxo","vp","owner"],"detail":"full","limit":2}' --max-cost 0.30 --wait 120
```

Pass the `domain` step 2 found as `company_domains`: it is the precise employer key and opens the database route, $0.036 a person actually returned (2 asked, 1 found, $0.036) with a work email when one is known. When step 2 found no domain, pass the posting's `company_url` in `companies` instead; a LinkedIn URL runs the LinkedIn route, which returns no emails. `seniority` is `entry`, `senior`, `manager`, `director`, `vp`, `cxo`, `partner` or `owner`; the API refuses other values. Put the buyer's titles in `titles`, not the hiring manager's: a "Head of Growth" search returns the person who will report to the buyer. That route quotes $0.15 a search page plus $0.006 a profile in full mode plus up to $0.030075 to resolve the employer ($0.192 at a limit of 2), and `max_cost` must cover it for auto routing to fall back to it: 0.30 covers a limit of 2 to 25 on either route. Two people per account at most. Rows carry `first_name`, `last_name`, `name`, `headline`, `current_title`, `current_company`, `linkedin_url`, `location` and `email` (empty on the LinkedIn route). A row that already carries an email skips step 4 and goes straight to step 5. Drop any row whose last name is missing or reads `undefined`: LinkedIn truncates some names and the email lookup cannot use them. Drop rows with an empty `current_company`. Small companies often return nobody; that is a miss, not an error.

### 4. Work email

```bash
routergrowth run -c contact.find -i '{"first_name":"Alex","last_name":"Rivera","company_domain":"acme.com"}' --max-cost 0.10
```

Auto routing waterfalls across providers and charges only the one that delivers. A no-match is released, not billed, so a list with a 60% hit rate costs 60% of a list. The hold is 1.5x the quote ($0.056 held for a $0.0375 quote), which `max_cost` 0.10 covers. Over MCP, send all rows in one `batch_run` with `max_cost` per item and `max_total_cost` for the batch. Over the CLI, loop `run` and collect run IDs.

Before the lookups, run the free dedupe pass: `routergrowth history --file people.txt` (one LinkedIn URL per line) and read the `contacted` and `reusable` columns. `contacted` means this workspace already emailed or messaged the person: drop them. `reusable` means a paid result exists: reuse it instead of paying again. `seen` alone means a run touched the URL (the search you just ran counts) and is not a reason to drop anyone.

### 5. Verify before anyone sends

```bash
routergrowth run -c contact.verify -i '{"email":"alex.rivera@acme.com"}' --max-cost 0.02
```

Keep `valid`. Drop `invalid`. Hold `catch_all` and `unknown` in a separate column and say so: a catch-all domain accepts everything, so the address is unproven, not clean.

## Rules

- Inspect once per capability, quote the whole list, then run. Do not re-ask between rows once the user approved the total.
- `max_cost` on every run. Keep the first `company.jobs` limit at 30 or below until the user has seen one result. Per-result capabilities bill the requested limit even when fewer rows come back.
- Stop and ask before a batch over about $1 unless the user asked for that volume.
- Never present sandbox (`rg_test_`) output as real data. Every row carries the run ID that produced it.
- Do not email anyone from this skill. Sending is the `cold-email-pipeline` skill, which starts with its own gate.

## Human gate

Before handing off to any outreach: show the account count, the contact count by verification status, the total charged (the sum of every run's `billing.charged`, not a wallet difference: the balance is shared by every session on the key), and five sample rows. Wait.

## What one real run looked like

10 postings for "GTM engineer" in the United States ($0.015), 3 people at one of the two companies searched ($0.174), the domain from company.search ($0.0075), one email found ($0.0375) and one no-match released ($0), the found email verified valid ($0.009). About $0.24 for a verified contact, with the misses costing nothing.

A second run on 2026-09-12: 76 postings across three searches ($0.135), 12 company lookups ($0.135), 5 people searches ($0.81), 3 email lookups with 2 found ($0.075), 2 verified valid ($0.019). $1.17 for two verified buyers at growth-engineer-hiring startups; the people searches were three quarters of it, which is why the size filter runs before them.

## Output

A CSV with one row per contact: `company, domain, employee_count, posting_title, posted_at, first_name, last_name, current_title, linkedin_url, email, verify_status, provider, run_ids, charge`. `run_ids` lists the jobs, company, people, find and verify runs behind the row, space-separated; `charge` is the find plus verify cost of that row, and the search costs go in the totals. Plus the totals: accounts found, buyers found, emails found, emails valid, total charged. Misses are listed at the bottom with the reason, so the user can see what was filtered and why.
