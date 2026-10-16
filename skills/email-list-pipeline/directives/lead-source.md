# Lead source

Where the list comes from, and how a targeting sentence becomes `people_search` (or `company_search`) filters.

## The user's own sources first

- (CRM export, event attendee list, inbound form leads, customer list, webinar sign-ups: name the file and its columns)

These already carry the reason to write. The pipeline grades and verifies them like any other row.

## Default filters for `people_search`

- titles: (the titles that map to "roles to reach" in the ICP file)
- seniority: (from `entry`, `senior`, `manager`, `director`, `vp`, `cxo`, `partner`, `owner`; other words are refused)
- industries: (the industry labels that match the firm type)
- company_headcount: (bands from `1-10`, `11-50`, `51-200`, `201-500`, `501-1000`, `1001-5000`, `5001-10000`, `10001+`)
- locations: (city and country, e.g. "Lyon, France")
- limit: 25 for a first search, then what the user asks for. Priced per person returned: check `get_operation_pricing` before the first call.

## Mapping rules

- A city in the sentence sets `locations`; a country alone sets the country.
- A size word ("small", "independent") sets the headcount band; "any size" removes it.
- A role word sets `titles`; without one, use the default roles to reach.
- Apply negative keywords as filters where the tool supports them, otherwise leave them to Grade.

## Other sources

- Accounts first: run the `hiring-signal-leads` skill or `company_search` (query, location) and search people inside those companies with `companies` or `company_domains`. `company_search` is also where the web domain and the headcount come from.
- Public registers: for regulated professions with a public register, the register is often a better and free source. Say which register and how to read it here, then use `contact_find` to add the email.
