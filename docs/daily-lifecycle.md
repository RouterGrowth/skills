# The daily lifecycle pattern

Several skills here (sdr-daily, linkedin-drafts, intent-messaging, community-help-drafts) run as a daily loop rather than a one-off. The loop has a shape that keeps a scheduled agent safe. Copy it when you write one.

## Monitor before you source

Every run starts with what is not finished: drafts the user has not sent yet, messages the user sent without a reply, threads the user posted in. Reconcile what happened (accepted, replied, bounced, removed) before drafting anything new. On RouterGrowth the free `list_workspace_events` tool answers most of it in one call: replies, bounces, complaints, new LinkedIn connections and dropped sessions since your last cursor. A run that only reports what it drafted today is incomplete.

## Unknown is not "no reply"

When an inbox, a thread or a provider cannot be checked, record the state as unknown, hold every action that depends on it, and report the blocker. Never infer silence from a failed check.

## Nothing goes out unapproved

An approval covers the messages the user saw, exactly as shown: one recipient, one channel, one subject, one body, one sequence step each. Edit any of them and that approval is void. Email can then go out through RouterGrowth, one at a time; LinkedIn, Instagram and WhatsApp stay drafts the user sends. A scheduled run drafts and never sends.

## A reply stops the sequence

Any reply, decline, bounce, unsubscribe, hard bounce, suppression or manual stop ends every remaining step for that person. If a reply arrives while a draft is waiting, drop the draft and hand the thread to the human. A person who opted out with RouterGrowth (a lookup answers no_match saying so) is out for good.

## One active sequence per person

Dedupe on the identifiers you have (email, LinkedIn URL, domain, permalink) before searching, enriching or drafting. RouterGrowth's free `get_subjects_history` tool answers "has this workspace already touched this subject" across every capability, so a person drafted for by one skill is not drafted for again by another.

## Caps are on new work, not on monitoring

Daily caps limit new sourcing, new drafts and new sends. Monitoring, reconciliation and reply triage are always complete and never count against a cap.

## Every external call carries its receipt

Tool, price, actual charge, run ID, timestamp, result (`list_runs` reads them back for free). The briefing sums them. A run that cannot show its receipts did not happen.
