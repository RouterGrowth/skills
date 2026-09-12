# Directives

These files are the brain of the pipeline. Configure them once per ICP, then drive the pipeline in plain language. When the user says "target B2B mortgage brokers in Lyon", the pipeline reads these to know who that means, how to search, what to filter out, how to qualify and how to write.

## Setup (once)

1. Copy this folder into the working project as `directives/`.
2. Fill, in this order: `icp.md` (mandatory), `lead-source.md` (mandatory), `email-copy.md` (mandatory), `negative-keywords.md` (strongly recommended), `qualification.md` (the defaults are sensible).
3. Leave `research-brief.md` empty; the Research stage writes it.
4. Keep the folder in version control. It improves with every campaign.

Write them the way you would brief a sharp new SDR: concrete, opinionated, with examples. Vague directives produce vague targeting.

## Who reads what

| Stage | Reads |
| --- | --- |
| Research | `icp.md`, writes `research-brief.md` |
| List | `icp.md`, `lead-source.md`, `negative-keywords.md` |
| Grade | `qualification.md`, `negative-keywords.md` |
| Verify | nothing (mechanical) |
| Write | `email-copy.md`, `research-brief.md`, `icp.md` |
| Send | `email-copy.md` (sender identity, opt-out line) |
