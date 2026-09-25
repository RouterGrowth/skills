# Lead source

How a targeting sentence becomes `people.search` (or `company.search`) filters.

## Default filters

- titles: (the titles that map to "roles to reach" in icp.md)
- seniority: (from `entry`, `senior`, `manager`, `director`, `vp`, `cxo`, `partner`, `owner`; other words are refused)
- industries: (the industry labels that match the firm type)
- company_headcount: (bands from `1-10`, `11-50`, `51-200`, `201-500`, `501-1000`, `1001-5000`, `5001-10000`, `10001+`)
- locations: (city and country, e.g. "Lyon, France")
- limit: 25 for a first run ($0.35 in full mode), then what the user asks for

## Mapping rules

- A city in the sentence sets `locations`; a country alone sets the country.
- A size word ("small", "independent") sets the headcount band; "any size" removes it.
- A role word sets `titles`; without one, use the default roles to reach.
- Apply negative keywords as filters where the source supports them, otherwise leave them to Grade.

## Other sources

- Accounts first: run the `hiring-signal-outbound` skill or `company.search` (query, location) and search people inside those companies with `companies: [...]` (up to six LinkedIn company URLs in one call). `company.search` is also where the web domain and the headcount come from; `people.search` rows have neither.
- Public registers: for regulated professions with a public register, the register is often a better and free source. Say which register and how to read it here, then use `contact.find` to add the email.
