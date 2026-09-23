---
name: social-lead-discovery
description: >-
  Find leads on X, Instagram, TikTok and YouTube with RouterGrowth and enrich
  them to a verified email. Search posts by keyword or hashtag (social.search)
  or mine the commenters under a competitor's post (social.comments), qualify
  from the post before paying for the profile, read the profile for the
  website, the bio links, the own domain and a public email (social.profile,
  or instagram.profile from a connected Instagram account for the business
  email and phone too), then resolve and verify a work email (contact.find,
  contact.verify), and send the Instagram DM from the user's own account
  behind a human gate (instagram.message). Use when the user wants leads from
  X (Twitter), Instagram, TikTok or YouTube, wants to reach founders, operators,
  creators, studios, shops or local businesses that post about a topic, says
  "find me people posting about X", "who is complaining about Y on Twitter",
  "who is commenting under Z", "scrape Instagram for leads", "DM the people
  who commented", or has an ICP that lives on social rather than LinkedIn
  (founders and GTM people on X; architects, interior designers, home
  builders, e-commerce brands, coaches, restaurants on Instagram).
---

# Social lead discovery

Some buyers never touch LinkedIn but post every week on X, Instagram, TikTok or YouTube: founders and GTM operators complaining about a tool on X; architects, interior designers, home builders, e-commerce brands, coaches, clinics, restaurants on Instagram. Their posts say what they sell or what hurts, and their bio says how to reach them. This skill turns a topic into a list of those accounts, reads each profile for the website, the bio links and the email, and hands back verified contacts plus a "social only" list for the ones that keep their inbox off the internet. Email goes out through the cold email skill. The Instagram DM goes out from the user's own connected account, one approved batch at a time, in step 6. There is no X DM capability: an X lead with an email goes to the cold email skill, and the rest get a reply the user posts by hand.

## Before you start

- Load the core `routergrowth` skill (https://www.routergrowth.com/SKILL.md) if it is not loaded. Confirm access with the free `balance` tool or `routergrowth balance`, without printing credentials.
- Ask for four things if the user did not give them: who the buyer is (one sentence), the topics or hashtags that buyer posts under, which of the four platforms to cover, and what "high intent" means for them (complaining about the tool you replace, posting about a project, asking for a quote under a competitor, using a hashtag that implies a purchase).
- Inspect the five capabilities once and show the prices before the first billable run: `routergrowth inspect -c social.search`, then `social.comments`, `social.profile`, `contact.find`, `contact.verify`. Quote the run as a whole, get a yes on the total.
- Run the free `instagram.accounts`. If the workspace has an Instagram account connected, step 3 reads profiles with `instagram.profile` (business email and phone included) and step 6 can send the DMs. If not, and the user wants DMs sent, `instagram.account` with a name returns the hosted sign-in link; the account holder opens it. The account is the user's own, aged and active. Never a bought one.
- Know the platform rules before you search. Instagram search is by hashtag only: no keyword, bio, location or follower search exists. X, TikTok and YouTube take free-text keywords. On X the phrase has to be the words a buyer types, not the category: "enrichment credits" found people burning credits, "clay credits" found tennis and pottery, "apollo credits" found a film. None of the four exposes a follower export, so "everyone who follows an account" is not a list you can build; commenters under that account's posts is, except on X, where `social.comments` is not available (search the thread's subject instead).

## Steps

### 1. Discovery: who is posting, who is asking

Two sources, use one or both. Keep the first limit at 50 per query until the user has seen a result.

**Topic search.** One run per platform and query. Instagram takes the hashtag with or without the `#`; X takes the phrase:

```bash
routergrowth run -c social.search -i '{"platform":"x","query":"enrichment credits","limit":30}' --max-cost 0.05 --wait 120 -o x.json
routergrowth run -c social.search -i '{"platform":"instagram","query":"interiordesignlyon","limit":50}' --max-cost 0.20 --wait 120 -o ig.json
routergrowth run -c social.search -i '{"platform":"tiktok","query":"kitchen renovation before after","limit":50}' --max-cost 0.20 --wait 120 -o tt.json
routergrowth run -c social.search -i '{"platform":"youtube","query":"house tour architect 2026","limit":50}' --max-cost 0.25 --wait 120 -o yt.json
```

Each post comes back with `author` (the display name), `author_handle`, `author_url` when the platform gives one, `url`, `text`, `created_at` and `engagement`. Priced per post, about $0.0006 on X, $0.00345 on Instagram, $0.0045 on YouTube and $0.0015 a search plus $0.0045 a post on TikTok at the time of writing, so 30 posts on X is 2 cents and 50 on Instagram is under 20 cents. The hold covers the requested limit and the charge covers the posts returned: 20 posts back on a limit of 30 bill 20. Three phrases per platform beats one broad one: the specific phrase is where the specific buyer posts. Expect noise on X, a third to a half of the rows: that is what step 2 is for, and it is free.

