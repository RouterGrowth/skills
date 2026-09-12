---
name: sdr-daily
description: >-
  Run one day of the SDR loop on a RouterGrowth cold email campaign: read the
  campaign inbox and triage replies (email.messages), keep the suppression list
  current, send the follow-ups that are due and drip the next first-touch emails
  from an approved queue (email.send) inside a daily cap, then write the morning
  briefing. Nothing new goes out without approval; the drip and the follow-ups
  come from copy approved at the cold-email-pipeline gates. Use when the user
  says "run the SDR", "daily briefing", "who replied", "send today's batch",
  "check the campaign", or wants to advance an outreach campaign by one day.
---

# SDR daily

One day of a Sales Development loop. You do the mechanical work (read, classify, send what was already approved), surface the few human decisions, and hand back a short briefing. You run from the campaign folder the `cold-email-pipeline` skill produced: `out/campaign.csv`, `out/sent-log.json`, `out/replied.json`.

## Before you start

- Load the core `routergrowth` skill (https://www.routergrowth.com/SKILL.md) if it is not loaded. Confirm access with the free `balance` tool or `routergrowth balance`.
- Establish, once per campaign and reuse after: `CAMPAIGN_CSV` (the approved rows with a `stage` column: J+0, J+4, J+10), `INBOX_ID` (from the free `email.inboxes`), `DAILY_CAP` (default 30, all stages together), `LAST_RUN` (the timestamp of the previous run, from the sent log).
- If `out/replied.json` does not exist, create it as `[]`.

## The one rule

**Nothing new goes out without approval.** The drip and the follow-ups are not new: their copy and targeting were approved at Gate 1 of the pipeline, and the domain passed the test send at Gate 2. So, without asking, you may: drip first-touch from the approved queue inside the cap, send due follow-ups, read and classify replies, draft responses, update the suppression file, run diagnostics. You may not: send a reply to a prospect (draft it, the user sends), start a queue whose copy was not approved, exceed the cap, or email anyone in `replied.json`.

## Run order

### 1. Triage replies

```bash
routergrowth run -c email.messages -i '{"inbox_id":"<id>","after":"<LAST_RUN>","limit":100}' --max-cost 0.05 --wait 30 -o out/inbox.json
```

Read every message that is a reply to a campaign email (match on the sender and the thread). Classify:

| Class | Action |
| --- | --- |
| Interested | Draft a reply for the user to approve. Add to `replied.json` (stops follow-ups). |
| Not interested | Add to `replied.json`. No response. |
| Wrong contact | Note the redirect, propose the named person. Add the original to `replied.json`. |
| Auto-reply or out of office | Do not suppress. Note the return date. |
| Unsubscribe request | Add to `replied.json` immediately. Never contact again. |
| Ambiguous | Show verbatim. Do not guess. |

Also read bounce notices in the inbox: a hard bounce goes to `replied.json` with `reason: bounce`.

### 2. Hygiene

Count bounces since `LAST_RUN`. Any spam complaint, or bounces above 5% of sends, is the kill switch: recommend pausing the drip until the list and copy are reviewed, and do not drip today.

### 3. Follow-ups due

From `out/sent-log.json`, a J+0 sent 4 or more days ago with no reply and no J+4 is due for J+4; a J+4 sent 6 or more days ago with no reply is due for J+10. Skip anyone in `replied.json`. Send the due rows, oldest first, threaded on the original:

```bash
routergrowth run -c email.send -i '{"inbox_id":"<id>","to":"alex@example.com","subject":"Re: <original subject>","text":"<approved J+4 body>","in_reply_to":"<message id of the J+0>","reply_to":"you@yourdomain.com","unsubscribe_url":"..."}' --max-cost 0.01
```

Count them as F. Follow-ups are time-sensitive and take the first claim on the cap.

### 4. First-touch drip

Budget: `DRIP = DAILY_CAP - F`. If positive, send the next `DRIP` J+0 rows that are not in the sent log and not in `replied.json`. Before the send, the free `routergrowth history --file today.txt` on today's addresses confirms nobody was contacted from another campaign in this workspace.

Spread the sends across the day rather than in one burst. On a fresh domain, ramp the cap: 5 to 10 a day for days one to three, 15 through day seven, then 25 to 30. Log every send with its run ID, stage and timestamp.

When the queue is empty, say so and suggest running `cold-email-pipeline` for the next batch.

### 5. Briefing

```
SDR briefing, <date>, <campaign>

Interested (<n>): drafts below, your approval to send
  - <company> (<name>): "<gist>"
Not interested (<n>) suppressed. Redirects (<n>). Unsubscribes (<n>).

Sent today: <F + DRIP> of <DAILY_CAP>
  - Follow-ups <F>, first-touch <DRIP>, queue remaining <n> (about <days> days)

Hygiene: bounces <n>, complaints <n>, domain OK or AT RISK

Your decisions today
  1. Approve or edit <n> reply drafts (below)
  2. <replenish the queue, pause, anything else human>

Charged today: $<total> across <n> runs
```

Then the reply drafts, one per interested thread.

## Rules

- One daily cap across drip and follow-ups. Never exceed it.
- Suppression is sacred: anyone who replied (other than an auto-reply) is never contacted again by this campaign.
- Reply responses are drafted, never auto-sent, even on a scheduled run.
- Honesty on signal: zero replies in week one is normal; a booking that predates the campaign is not a result.
- `max_cost` on every run. Every send logged with its run ID.

## Scheduling

Once the user trusts the drafts (a week or two of manual runs), this skill can run each weekday morning on a schedule. The scheduled run drips, follows up, triages and briefs on its own, and still only drafts responses.
