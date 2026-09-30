---
name: multichannel-intent-outbound
description: >-
  Run the five-step multichannel outbound loop with RouterGrowth: find
  high-intent leads (a hiring post, a post about the problem, engagement with a
  competitor), get each person's LinkedIn, send a connection request with a note
  and a message once accepted, enrich them with a verified work email, and
  follow up by email when nobody answers, from the user's Gmail or from a
  sending domain RouterGrowth sets up and warms up. WhatsApp is an optional,
  untested last step. Use when the user wants multichannel or omnichannel
  outreach, LinkedIn plus email sequences, "find intent leads and reach them",
  a follow-up on another channel when LinkedIn goes quiet, sending domains and
  inbox warm-up for outbound, or one agent that runs outbound from signal to
  reply.
---

# Multichannel intent outbound

Five steps, one key, one balance, the channels the user already owns:

1. **Find high-intent leads.** Only people with a dated, public reason to care this week.
2. **Get their LinkedIn.** The profile is the identity everything else hangs on.
3. **Connect and message.** A note written from the signal, a message once they accept.
4. **Enrich.** A verified work email for everyone.
5. **Follow up if no answer.** Email on day 3 from a Gmail or a warmed inbox, and any reply on any channel stops everything. WhatsApp on day 5 only if the user opts in (see Optional: WhatsApp).

The agent does the finding, the reading and the drafting. Every send goes out from the user's own connected accounts, after a gate the user passes. This skill chains three others; read them for depth: `hiring-signal-outbound` and `social-lead-discovery` (step 1), `linkedin-outbound` (step 3), `sdr-daily` and `docs/daily-lifecycle.md` (the daily loop).

## Before you start