**Audience mining.** The comments under a competitor's post, a supplier's post or a niche creator's post are the people who already want the thing (Instagram, TikTok, YouTube; not X). Pick three to five posts from the search above (highest `replies`), then:

```bash
routergrowth run -c social.comments -i '{"url":"https://www.tiktok.com/@competitor/video/7301","limit":100}' --max-cost 0.10 --wait 120 -o comments.json
```

Priced per comment, about $0.00345 on Instagram, $0.00225 on YouTube and $0.0015 on TikTok, charged on the comments returned. Each comment carries `author`, `author_url` when the platform exposes it, `text` and `likes`. A comment that asks a price, a lead time, a location or "do you do this in Bordeaux" is intent written down; keep the text as the evidence column.

Dedupe on handle across every query and every platform before step 2. The distinct-author count is the number the rest of the run is quoted on.

### 2. Qualify from the post, before paying for the profile

Every step after this one costs more per row than the search did, so filter here, for free:

- Drop authors whose posts are in the wrong language or country for the offer.
- Drop the rows the keyword matched by accident (on X a phrase like "clay credits" also returns tennis, pottery and film credits) and the vendors, competitors and news accounts talking about the topic rather than living it.
- Drop negative keywords the user gave (students, inspiration accounts, "dm for credit" reposters, media pages).
- Keep the recency and engagement floor the user set. A post from 2023 is not a signal.
- On comments, keep the ones that ask or complain. "Stunning" is applause, not intent.

Show the user the count in and the count out, with five sample rows, before step 3.

### 3. The profile: bio link, own domain, public email

One call per surviving handle. Pass the handle, or the `author_url` for YouTube channels:

```bash
routergrowth run -c social.profile -i '{"platform":"x","handle":"miracold"}' --max-cost 0.01 --wait 120
routergrowth run -c social.profile -i '{"platform":"instagram","handle":"atelier.nord"}' --max-cost 0.02 --wait 120
```

About $0.002 on X, $0.0035 on Instagram, $0.006 on TikTok and $0.0045 on YouTube per profile. The `profile` object always carries `name`, `handle`, `followers`, `bio`, `verified`, and when the platform exposes them: `website` (the profile's website field, or the bio link), `links` (every link the profile lists; on X the t.co redirects in the bio are expanded to the page they point to, in the bio text too), `domain` (the registrable domain of the person's own site; link hubs such as Linktree, Beacons and Stan are never a domain, and neither is another social network; when the bio lists two unrelated sites, the X website field decides), `email` (a public or business email, or one written in the bio), `profile_url`, `is_business` (X professional accounts included), `category` and `location`. On X about half of the qualified profiles carry a website; the rest name their company in the bio and go through `company.search` for the domain.

When the workspace has an Instagram account connected, read Instagram handles with `instagram.profile` instead. Same fields, plus what only a signed-in lookup gives: the business `email`, `phone` and `address` block that business accounts publish, `follows_you`, and the `messaging_id` step 6 needs. About $0.002 per profile, and it counts as one of the account's roughly 100 daily actions, so keep it for the handles that survived step 2.

```bash
routergrowth run -c instagram.profile -i '{"handle":"atelier.nord"}' --max-cost 0.01
```

Score each profile before anything else is spent: bio words that match the buyer description, a follower band that fits (a 300k account is media, a 2k account with a studio website is a buyer), `is_business` true, `category` in range, a `domain` present. Then route each row:

- `email` present: go straight to step 5.
- `domain` present, no email: step 4.
- `links` holds a LinkedIn URL: that person is reachable through the `linkedin-outbound` skill; note the URL and move on.
- only a link hub, or nothing: keep the row in the social-only list with `profile_url` and, on Instagram, `messaging_id`. These are the rows step 6 is for. Do not try to scrape the link hub from this skill; `web.scrape` is not routable on production yet.

### 4. Work email from the domain

`contact.find` needs a first name, a last name and the domain. Split `name` when it is a person, and strip the decoration first: "Ivan Escobar | GTM Engineer" is Ivan Escobar. When `name` is a single word ("Parth", "Atishay"), there is no last name to pass: do not invent one, the lookup will happily return a pattern-guessed address for a person who does not exist. Ask the user, or find the person with `people.search` on the company. When the account is a studio or a shop ("Atelier Nord"), you need the owner's name first: ask the user if they know it, or look for it in the bio and pinned posts you already paid for. Only when the account is worth it, `people.search` with the company name and the titles `founder`, `owner`, `gérant` finds the person for about 15 cents base plus a few tenths of a cent per result; it is the one call in this skill that is not cheap per row, so quote it separately.

```bash
routergrowth run -c contact.find -i '{"first_name":"Claire","last_name":"Nord","company_domain":"atelier-nord.fr"}' --max-cost 0.10
```

