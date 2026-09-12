# The daily lifecycle pattern

Several skills here (sdr-daily, linkedin-outbound, community-help-drafts) run as a daily loop rather than a one-off. The loop has a shape that keeps a scheduled agent safe. Copy it when you write one.

## Monitor before you source

Every run starts by inspecting everything the previous runs did that is not finished: invitations pending, emails sent without a reply, threads posted in. Reconcile what happened (accepted, replied, bounced, removed) before creating anything new. A run that only reports what it created today is incomplete.

## Unknown is not "no reply"

When an inbox, a thread or a provider cannot be checked, record the state as unknown, hold every action that depends on it, and report the blocker. Never infer silence from a failed check.

## An approval is tied to one exact message

An approval covers one recipient, one channel, one sender, one subject, one body, one sequence step. Change any of them and the approval is void. Never reuse an approval for another step. Drafting never authorizes sending.

## A reply stops the sequence

Any reply, decline, bounce, unsubscribe, hard bounce, suppression or manual stop ends every remaining automated step for that person. If a reply arrives while a draft is waiting for approval, drop the draft and hand the thread to the human.

## One active sequence per person

Dedupe on the identifiers you have (email, LinkedIn URL, domain, permalink) before searching, enriching or drafting. RouterGrowth's free `history` call answers "has this workspace already touched this subject" across every capability, so a person contacted by one skill is not contacted again by another.

## Caps are on new work, not on monitoring

Daily caps limit new sourcing and new sends. Monitoring, reconciliation and reply triage are always complete and never count against a cap.

## Every external call carries its receipt

Provider, quoted price, actual charge, run ID, timestamp, result. The briefing sums them. A run that cannot show its receipts did not happen.
