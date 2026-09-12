---
name: cold-email-pipeline
description: Run a cold email campaign end to end on RouterGrowth from one targeting sentence: Research, List, Grade, Verify, Write, Send. Reads a directives folder (ICP, lead source filters, negative keywords, qualification rubric, copy rules) so "target independent mortgage brokers in Lyon" becomes a graded, verified, personalised campaign sent from an inbox the workspace owns, with two human gates. Use when the user wants to launch cold outreach, build and qualify a lead list, write cold email at scale, or run the prospecting pipeline. The daily loop after the first send is the sdr-daily skill.
---

# Cold email pipeline

Six stages over a directives folder the user configures once. The stages that touch data call RouterGrowth capabilities; the stages that judge (grading, writing) run on you. Two gates: the final list and copy, and the first live send. Everything between them runs on its own.

```
Research → List → Grade → Verify → Write → Send
  brief    raw    keep    clean   per-    inbox the
           leads  ICP     list    lead    workspace
                  only            copy    owns
```

Raw lead lists are 30 to 50% wrong-ICP. Grade and Verify exist so the campaign does not email agencies, dead sites and wrong-geo firms, tank the reply rate and burn the domain.

## Before you start

- Load the core `routergrowth` skill (https://www.routergrowth.com/SKILL.md) if it is not loaded. Confirm access with the free `balance` tool or `routergrowth balance`.
- Check `directives/` exists in the working project. If not, copy the `directives/` folder next to this file into the project and ask the user to fill `icp.md`, `lead-source.md` and `email-copy.md`. Those three are mandatory; the others have sensible defaults.
- Run the free `email.inboxes`. The campaign sends from an inbox the workspace owns on a verified domain. If there is none, stop and run the cold email infrastructure setup first (`domain.search`, `domain.register`, `email.domain`, `domain.dns`, `email.inbox`: the guide at https://www.routergrowth.com/use-cases/cold-email-infrastructure), each purchase behind its own confirmation.
- Inspect `people.search`, `contact.find`, `contact.verify`, `web.scrape` and `email.send` once and show the prices. Quote the campaign as a whole before stage 2.

## Stages

### 1. Research (once per ICP)

Write `directives/research-brief.md`: what these buyers care about, the daily friction, the words they use, the events that make now the right time. Use your own web search and fetch when you have them; `web.search` and `web.scrape` when you do not or a site blocks you. Every claim in the brief carries a source URL. Reused across campaigns.

### 2. List

Translate the user's sentence through `directives/lead-source.md` into `people.search` filters:

```bash
routergrowth run -c people.search -i '{"titles":["founder","managing director"],"industries":["financial services"],"locations":["Lyon, France"],"company_headcount":["2-10","11-50"],"limit":100}' --max-cost 0.50 --wait 90 -o out/leads-raw.json
```

Or start from accounts (the `hiring-signal-outbound` skill, or `company.search` for a query and location) and search people inside them. Apply `negative-keywords.md` at search time where a filter supports it. Output: `out/leads-raw.csv`.

### 3. Grade

For each company, read its website and assign a category from `directives/qualification.md`: `ICP` to keep; `agency`, `saas`, `freelancer`, `enterprise`, `wrong-geo`, `dead-site`, `unclear` to drop or hold. Fetch with your own tool when you have one; `web.scrape` (`{"url": ...}`) when you do not. Pre-classify with the negative keywords, then read the fetched text yourself for every `unclear` row and a sample of `ICP` rows. The rubric judges, not the keywords. Output: `out/leads-graded.csv`, all rows kept with `category` and `category_reason`, so the user can audit the filter.

### 4. Verify

On `ICP` rows only:

1. Free dedupe first: `routergrowth history --file emails.txt` says who this workspace already contacted. Drop them.
2. Email missing: `contact.find` with first name, last name and company domain. No-match is released, not billed.
3. Every email: `contact.verify`. Keep `valid`; drop `invalid`; hold `catch_all` and `unknown` in their own column.
4. One row per company unless the user targets named individuals; two contacts per company at most.
5. Clean merge fields: strip legal suffixes (Inc, Ltd, SARL, Lda), fix ALL-CAPS names. A broken merge field is an instant blast tell.

Output: `out/leads-verified.csv`.

### 5. Write

Per-lead copy from `directives/email-copy.md` fused with the research brief. Rules: the first line is written from that lead (role, company, one site detail); the angle follows the tier in the directive; one call to action; plain text; 120 to 160 words; the product facts match the live site (verify, never invent a feature or a trial term). Write the J+0, J+4 and J+10 rows per lead with a `stage` column.

Output: `out/campaign.csv` with `to, first_name, company, tier, stage, subject, body`.

**Gate 1: show the count, the category breakdown, the verification breakdown, three sample emails, and the quote for the send. Wait.**

### 6. Send

1. Send one test to the user's own address from the campaign inbox and ask them to check it lands in the inbox, not in promotions or spam.
2. **Gate 2: the user confirms the first live batch.**
3. Send from the owned inbox, plain text, with a reply-to and an unsubscribe line:

```bash
routergrowth run -c email.send -i '{"inbox_id":"<id>","to":"alex@example.com","subject":"...","text":"...","reply_to":"you@yourdomain.com","unsubscribe_url":"https://yourdomain.com/unsubscribe"}' --max-cost 0.01
```

Ramp on a fresh domain: 5 to 10 a day for the first three days, 15 through day seven, then 25 to 30. Never burst: spread a day's sends across the day. Log every send to `out/sent-log.json` with the run ID, the stage and the timestamp; the `sdr-daily` skill reads it.

## Rules

- Inspect once per capability, quote the whole campaign at stage 2 and the send at Gate 1. Stop before a batch over about $1 unless the user asked for that volume.
- `max_cost` on every run, `max_total_cost` on every `batch_run`.
- Only email people the user is entitled to contact under the law that applies to them and to the recipient. B2B first-party outreach with an identifiable sender and a working opt-out is the floor; the user decides what their jurisdiction needs and the skill does not lower it.
- Never send from a shared or unverified domain. Never send HTML, images or tracking pixels in a first touch.
- Never fabricate a product fact, a number or a first line. If the research does not support a hook, use a plain one.

## Output

The four CSVs in `out/`, the sent log, and a summary: leads raw, kept after grade, kept after verify, sent, total charged, with run IDs. Then hand the loop to `sdr-daily`.