Auto routing waterfalls across providers and charges only the one that delivers, about four cents on a hit, nothing on a miss. Small studios miss more often than SaaS companies; that is expected, and the miss costs nothing. Over MCP, send the rows as one `batch_run` with `max_cost` per item and `max_total_cost` for the batch. Before the lookups, run the free dedupe pass: `routergrowth history --file handles.txt` (one handle, email or profile URL per line) says who was already enriched or contacted and returns the reusable result.

### 5. Verify before anyone sends

```bash
routergrowth run -c contact.verify -i '{"email":"hello@atelier-nord.fr"}' --max-cost 0.02
```

About a cent each. Keep `valid`. Drop `invalid`. Hold `catch_all` and `unknown` in their own column and say so: a catch-all domain accepts everything, so the address is unproven, not clean. Verify the emails that came from a bio too; a bio email is often the oldest address the person owns.

### 6. The Instagram DM, one approved batch at a time

X rows: there is no DM capability, and this skill never posts. Draft the reply or DM (under 280 characters, names the post, asks one question, no pitch) and put it in the `dm_draft` column for the user to send from their own account by hand; the rows with a verified email go through the cold email skill instead.

Only with an Instagram account the user connected, and only after the human gate below. Two days after the email for the rows that have one; first touch for the social-only rows. The message names the project or post that surfaced them, asks one question, and does not pitch. Under 300 characters.

```bash
routergrowth run -c instagram.message -i '{"messaging_id":"17841412345","text":"Saw the Croix-Rousse flat on your feed, the kitchen light is unreal. Do you take on renovation projects outside Lyon?"}' --max-cost 0.01
```

Half a cent a message. A first message to someone who does not follow the account lands in their requests folder, so the reply rate is the number to watch, not the send count. Cap the batch at 20 a day for a warm account and 10 for a new one, spread over the day at random gaps; Instagram tolerates about 100 actions a day and 10 an hour across profile reads and DMs together. Read replies with `instagram.messages` (`unread: true`), and answer them by `chat_id` the same day: replying to inbound is safe at any volume. Anything that reads as a complaint or a "who is this" gets a human answer, not a template.

## Rules

- Inspect once per capability, quote the whole run, then run. Do not re-ask between rows once the user approved the total.
- `max_cost` on every run, `max_total_cost` on every batch. Stop and ask before a batch over about $1 unless the user asked for that volume.
- Public business and creator profiles only. Skip accounts that read as private individuals, and skip anything that looks like a minor's account. Keep the columns the user needs and nothing else; the evidence column is a post excerpt, not the person's whole feed.
- Never follow, like, reply or comment anywhere, on X least of all, and never send from an account the user did not connect. The only send in this skill is step 6, from the user's own Instagram account, after the gate, inside the daily cap. Email outreach is the `cold-email-pipeline` skill and LinkedIn is the `linkedin-outbound` skill.
- Never present sandbox (`rg_test_`) output as real data. Every row carries the run ID that produced it.

## Human gate

Before handing off to any outreach, and again before every DM batch: show the account count by platform, the contact count by verification status, the size of the social-only list, the total charged, five sample rows with their evidence, and for a DM batch the full text of every message. Wait.

## Budget for one run

Estimate from the rate card at the time of writing, not a recorded run: three platforms at 50 posts each, about $0.62; 60 distinct authors qualified down to 30 profiles, about $0.14; 12 of those with an email in the profile; 10 with a domain sent to `contact.find`, at most $0.38 with the misses free; 20 verifications, about $0.19. About $1.35 for roughly 20 verified contacts and a social-only list of the rest. Instagram business accounts carry an email far more often than TikTok or YouTube accounts do, so a run that is Instagram-heavy spends less on step 4.

What one real X run looked like (2026-09-14): three phrases at 30 posts, 80 posts back ($0.054); 72 distinct authors, 15 qualified for free; 15 profiles ($0.030), 8 with a website; 5 with a full name sent to `contact.find`, 3 found ($0.1125) and 2 released ($0); 3 verified, all valid ($0.028). $0.22 for three verified buyers, plus a social-only list of twelve.

## Output

A CSV with one row per account: `platform, handle, profile_url, name, followers, category, is_business, source, evidence, bio, website, domain, email, email_source, phone, verify_status, messaging_id, dm_draft, dm_status, run_id, charge`. `source` is the query or the post URL that surfaced the account; `evidence` is the post or comment text that qualified it; `email_source` is `profile`, `bio` or `contact.find`; `dm_status` is empty, `sent`, `replied` or `skipped`. Plus the totals: authors found, authors qualified, profiles read, emails found, emails valid, social-only accounts, total charged. Misses are listed at the bottom with the reason, so the user can see what was filtered and why.
