## What this adds or changes

One skill per PR. Say which job it finishes and for whom.

## Checklist

- [ ] `python3 scripts/check_skills.py` passes (strict YAML frontmatter, name matches folder, no em dashes)
- [ ] Every capability and input field named in the skill exists in the catalog
- [ ] A human gate sits before anything that leaves the workspace
- [ ] Prices are quoted at run time (`inspect`), not written into the file
- [ ] No keys, personal data or client names anywhere in the diff

## Ran on a real account

Which agent, what it cost, what broke. A skill that has not run is not ready to merge.
