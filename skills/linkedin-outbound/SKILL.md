---
name: linkedin-outbound
description: >-
  Run a LinkedIn outbound loop with RouterGrowth on a LinkedIn account the user
  connected: search people (linkedin.search), read the profile before writing
  (linkedin.profile), send a connection request with a short note
  (linkedin.invite), message once accepted (linkedin.message), read and triage
  replies (linkedin.messages), inside daily caps. Use when the user wants
  LinkedIn outreach, connection requests at scale with a human gate, wants to
  message people who accepted, asks "who replied on LinkedIn", or wants to work
  a LinkedIn list.
---

# LinkedIn outbound

One connected LinkedIn account, a target search, a daily budget of invites and messages, and a human who approves every batch of copy before it goes out. The agent does the search, the reading and the drafting; the invites and messages go out only after the gate.

## Before you start

- Load the core `routergrowth` skill (https://www.routergrowth.com/SKILL.md) if it is not loaded. Confirm access with the free `balance` tool or `routergrowth balance`.
- Run the free `linkedin.accounts` first. It lists the accounts the workspace already connected, which profile each one is, and the `account_id` to pass; ignore rows whose status is `EXPIRED` or `PENDING` (a sign-in link that was never finished). If none is connected, run `linkedin.account` with a name: it returns a hosted sign-in link the user opens once. Never ask for the user's LinkedIn password.
- Ask for the target (title, company type, location), the offer in one sentence, and the daily caps if the user has them. Default: 20 actions a day per account, invites and messages together, never both to the same person on the same day. Keep the log at `linkedin/log.csv` (columns: date, action, profile_url, provider_id, run_id, note_or_message, status) and the suppression list at `linkedin/suppressed.txt`, relative to the folder the user names; ask once.
- Inspect `linkedin.search`, `linkedin.profile`, `linkedin.invite`, `linkedin.message` once and show the prices. Quote the day: N searches, N profiles, N invites, N messages.

## Steps

### 1. Search

```bash
routergrowth run -c linkedin.search -i '{"keywords":"head of growth fintech","location":["London"],"network_distance":[2,3],"account_id":"<id>","limit":10}' --max-cost 0.05 --wait 60 -o search.json
```

A search costs a fraction of a cent. `location`, `company` and `industry` take place or company names as well as LinkedIn ids; a name resolves to its first LinkedIn match ("London" becomes "London Area, United Kingdom"), so use the name LinkedIn shows for the place you mean. A name that matches nothing is dropped, the search still runs, and the result carries `dropped_filters` and a `note`: check for them before trusting the list, and fall back to a broader place name, the id, or the city in `keywords`. Classic search returns a page of 10 whatever the limit and bills the page; use `cursor` for the next one. Rows carry `provider_id`, `public_identifier`, `profile_url`, `name`, `headline`, `location`, `degree`: the company is in the headline, and `location` comes back in the account's own LinkedIn language ("Londres, Angleterre, Royaume-Uni" on a French account), so never filter rows on an English place string. Expect noise (a "Head of People" for a growth search, an anonymous "LinkedIn Member" row): the profile read in step 2 is what qualifies a row, not the search. Keep name, headline, profile URL. Before anything else run the free dedupe pass: `routergrowth history --file urls.txt` with the profile URLs and read the `contacted` column, which is who this workspace already invited or messaged; drop them. `seen` is always yes right after a search and means nothing here.

### 2. Read before writing

```bash
routergrowth run -c linkedin.profile -i '{"profile_url":"https://www.linkedin.com/in/example","full":true,"account_id":"<id>"}' --max-cost 0.10 --wait 60
```

The profile read returns `provider_id`, which `linkedin.invite` and `linkedin.message` accept in place of the URL. Without `full: true` it carries only the name, headline, location, degree and counts; `full` adds the summary, the work history and the skills (LinkedIn throttles it, so read at most the people you will write to). There is no posts field. Pull the one detail the note will use: a recent role change, a company event, a line from the summary. A note without a real detail is a template; do not send templates.

### 3. Draft the notes

One per person, under 300 characters (LinkedIn's cap; shorter reads better), no link, no pitch, one reason the connection makes sense. The offer sentence belongs in the step 5 message, not in the note. Put them in a table: name, profile URL, the detail used, the note.

**Gate 1: show the table and wait.** The user edits or approves. Nothing is sent before this.

### 4. Invite

```bash
routergrowth run -c linkedin.invite -i '{"profile_url":"https://www.linkedin.com/in/example","message":"<approved note>","account_id":"<id>"}' --max-cost 0.05 --wait 60
```

Before the batch, run the free headroom check:

```bash
routergrowth run -c linkedin.invitations_sent -i '{"account_id":"<id>"}' --wait 60
```

It counts the account's pending invitations over the last 24 hours and 7 days and returns `remaining_today`, the most to send now (LinkedIn allows roughly 100 a day and 200 a week). Send no more than the lower of `remaining_today` and the daily invite cap; when it is 0, send nothing and say so. The counts are a floor (accepted and withdrawn invitations leave the pending list), so the user's own cap still rules. Stop the batch at the first `provider_rate_limited`; it bills nothing and is never retried.

Up to the daily invite cap. Log each one: profile URL, date, run ID, note.

### 5. Message after accept

On the next run, `linkedin.messages` with `unread: true` and `after` set to the last run's timestamp lists the conversations with something new, each with the person's `name`, `profile_url`, `headline` and `degree`; an empty list means nobody wrote, and is a success, not an error. Acceptance is not in the inbox: `linkedin.profile` on each invited person shows `degree` 1 (`connected: true`) once they accepted. For accepted connections that have not replied, draft one message each: the offer in two sentences, one question, no attachment.

**Gate 2: show the messages and wait.** Then:

```bash
routergrowth run -c linkedin.message -i '{"profile_url":"https://www.linkedin.com/in/example","text":"<approved message>","account_id":"<id>"}' --max-cost 0.05 --wait 60
```

Up to the daily message cap. Use `chat_id` instead of `profile_url` when continuing an existing thread.

### 6. Triage replies

Read each conversation with `chat_id`: messages carry `text`, `sent_by_me`, `sender_name`, `sender_profile_url` and `sent_at`. For every reply: interested, not interested, wrong person, question, out of office. Draft a response for interested and question; the user sends it or approves it. Add not interested to `linkedin/suppressed.txt`. Never message someone who said no.

## Rules

- Caps are per account per day and shared across invites and messages. Never exceed them, and start lower on a fresh account (5 to 10 a day for the first week).
- One note per person, written from that person's profile. No bulk template, no link in a connection note.
- The agent drafts; the user approves each batch. A scheduled run may search, read and draft on its own, and may send only copy the user approved in an earlier gate.
- Respect LinkedIn's terms and the user's: this skill sends through the user's own account on a hosted connection, at human pace, with a human in the loop. It never scrapes beyond what the capabilities return and never automates likes, comments or posts.
- `max_cost` on every run, `--wait 60` on every example (a bare `run` returns a receipt, not a result). Every action logged with its run ID. Report the day's cost as the sum of every run's `billing.charged`, not a wallet difference: the balance is shared by every session on the key.

## Output

A daily briefing: invites sent (with the log), acceptances since last run, messages sent, replies by class with the drafts to approve, and the running totals for the week. Plus the CSV log the next run reads.
