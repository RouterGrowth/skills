# Directives

These files are the brain of the pipeline. Configure them once per ICP, then drive the pipeline in plain language. When the user says "independent mortgage brokers in Lyon we met at the trade show", the pipeline reads these to know who that means, why the user may write to them, how to search, what to filter out, how to qualify and how to write the drafts.

## Setup (once)

1. Copy this folder into the working project as `directives/`.
2. Fill, in this order: `icp.md` (mandatory, including the reason to contact), `lead-source.md` (mandatory), `email-copy.md` (mandatory), `negative-keywords.md` (strongly recommended), `qualification.md` (the defaults are sensible).
3. Leave `research-brief.md` empty; the Research stage writes it.
4. Keep the folder in version control. It improves with every list.

Write them the way you would brief a sharp new SDR: concrete, opinionated, with examples. Vague directives produce vague targeting.

## Who reads what

| Stage | Reads |
| --- | --- |
| Research | `icp.md`, writes `research-brief.md` |
| List | `icp.md`, `lead-source.md`, `negative-keywords.md` |
| Grade | `qualification.md`, `negative-keywords.md` |
| Verify | nothing (mechanical) |
| Draft | `email-copy.md`, `research-brief.md`, `icp.md` |

The pipeline ends at the drafts. The user sends them from their own mail tool.
