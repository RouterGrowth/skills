---
name: ad-creative-batch
description: >-
  Produce a set of ad creatives from one brief with RouterGrowth, priced before
  anything is generated: image variants (creative.image), edits of the winner
  instead of regenerations (creative.image_edit), a product cutout reused across
  placements (creative.remove_background), upscales only for what ships
  (creative.upscale), and a short video from the winning still (creative.video).
  Use when the user wants ad creatives, image variants for a test, a batch of
  visuals for Meta or TikTok, a product shot on new backgrounds, or a short ad
  video.
---

# Ad creative batch

A brief in, a priced variant set out. The order matters for cost: generate small, pick, edit the winner, cut out once, upscale only what ships, animate one.

## Before you start

- Load the core `routergrowth` skill (https://www.routergrowth.com/SKILL.md) if it is not loaded. Confirm access with the free `balance` tool or `routergrowth balance`.
- Ask for the brief if it is missing: the product, the audience, the placement (feed 1:1, story 9:16, landscape 16:9), the message in one line, and any brand constraints (colours, no faces, no text in image). Ask for a product image URL if the user has one; a cutout from a real product beats a generated one.
- Inspect the five capabilities once and show the prices. Quote the whole set before generating: N variants, M edits, one cutout, K upscales, one video. Get a yes on the total. Video is priced per second of output, so it is the expensive line; say so. When no human is in the loop, pick the winner yourself, say why, and stop at the caller's budget.

## Steps

### 1. Variants, not a single image

Four to eight variants per concept, at the placement's aspect ratio, with the fastest model first:

```bash
routergrowth run -c creative.image -i '{"prompt":"<concept, subject, setting, lighting, no text>","aspect_ratio":"9:16","count":2}' --max-cost 0.05 --wait 90 -o variants-a.json
```

`count` gives samples of one prompt; to vary one thing per variant (setting, angle, colour) run one prompt per variant, same total cost. Generate at the aspect ratio the final placement needs: image-to-video keeps the still's ratio, so a vertical video starts from a 9:16 still. Results come back as `result.images[]` with a URL each. Show the user the grid with the run ID and the charge per image.

### 2. Edit the winner instead of regenerating

Once the user picks one or two, change what needs changing on that image rather than rolling again:

```bash
routergrowth run -c creative.image_edit -i '{"prompt":"swap the background for a kitchen at dawn, keep the product exactly as is","image_url":"https://..."}' --max-cost 0.10 --wait 90
```

### 3. Cut the product out once

```bash
routergrowth run -c creative.remove_background -i '{"image_url":"https://..."}' --max-cost 0.05 --wait 60
```

One cutout, reused on every placement and every background. Do it on the real product photo when there is one.

### 4. Upscale only what ships

Feed placements do not need it. Upscale the one or two finals that go to a large placement:

```bash
routergrowth inspect -c creative.upscale
routergrowth run -c creative.upscale -i '{"image_url":"https://..."}' --max-cost 0.25 --wait 120
```

### 5. One video from the winning still

```bash
routergrowth run -c creative.video -i '{"prompt":"slow push in, steam rising, soft morning light","image_url":"https://...","model":"hailuo-02","duration_seconds":6}' --max-cost 0.50
```

Video takes one to four minutes: submit (the receipt shows the quote), then poll with `routergrowth runs get -r <run_id> --wait 60 -o video.json` until `status` is terminal, usually two or three polls. Duration snaps to the model's options (hailuo-02 6 or 10 seconds, kling 5 or 10, veo3 4, 6 or 8) and bills the snapped length; `aspect_ratio` applies to text-to-video only. The result is `result.video`. One video per set unless the user asks for more; quote each one as rate x seconds.

Prices when this was written: image $0.00525 (flux-schnell, per image), edit $0.06825, cutout $0.0315, upscale $0.21 (2x) or $0.84 (4x), video $0.07875 a second on hailuo-02 ($0.4725 for its 6-second clip; other models cost more, inspect lists them). Charges can settle a few percent above the quote (a larger source image, a longer clip), so set `max_cost` above the quote, not equal to it. The upscale and the video are the surprise lines; quote them explicitly. Cutouts and upscales return `result.image`, not a list. If the CLI drops its connection while waiting on a slow run, the run keeps going on the router: `routergrowth runs` shows it and `runs get` fetches the result. Do not resubmit before checking.

## Rules

- Quote the set before step 1 and every video before it runs. `max_cost` on every run.
- Generated images are drafts for a test, not proof of anything. Never describe a generated image as a photograph of the product.
- No text baked into images unless the user asks; models get letters wrong. Overlay copy in the ad tool.
- No real people's likeness, no competitor logos, no trademarks the user does not own.
- Keep every result URL with its run ID; result URLs expire, so save the files the user wants to keep.

## Output

A folder with the variants, the edits, the cutout, the upscales and the video, named by step and variant, plus a manifest: file, capability, model, prompt, run ID, charge (the edit result does not echo the prompt, so the manifest is where it lives). And the total for the set, as the sum of every run's `billing.charged`, against the quote.