- Load the core `routergrowth` skill (https://www.routergrowth.com/SKILL.md) if it is not loaded. Confirm access with the free `balance` tool or `routergrowth balance`, without printing credentials.
- Check the channels with the free listings: `linkedin.accounts`, then the email side: `gmail.accounts` for the user's own Gmail, `email.inboxes` for RouterGrowth inboxes on a domain the user owns, and `email.warmup_status` for how those inboxes are warming. Ignore rows whose status is `EXPIRED` or `PENDING`. A missing LinkedIn or Gmail is connected with `linkedin.account` or `gmail.account` and a `name`: each returns a hosted sign-in link (Google OAuth) the user opens once. Never ask for a password. Say that a connected account is billed monthly (the `inspect` note gives the amount) before connecting one.
- Pick the email route with the user (details under Email setup): their own Gmail for low volume from their real address, or a dedicated sending domain with inboxes that warm up before the first cold email. Never send cold email from the company's main domain.
- Ask for: the signal (the role they hire for, the problem phrase they post about, or the competitor they engage with), the buyer (titles and seniority that sign), the geography, the offer in one sentence, and the daily caps. Defaults: 20 LinkedIn actions a day per account, 30 emails a day per mailbox (never more than the inbox's warm-up target), and the cadence day 0 LinkedIn, day 3 email.
- Keep the state on the workspace when it can. `routergrowth features` shows whether workspace tables are on (the user turns them on with `routergrowth features --enable tables`; it is their choice, because it changes how sends behave). With tables on: one table per campaign (`routergrowth rows upsert outbound -f leads.json`, keyed on email or LinkedIn URL, so a person found twice stays one row), `routergrowth suppress add <email or LinkedIn URL> --reason not_interested` for anyone who says no, bounces or asks to stop, and the server then refuses any send to a suppressed person and any repeat first message to someone the workspace already contacted on that channel in the last 30 days (`409 repeat_touch`, not charged). Every agent on the workspace shares the same list. Docs: https://www.routergrowth.com/docs/api/tables.md
- With tables off, keep three files in the folder the user names (ask once): `outbound/leads.csv` (one row per person, the columns under Output), `outbound/log.csv` (date, channel, action, person, run_id, text, status) and `outbound/suppressed.txt` (anyone who said no, bounced or asked to stop, on every channel).
- Inspect every capability the run will touch, once, and quote the batch before the first billable run: N leads, N profile reads, N invites, N email lookups and verifications, N phone lookups at most, N sends per channel. Get a yes on the total. A scheduled or delegated run treats the budget the caller set as the approval, stops at it and reports.

## 1. Find high-intent leads

Pick one signal source per run; the lead table records which one produced each row. A signal you will check again every week goes into a watch: `POST /v1/watch` (or the MCP `watch` tool) saves the query and runs it once, and each weekly refresh (`POST /v1/watch/{id}/refresh`) returns only the new and changed postings or posts, so the loop never re-reads last week's leads. With tables on, pass `into` and every refresh lands its new records as rows. Docs: https://www.routergrowth.com/docs/api/watch.md

| The signal | How to get it | Then |
| --- | --- | --- |
| Hiring for the role you sell to | `company.jobs` by title and location, `company.search` for the domain and headcount | `people.search` with `company_domains` for the buyer (hiring-signal-outbound) |
| Posting about the problem | `social.search` on X, LinkedIn, Reddit, YouTube, TikTok or Instagram with a phrase a buyer would write | read the post, keep the buyers, `social.profile` for the website (social-lead-discovery) |
| Engaging a competitor | `social.comments` on the competitor's recent posts | the commenters who ask, compare or complain |
| Money to spend | `company.funding` on the accounts you already have | the buyer at each, as for hiring |

```bash
routergrowth run -c people.search -i '{"company_domains":["acme.com"],"titles":["Founder","CEO","Head of Growth"],"seniority":["cxo","owner","vp","director"],"limit":2}' --max-cost 0.30 --wait 120
```

With a domain, `people.search` bills per person returned and carries the LinkedIn URL and, when known, a work email. Qualify by reading, not by keyword: drop vendors, recruiters, students, competitors and anyone who is not the buyer. Every kept row carries the signal text, its date and its URL. No signal, no lead. Then run the free dedupe: `routergrowth history --file people.txt` and drop everyone this workspace already `contacted` on any channel, plus everyone suppressed (`routergrowth suppress list`, or `suppressed.txt` with tables off).

## 2. Get their LinkedIn

Rows from `people.search` already carry `linkedin_url`. For the rest (a lead from a post, a comment or a job ad):

```bash
routergrowth run -c linkedin.search -i '{"keywords":"<first> <last> <company>","account_id":"<id>","limit":10}' --max-cost 0.05 --wait 60
```

Accept a match only when the headline names the company or the role the signal showed; two plausible rows means no match. `person.enrich` with a work email is the second route when you already have one. A lead with no LinkedIn skips step 3 and starts on email in step 5.

Read the profile of everyone you will write to, with `full: true` (LinkedIn throttles full reads, so only them):

```bash
routergrowth run -c linkedin.profile -i '{"profile_url":"https://www.linkedin.com/in/example","full":true,"account_id":"<id>"}' --max-cost 0.05 --wait 60
```

Keep `provider_id` (the invite and message accept it), `degree` (1 means already connected: skip the invite, go to the message) and the one detail the note will use.

## 3. Connect and message

Draft one note per person, under 300 characters: the signal in their words, one reason to connect, no link, no pitch. The offer waits for the message.

**Gate 1: show the table (person, signal, detail, note) and wait.** Nothing is sent before the user approves it.

Check headroom with the free `linkedin.invitations_sent` and send no more than the lower of `remaining_today` and the daily cap:

```bash
routergrowth run -c linkedin.invite -i '{"provider_id":"<id>","message":"<approved note>","account_id":"<id>"}' --max-cost 0.05 --wait 60
```

Stop the batch at the first `provider_rate_limited`. Log every invite with its run ID. On later runs, `linkedin.profile` shows `degree` 1 once someone accepted: draft one message each (the offer in two sentences, one question, still anchored on the signal), **Gate 2**, then `linkedin.message` with the approved text. Details, caps and reply reading: `linkedin-outbound`.

## 4. Enrich

Enrich in the order the channels need it, so nobody pays for data a reply made useless.

- **Work email, for everyone.** Use the email `people.search` returned, or `contact.find` with first name, last name and the company domain (a miss is released, not billed). Then `contact.verify` every address before it touches a sender: keep `valid`, drop `invalid`, hold `catch_all` and `unknown` in their own column and do not email them without the user's say.

```bash
routergrowth run -c contact.find -i '{"first_name":"Alex","last_name":"Rivera","company_domain":"acme.com"}' --max-cost 0.10
routergrowth run -c contact.verify -i '{"email":"alex.rivera@acme.com"}' --max-cost 0.02
```

- **No mobile by default.** A phone number is only needed for the optional WhatsApp step; see Optional: WhatsApp.

## Email setup

Pick one route before the first email goes out, and write it down with the campaign.

- **The user's Gmail.** `gmail.accounts`, or `gmail.account` to connect one. Their real address, already warm, fine for a few follow-ups a day. Keep it well under the daily cap and never blast from it.
- **A dedicated sending domain with warmed inboxes**, for real volume without risking the main domain. Each step quotes before it spends, and the user approves the total once:

```bash
routergrowth run -c domain.search -i '{"name":"getacme"}' --max-cost 0.01          # a lookalike of the main domain
routergrowth run -c domain.register -i '{"domain":"getacme.com"}' --max-cost 30     # WHOIS privacy on; or bring a domain the user owns
routergrowth run -c email.domain -i '{"domain":"getacme.com"}' --max-cost 3         # the SPF, DKIM, DMARC and MX records to add
routergrowth run -c domain.dns -i '{"domain":"getacme.com","records":[…]}' --max-cost 0.01   # writes them, for a domain bought through RouterGrowth
routergrowth run -c email.domain -i '{"domain":"getacme.com"}' --max-cost 3         # again: a free re-check until it reports verified
routergrowth run -c email.inbox -i '{"name":"alex","domain":"getacme.com"}' --max-cost 3
routergrowth run -c email.warmup -i '{"inbox_id":"<id>","emails_per_day":20,"ramp_up":"slow","timezone":"Europe/Paris"}' --max-cost 10
routergrowth run -c email.warmup_status -i '{"inbox_id":"<id>"}'                    # free: health grade and 14-day inbox placement
```

`email.domain` returns the DNS records; `domain.dns` writes them on a domain registered through RouterGrowth, and a domain the user brings needs them added at their own registrar. Then run `email.domain` again (the re-check is free) until it reports verified. `email.warmup` puts the inbox on a network of real mailboxes that open, reply and pull its mail out of spam, on a ramp to the daily volume set, weekdays 8am to 6pm in the timezone given. Set `emails_per_day` to the cold volume planned for that inbox (50 at most) and `ramp_up: slow` for a domain registered in the last few weeks. It renews every 30 days; `action: pause`, `resume` or `stop` (stop ends the billing).

**No cold email from an inbox that is still warming.** Check `email.warmup_status` first: send only once its ramp has reached the target volume and its warm-up mail lands in the inbox rather than spam over the last 14 days (a new domain usually needs two to three weeks). Keep the warm-up running while the campaign sends, and keep each inbox's cold sends at or under its warm-up target. Several inboxes on one or two domains spread the volume.

## 5. Follow up if no answer

Every run starts by reading every inbox in use since the last run, before any new send: `linkedin.messages` with `unread: true` and `after`, `gmail.messages` with `after` (or `email.messages` for a RouterGrowth inbox), and `whatsapp.messages` with `unread: true` and `after` if WhatsApp is on. A reply on any channel ends every remaining step for that person on every channel. An inbox that cannot be read means unknown, not silence: hold that person's next step and say why.

| Day | Channel | When | Capability |
| --- | --- | --- | --- |
| 0 | LinkedIn | invite with the note; message once accepted | `linkedin.invite`, `linkedin.message` |
| 3 | Email | no reply on LinkedIn (accepted or still pending), verified email only, from the Gmail or a warmed inbox | `gmail.send` or `email.send` |
| 5 or later (optional) | WhatsApp | only if the user turned WhatsApp on; see Optional: WhatsApp | `whatsapp.message` |

The email is short: a subject that names the signal, three sentences, one question, no attachment, a plain way to say no.

**Gate 3: show every follow-up (person, channel, sender, text) and wait.** An approval covers one exact message to one person on one channel; change any of them and it is void.

```bash
routergrowth run -c gmail.send -i '{"to":["alex.rivera@acme.com"],"subject":"<approved subject>","text":"<approved body>","account_id":"<id>"}' --max-cost 0.05 --wait 60
routergrowth run -c email.send -i '{"inbox_id":"<warmed inbox>","to":["alex.rivera@acme.com"],"subject":"<approved subject>","text":"<approved body>"}' --max-cost 0.02 --wait 60
```

Reply in the same thread when one exists: `in_reply_to` with the `message_id` from `gmail.messages` or `email.messages`, `chat_id` from `linkedin.messages`.

Triage every reply: interested, question, not now, wrong person, not interested, out of office. Draft a response for interested and question for the user to approve. Not interested, a bounce or a request to stop is suppressed (`routergrowth suppress add`, or `suppressed.txt` with tables off) and ends every channel for that person.

## Optional: WhatsApp

Off by default. The WhatsApp capabilities exist, but this step has not been tested end to end with RouterGrowth yet: say so, and run it only when the user turns it on for this campaign. Ask once whether WhatsApp cold follow-ups are acceptable for their market and their own policy; many teams keep it for people who accepted on LinkedIn.

When it is on: connect the account with `whatsapp.accounts` and `whatsapp.account` (a hosted QR or pairing code, billed monthly), cap it at 10 messages a day, and only on day 5 or later, only for the people still silent after the email:

```bash
routergrowth run -c contact.phone -i '{"profile_url":"https://www.linkedin.com/in/example"}' --max-cost 0.30
routergrowth run -c whatsapp.profile -i '{"phone":"+14155550123","account_id":"<id>"}' --max-cost 0.02 --wait 60
routergrowth run -c whatsapp.message -i '{"phone":"+14155550123","text":"<approved message>","account_id":"<id>"}' --max-cost 0.05 --wait 60
```

`contact.phone` bills only when a number is found and is the most expensive call in the loop, so never run it up front. A number that is not on WhatsApp comes back from `whatsapp.profile` as an unbilled no-match and ends the sequence for that person. The message is two lines, who you are and the one question, behind Gate 3 like every other send. Report anything that behaves unexpectedly back to the user rather than retrying.

## Rules

- Inspect once per capability, quote the batch, then run. `max_cost` on every run and `--wait 60` on every send example (a bare `run` returns a receipt, not a result). Stop and ask before a batch over about $1 unless the user asked for that volume.
- Nothing is sent without its gate. A scheduled run may search, read, enrich and draft on its own, and may send only copy the user approved for that exact person and step.
- One active sequence per person, one message per channel per step, never two channels on the same day. Caps count new sends only; reading inboxes is always complete.
- Never invent a last name, a LinkedIn match, an email or a number. Never email an unverified address. Never buy a phone number for someone who already replied.
- Start slow on fresh accounts (5 to 10 LinkedIn actions a day for the first week), never send cold email from an inbox that is still warming, and respect LinkedIn's, Google's and WhatsApp's own limits: the first `provider_rate_limited` stops that channel for the day.
- Never present sandbox (`rg_test_`) output as real data. Every row carries the run IDs behind it. Report cost as the sum of every run's `billing.charged`, not a wallet difference.

## Output

One row per person, in the workspace table (tables on) or `outbound/leads.csv`: `name, title, company, domain, signal, signal_date, signal_url, linkedin_url, provider_id, degree, email, verify_status, sender, stage, last_touch, next_touch, replied_on, run_ids, charge` (plus `phone, on_whatsapp` when WhatsApp is on). `stage` is one of `found, invited, connected, messaged, emailed, whatsapped, replied, suppressed`; with tables on it is the row's `status` and `next_touch` its `next_at`, so `routergrowth rows outbound --due` lists who is up today.

A daily briefing: replies by channel with the drafts to approve, invites accepted, sends done per channel against the caps, each sending inbox's warm-up state, follow-ups due tomorrow, people suppressed, and the day's total charged with the run IDs.

## What a lead costs

Checked with `inspect` on 30 September 2026; run `inspect` again before quoting, prices move. A person found through `people.search` with a domain is $0.042 with the email when known; a LinkedIn profile read $0.002; an invite or a LinkedIn message $0.00875; `contact.find` $0.04375 per match and nothing on a miss; `contact.verify` $0.010938 a verdict; `gmail.send` $0.00875 and `email.send` $0.0035 a send. A lead worked to the email step costs about $0.12.

The sending setup is a one-off per domain and inbox: `domain.search` $0.002, a domain about $21 to $23 a year depending on the extension (quoted live by `domain.register`), `email.domain` $2.3275, `domain.dns` $0.002 a call, `email.inbox` $2.3275, and `email.warmup` $9.3275 per inbox per 30 days at 20 a day (`email.warmup_status` is free).

With WhatsApp on: `contact.phone` $0.21875 per number found, `whatsapp.profile` $0.002, `whatsapp.message` $0.00875, so a lead that goes all the way costs about $0.35, most of it the phone lookup, which is why it runs last and only for the people still silent.
