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
- Inspect the four capabilities once and show the prices before the first billable run: `routergrowth inspect -c company.jobs`, then `people.search`, `contact.find`, `contact.verify`. Quote the list as a whole: N accounts, roughly N buyers, roughly N contact lookups. Get a yes on the total.

## Steps

### 1. Accounts from postings

Search postings by title and location, not by company. The account list is the side effect.

```bash
routergrowth run -c company.jobs -i '{"query":"lifecycle marketing manager","location":"United States","posted_within":"30d","limit":50}' --max-cost 0.30 --wait 60 -o jobs.json
```

Keep company, the LinkedIn company URL (`company_url`), title, location and posted date. Postings carry no web domain; step 2 takes the LinkedIn URL directly, and step 2b resolves the domain the email lookup needs. Dedupe on company URL. Sort by date: newest posting first is the queue.

Optional stacking signals, only when the user wants a tighter list: `company.funding` (a round inside 90 days is budget that must be spent) and `company.technologies` (running the tool you replace, or the one you integrate with). Run them on the deduped domains and score: hiring plus funded plus running the tool is not a cold lead.

### 2. The buyer at each account

The hiring manager is rarely the buyer. Search by seniority and function inside each company:

```bash
routergrowth run -c people.search -i '{"companies":["https://www.linkedin.com/company/acme"],"titles":["VP Marketing","Head of Growth"],"seniority":["vp","head","director"],"detail":"full","limit":4}' --max-cost 0.30 --wait 120
```

`companies` takes company names or LinkedIn company URLs, so the postings feed it directly. The quote is a per-call base plus a per-result rate (about $0.15 plus $0.006 a profile at the time of writing), so `max_cost` has to cover the base: 0.10 is rejected, 0.30 covers a limit of 4 to 20. Two people per account at most. Keep first name, last name, headline and the LinkedIn URL. Drop any row whose last name is missing or reads `undefined`: LinkedIn truncates some names and the email lookup cannot use them. Small companies often return nobody; that is a miss, not an error.

### 2b. The domain

`contact.find` needs the company's web domain and neither step above returns one. Resolve it once per account:

```bash
routergrowth run -c company.search -i '{"query":"Acme","limit":2}' --max-cost 0.02 --wait 60
```

Pick the row whose `linkedin_url` matches the posting's company URL and take its `domain`. Under a cent per lookup.

### 3. Work email

```bash
routergrowth run -c contact.find -i '{"first_name":"Alex","last_name":"Rivera","company_domain":"acme.com"}' --max-cost 0.10
```

Auto routing waterfalls across providers and charges only the one that delivers. A no-match is released, not billed, so a list with a 60% hit rate costs 60% of a list. Over MCP, send all rows in one `batch_run` with `max_cost` per item and `max_total_cost` for the batch. Over the CLI, loop `run` and collect run IDs.

Before the lookups, run the free dedupe pass: `routergrowth history --file people.txt` (one email, name or LinkedIn URL per line) says who was already contacted or already enriched, and returns the reusable result so you do not pay twice.

### 4. Verify before anyone sends

```bash
routergrowth run -c contact.verify -i '{"email":"alex.rivera@acme.com"}' --max-cost 0.02
```

Keep `valid`. Drop `invalid`. Hold `catch_all` and `unknown` in a separate column and say so: a catch-all domain accepts everything, so the address is unproven, not clean.

## Rules

- Inspect once per capability, quote the whole list, then run. Do not re-ask between rows once the user approved the total.
- `max_cost` on every run. Keep the first `company.jobs` limit at 50 or below until the user has seen one result.
- Stop and ask before a batch over about $1 unless the user asked for that volume.
- Never present sandbox (`rg_test_`) output as real data. Every row carries the run ID that produced it.
- Do not email anyone from this skill. Sending is the `cold-email-pipeline` skill, which starts with its own gate.

## Human gate

Before handing off to any outreach: show the account count, the contact count by verification status, the total charged, and five sample rows. Wait.

## What one real run looked like

10 postings for "GTM engineer" in the United States ($0.015), 3 people at one of the two companies searched ($0.174), the domain from company.search ($0.0075), one email found ($0.0375) and one no-match released ($0), the found email verified valid ($0.009). About $0.24 for a verified contact, with the misses costing nothing.

## Output

A CSV with one row per contact: `company, domain, posting_title, posted_at, first_name, last_name, title, linkedin_url, email, verify_status, provider, run_id, charge`. Plus the totals: accounts found, buyers found, emails found, emails valid, total charged. Misses are listed at the bottom with the reason, so the user can see what was filtered and why.
