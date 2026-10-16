---
# Copy this file to skills/<your-skill-name>/SKILL.md and replace every line.
# It is not a skill itself: installers scan for SKILL.md files, which is why it does not carry that name here.
name: your-skill-name
description: >-
  One paragraph. What the skill does, in what order, and the phrases a user
  would say that mean they want it ("build a list of", "audit our", "draft
  the follow-ups"). This is the trigger, so be concrete.
---

# Your skill name

One sentence on the job and the shape of the result.

## Before you start

- The core `routergrowth` skill in this plugin carries the connector's tools and the spending rules.
- Confirm the connector works with the free `get_workspace_balance` tool. If the RouterGrowth tools are missing, ask the user to connect RouterGrowth and approve a workspace.
- Ask for the inputs this skill needs (the ICP, the brand, the domain) if the user has not given them.

## Steps

### 1. Name the step

What it does. The tool it calls and the input, for example `company_enrich` with `{"input": {"domain": "example.com"}, "max_cost": "0.10"}`.

What to keep from the result, what to drop.

### 2. Next step

## Rules

- Check the price with `get_operation_pricing` before the first paid call of a kind, and quote the total for a run of calls, not each item.
- `max_cost` on every paid call. Stop and ask before a run likely above about $1 unless the user asked for that volume.
- Never present simulated (sandbox) output as real data. Never fabricate a number: every figure carries its source or an "estimate" label.
- Never post, comment, like, send or automate engagement anywhere. Measure and draft; a human publishes and sends.

## Human gates

- Before spending beyond the agreed budget: show the plan and the price, and wait.
- Messages go out only after the user approved them as shown: email one at a time, other channels as drafts the user sends.

## Output

What the user gets: a file, a table, a briefing, in what shape.
