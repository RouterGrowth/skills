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
- Run the free `linkedin.accounts` first. It lists the accounts the workspace already connected, which profile each one is, and the `account_id` to pass. If none is connected, run `linkedin.account` with a name: it returns a hosted sign-in link the user opens once. Never ask for the user's LinkedIn password.
- Ask for the target (title, company type, location), the offer in one sentence, and the daily caps if the user has them. Defaults: 20 invites a day, 20 messages a day, never both to the same person on the same day.
- Inspect `linkedin.search`, `linkedin.profile`, `linkedin.invite`, `linkedin.message` once and show the prices. Quote the day: N searches, N profiles, N invites, N messages.

## Steps

### 1. Search

```bash
routergrowth run -c linkedin.search -i '{"keywords":"head of growth fintech","location":"London","network_distance":[2,3],"account_id":"<id>","limit":25}' --max-cost 0.20 --wait 60 -o search.json
```

Keep name, headline, profile URL, company. Before anything else run the free dedupe pass: `routergrowth history --file urls.txt` with the profile URLs says who this workspace already invited or messaged. Drop them.

### 2. Read before writing

```bash
routergrowth run -c linkedin.profile -i '{"profile_url":"https://www.linkedin.com/in/example","account_id":"<id>"}' --max-cost 0.10
```

Pull the one detail the note will use: a recent role change, a post, a company event. A note without a real detail is a template; do not send templates.

### 3. Draft the notes

One per person, under 200 characters, no link, no pitch, one reason the connection makes sense. Put them in a table: name, profile URL, the detail used, the note.

**Gate 1: show the table and wait.** The user edits or approves. Nothing is sent before this.

### 4. Invite

```bash
routergrowth run -c linkedin.invite -i '{"profile_url":"https://www.linkedin.com/in/example","message":"<approved note>","account_id":"<id>"}' --max-cost 0.05
```

Up to the daily invite cap. Log each one: profile URL, date, run ID, note.

### 5. Message after accept

On the next run, `linkedin.messages` with `unread: true` and `after` set to the last run's timestamp shows who accepted and who wrote. For accepted connections that have not replied, draft one message each: the offer in two sentences, one question, no attachment.

**Gate 2: show the messages and wait.** Then:

```bash
routergrowth run -c linkedin.message -i '{"profile_url":"https://www.linkedin.com/in/example","text":"<approved message>","account_id":"<id>"}' --max-cost 0.05
```

Up to the daily message cap. Use `chat_id` instead of `profile_url` when continuing an existing thread.

### 6. Triage replies

For every reply: interested, not interested, wrong person, question, out of office. Draft a response for interested and question; the user sends it or approves it. Add not interested to the local suppression file. Never message someone who said no.

## Rules

- Caps are per account per day and shared across invites and messages. Never exceed them, and start lower on a fresh account (5 to 10 a day for the first week).
- One note per person, written from that person's profile. No bulk template, no link in a connection note.
- The agent drafts; the user approves each batch. A scheduled run may search, read and draft on its own, and may send only copy the user approved in an earlier gate.
- Respect LinkedIn's terms and the user's: this skill sends through the user's own account on a hosted connection, at human pace, with a human in the loop. It never scrapes beyond what the capabilities return and never automates likes, comments or posts.
- `max_cost` on every run. Every action logged with its run ID.

## Output

A daily briefing: invites sent (with the log), acceptances since last run, messages sent, replies by class with the drafts to approve, and the running totals for the week. Plus the CSV log the next run reads.
