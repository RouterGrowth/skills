---
name: list-enrichment
description: >-
  Enrich a list the user already has (a CSV, a spreadsheet export, a pasted
  table of names and companies, LinkedIn URLs or domains) with RouterGrowth:
  clean and dedupe it, fix missing or wrong company domains (company_search),
  find work emails across several data providers in turn (contact_find),
  verify every address (contact_verify), and add direct phone numbers
  (contact_phone) or full profiles (person_enrich) only when asked. Reuses
  results the workspace already paid for and skips people who opted out.
  Use when the user says "enrich this list", "find emails for these people",
  "verify these emails", "get phone numbers for my leads", uploads a CSV of
  contacts, or wants a Clay-style enrichment run without a subscription.
license: MIT
metadata:
  version: "0.3.1"
  author: RouterGrowth
  homepage: https://www.routergrowth.com/skills/list-enrichment
---

# List enrichment

The user brings the people; this skill brings back a verified work email for as many of them as the providers know, a phone where asked, and an honest count of what was found, what was risky and what was missed. Most of the money in a list job is spent here, so the order of the steps is the order that wastes the least.

## Before you start

- The RouterGrowth tools must be in your tool list. If they are missing, the user connects RouterGrowth (Claude settings, Connectors: sign in, approve a workspace). Confirm with the free `get_workspace_balance`.
- Read the list the user gave (a file in the working folder, an attachment or a pasted table). Name the columns you found and map them: first name, last name, full name, company name, company domain, LinkedIn URL, existing email. Ask only when a column is ambiguous.
- Ask what the list is for once, and which fields they need: emails only (the default), emails and phones, or full profiles. Phones and profiles cost more per row; never add them by default.
- Call `get_operation_pricing` (free) for `contact_find` and `contact_verify`, plus `company_search`, `contact_phone` or `person_enrich` if they will run. Read `waterfall.max_cost_for_all` for each: that is the cap you pass as `max_cost` on every lookup, because a lower cap skips the providers priced above it and turns findable rows into misses. Lookups are charged only when they find something, so the high cap does not raise the price of a hit.
- Quote the whole job before the first paid call: rows to look up times the found price, as a range, since misses are free. Get a yes on anything likely above about $1. When no human is in the loop, the budget the caller set is the approval: stop at it and report.
- Call `list_tables` (free). When tables are on, load the list into a table named after it (`upsert_table_rows`) and work from there; otherwise write `out/<list>-enriched.csv` (Claude Code) or a markdown table in the chat.

## Steps

### 1. Clean (free)

- Split full names into first and last name. Strip titles, emojis and suffixes ("PhD", "MBA") from names.
- Normalise domains: lowercase, no `https://`, no path, and no subdomain: `app.acme.com` and `www.acme.com` become `acme.com` (emails live on the root domain; a subdomain turns a findable row into a miss). A personal domain (gmail.com, outlook.com, yahoo.com, icloud.com) is not a company domain: clear it.
- Dedupe on LinkedIn URL, then on first name + last name + domain. Say how many duplicates you removed.
- Rows that already carry an email skip step 3 and go straight to step 4.

### 2. Free checks before paying

- `get_subjects_history` with the LinkedIn URLs and emails you have (batches of up to 100): it returns what this workspace already found for each person. Reuse those results instead of paying again, and drop anyone the workspace already contacted if the user says so.
- When tables are on, `list_suppressions` is the do-not-contact list: remove everyone on it now.

### 3. Fix the domains that are missing or wrong

`contact_find` needs the domain the person's email lives on. For rows with a company name and no domain, or a domain that missed in step 4 of an earlier run:

```json
{"input": {"query": "Acme Robotics", "location": "Germany", "limit": 5}, "max_cost": "<cap>"}
```

Pass a location when the list has one: a bare name matches homonyms worldwide. Take `domain` only from a row whose `name` matches the company and whose country fits; the database also matches words in company descriptions, so a short common name ("Sides", "Clay") returns unrelated companies, and then the domain stays empty and you say so. When two rows fit, keep the one whose `linkedin_url` matches the person's company page or whose description fits what the person does. Country variants and second domains are a common cause of misses (`acme.de` for a German team at `acme.com`, a short brand domain beside the main one): when a find misses on one, try the other once. The company's description or website often names it.

### 4. Find the emails

One call per row without an email:

```json
{"input": {"first_name": "Alex", "last_name": "Rivera", "company_domain": "acme.com"}, "max_cost": "<max_cost_for_all>"}
```

Each call tries the data providers in turn, cheapest first, until one finds the address; you pay only for the one that found it. Results carry `email`, `status` and `employment_verified`. A `no_match` that says the person opted out with RouterGrowth ends it for that person: no retry, no other tool, remove the row. Keep a running total from each receipt and stop at the approved budget.

### 5. Verify every address

`contact_verify` with `{"email": ...}` on every address, including the ones the user brought and the ones step 4 found:

- `valid`: keep.
- `invalid`: drop, and keep the row with an empty email so the user sees the miss.
- `catch_all` or `risky`: keep in a separate column and say so. The domain accepts anything, so the address is unproven: fine for a small personal send, wrong for a bulk send.
- `unknown`: free; leave unverified and say so.

### 6. Phones and profiles (only when asked)

- `contact_phone` with `{"email": ...}` or `{"profile_url": ...}` per row, `max_cost` at its `max_cost_for_all`. Charged only when a number is found, at the price of the provider that found it, which can be several times an email: quote the high end. Results carry `phone`, `type` (mobile or landline) and `confidence`. Flag a number whose country code matches neither the person's location nor the company's country as `check`. Never dial or text from this skill.
- `person_enrich` with `{"profile_url": ...}` for the current role, role history, education and skills, when the user needs more than an email.

## Gate

Before handing the list over, show: rows in, duplicates removed, already known (reused), suppressed, emails found, valid, catch-all or risky, invalid, not found, phones found if asked, the total spent (the sum of this job's charges from `list_runs`, not a wallet difference: the balance is shared by every session on the workspace), and ten sample rows. Then write the file or the table.

## Rules

- `max_cost` on every paid call; on lookups, the `waterfall.max_cost_for_all` from `get_operation_pricing`. Never cap a lookup at the cheapest provider's price.
- Never guess an email pattern (`first.last@`) and present it as found. A guessed address is not in the output unless the user asks for it, and then it carries the label `guessed, unverified`.
- Collect only the fields the job needs. Every enriched row carries the run ids that produced it.
- Emails, phones and profiles come from RouterGrowth's third-party data providers. If anyone asks where a value came from, point to https://www.routergrowth.com/privacy and https://www.routergrowth.com/privacy/opt-out.
- This skill sends nothing. To write to the list, hand the verified rows to `email-list-pipeline` (email after approval) or `linkedin-drafts` (drafts).
- If a tool fails in a way its error does not explain, offer to report it and call `submit_feedback` only if the user says yes.

## What a real run looked like

Our own pilot list: 582 founders and GTM leads at UK and French B2B SaaS companies. The first provider found 440 emails (76%); a second provider found 59 of the 81 misses it was given; of the addresses found, 92% verified valid and 6.5% came back catch-all or risky. Misses that stop at the first provider are the expensive mistake, which is why step 4 passes `max_cost_for_all`.

## Output

The user's list with these columns added: `domain_used, email, email_source_run, verify_status, phone, phone_type, notes`. Plus the totals above, and the misses at the bottom with the reason (no domain, not found, invalid, opted out, suppressed), so the user can see what was filtered and why.
