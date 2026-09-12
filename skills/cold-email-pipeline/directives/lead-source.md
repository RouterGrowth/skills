# Lead source

How a targeting sentence becomes `people.search` (or `company.search`) filters.

## Default filters

- titles: (the titles that map to "roles to reach" in icp.md)
- seniority: (owner, founder, c-level, vp, head, director, manager)
- industries: (the industry labels that match the firm type)
- company_headcount: (bands, e.g. "2-10", "11-50")
- locations: (city and country, e.g. "Lyon, France")
- limit: 100 for a first run, then what the user asks for

## Mapping rules

- A city in the sentence sets `locations`; a country alone sets the country.
- A size word ("small", "independent") sets the headcount band; "any size" removes it.
- A role word sets `titles`; without one, use the default roles to reach.
- Apply negative keywords as filters where the source supports them, otherwise leave them to Grade.

## Other sources

- Accounts first: run the `hiring-signal-outbound` skill or `company.search` (query, location) and search people inside those companies with `companies: [...]`.
- Public registers: for regulated professions with a public register, the register is often a better and free source. Say which register and how to read it here, then use `contact.find` to add the email.
