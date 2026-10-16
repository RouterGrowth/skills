# Email copy

The pipeline writes drafts from this file. The user sends them from their own mail tool.

## Sender

- From: (the address the user sends from, a real person at the company)
- Reply-to: (an address a human reads)
- Signature: name, role, company, website. One phone number if the user wants calls.
- Opt-out line: one sentence at the end telling the reader how to stop receiving these. Mandatory, and every opt-out is honored.

## Voice and rules

- Language: the recipient's.
- Plain text. No HTML, no images, no tracking.
- Make the reason to write plain in the first two lines (the event, the sign-up, the introduction, the role).
- Lead with the pain from research-brief.md, then the relief. The product comes second.
- Product facts match the live site. Never invent a plan name, a feature, a price or a trial term.
- First line written from this person: their role, their firm, one thing from their site.
- One call to action.
- 120 to 160 words.
- Merge fields `{first_name}` and `{company}` only, and only clean ones.

## Product facts (keep current)

- (plan names and prices as the site states them)
- (the proof point: customers, a number, a result, with its source)
- (the trial or proof of concept exactly as offered)

## Tier angles

- Founder or agency lead: oversight, visibility, control.
- Operator: time saved, fewer chases, a cleaner week.
- Generic mailbox: "please forward to the person who owns (function)".

## Templates

### First email

```
Subject: {first_name}, (the pain as a question)

Hi {first_name},

(the reason you are writing, and one line from their site or role)

(the pain as a question, from the research brief)

(what the product does about it, three short lines at most)

(the proof point)

(the offer, exactly as the site states it)

(one question as the call to action)

(signature)
(opt-out line)
```

### Optional follow-up (the user sends it only if there is no reply)

```
Subject: Re: (original subject)

Hi {first_name},

Short follow-up in case the first note got buried.

(the product in two lines)

(one question)

(signature)
(opt-out line)
```

One follow-up at most. No reply after that means no.
