---
# Copy this file to skills/<your-skill-name>/SKILL.md and replace every line.
# It is not a skill itself: installers scan for SKILL.md files, which is why it does not carry that name here.
name: your-skill-name
description: >-
  One paragraph. What the skill does, in what order, and the phrases a user
  would say that mean they want it ("build a list of", "audit our", "send the
  batch"). This is the trigger, so be concrete.
---

# Your skill name

One sentence on the job and the shape of the result.

## Before you start

- Load the core `routergrowth` skill (https://www.routergrowth.com/SKILL.md) if it is not already loaded. It carries the CLI, HTTP and MCP contract and the spending rules.
- Confirm access without printing credentials: the free `balance` tool, or `routergrowth balance`.
- Ask for the inputs this skill needs (the ICP, the brand, the domain) if the user has not given them.

## Steps

### 1. Name the step

What it does. The capability it calls and the input:

```bash
routergrowth inspect -c capability.name
routergrowth run -c capability.name -i '{"field":"value"}' --max-cost 0.05
```

What to keep from the result, what to drop.

### 2. Next step

## Rules

- Inspect once per capability and show the price before the first billable run. For a homogeneous batch, quote the batch total, not each item.
- `max_cost` on every run, `max_total_cost` on every batch. Stop and ask before a batch over about $1 unless the user asked for that volume.
- Never present sandbox (`rg_test_`) output as real data. Never fabricate a number: every figure carries its source or an "estimate" label.
- Never post, comment, like or automate engagement anywhere. Measure and draft; a human publishes.

## Human gates

- Before anything leaves the workspace: show the list, the copy or the order, and wait.

## Output

What the user gets: a file, a table, a briefing, in what shape.
