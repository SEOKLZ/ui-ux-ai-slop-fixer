---
name: ui-ux-ai-slop-fixer
description: Detects and fixes "AI slop" in UI/UX — the generic, vibe-coded look (purple gradients, Inter everywhere, card-in-card, icon tiles, pulsing badges, glassmorphism, emoji icons, hype copy, missing states). Audits code or a live URL across Visual Hierarchy, Spacing, Typography, Alignment and "Too Much", scores it, then rewrites with deliberate, brand-specific choices. Use whenever building, reviewing, redesigning or de-slopping any website, landing page, dashboard, app screen or component — including Persian/RTL UIs — or when the user says "looks AI-made", "vibe-coded", "generic", "de-slop", "اسلاپ", "شبیه هوش مصنوعی", "بی‌هویت", or asks for a UI audit.
---

# UI/UX AI Slop Fixer

AI-generated UIs are not recognizable by one property but by **convergence**: every model, asked for "modern clean UI", reaches for the same statistical defaults. Each tell is harmless alone; fifty of them together produce the "this is slop" feeling.

Two rules govern everything:

1. **Deleting a tell is not a fix.** Removing the purple gradient and reaching for the next safe default (cream background, italic serif hero, neobrutalism) is next year's slop. Every fix must replace a reflex with a decision derived from *this* product: domain, audience, brand, content.
2. **Slop rules are judgment; quality rules are not.** An italic serif is fine on an editorial magazine and a tell on a B2B SaaS. Low contrast, missing focus states and overflowing text are broken for everyone, always.

Smell test: *if you could swap this UI onto a different product and nothing would feel wrong, no decisions were made.*

## Modes

- **Audit** — "is this slop?", "review my UI", URL or files given → produce the report, don't edit.
- **Fix** — "de-slop this", "fix it" → audit, then edit surgically, then re-verify.
- **Build guard** — generating new UI → apply `references/tells.md` as a pre-flight checklist before showing output.

## Workflow

### 1. Establish the design direction (always first)
Before touching anything, write 2–3 sentences: what the product is, who uses it, the context of use (task tool vs. marketing page), and the intended character. Check for `DESIGN.md`, `AGENTS.md`, `PRODUCT.md`, tokens (`tokens.json`, `tailwind.config`, `:root` variables) and brand fonts — if present, they are the source of truth and a "tell" that the brand chose deliberately (e.g. Inter as the real brand font) is **not** a finding. If none exist and the user is present, ask at most one question about brand/audience; otherwise infer and state the assumption.

### 2. Detect
Run both layers when possible:

- **Static scan** (code): `python3 scripts/slop_scan.py <path> [--json]` — catches mechanical tells in HTML/CSS/JSX/TSX/Vue/Svelte/Tailwind (gradients, AI palette hexes, Inter/Geist, side-tab borders, nested cards, pulse/bounce animations, emoji in markup, hype words, `transition: all`, `outline-none`, missing alt/aria-label, hard-coded hex/arbitrary values). Exit code 2 = findings. It's a first pass, not a verdict.
- **Rendered check** (URL / dev server): if a browser tool is available (Playwright MCP `browser_navigate` + `browser_take_screenshot` + `browser_snapshot`, Claude in Chrome, or the built-in browser), screenshot at 375px and 1440px and inspect visually. Layout, hierarchy, alignment and "too much" tells mostly need eyes. Optionally `npx impeccable detect <url>` if the user has Impeccable.
- **Judgment pass**: walk the five pillars below against `references/tells.md`.

### 3. Score & report
Use the format in "Report format". Severity: **Critical** (broken/inaccessible), **High** (strong slop signal, hurts conversion/trust), **Medium**, **Low**. Score = 100 − (Critical×10 + High×5 + Medium×2 + Low×1), floor 0. Bands: 85+ intentional · 65–84 some reflexes · 40–64 clearly AI-made · <40 slop.

### 4. Fix (Fix mode)
Follow `references/fix-playbook.md`. Order: quality/critical → hierarchy → spacing → typography → alignment → too much → copy. Edits are **surgical** — change the offending classes/rules, keep structure and logic; never rewrite a whole file to fix a tell. Fix the system, not the instance: if a color/radius/spacing value recurs, introduce or reuse a token instead of patching each occurrence.

### 5. Verify
Re-run the scanner and re-screenshot. A clean scan is evidence, not proof. Confirm no new default was introduced (the "next safe default" trap) and that states (empty/loading/error/disabled/focus) exist for anything interactive touched.

## The five pillars (what to look at)

**1. Visual Hierarchy** — Is there exactly one thing the eye hits first and one primary action per screen? Flags: everything same weight (identical card grids, equal-volume colors), heading barely larger than body, gradient text used for emphasis, badge/eyebrow pill above every H1, hero metric template, multiple competing CTAs, glow/halo doing the job contrast should do.

**2. Spacing** — Does space encode relationships (related = close, separate = far)? Flags: uniform 24px padding + 16px radius on everything, monotonous gaps, heading closer to previous section than its own content, cramped buttons, cards flush to scroller edge, no spacing scale (arbitrary `p-[14px]`).

**3. Typography** — Does the type have a point of view and a scale? Flags: Inter/Geist/system default with no brand reason, JetBrains Mono + `//` prefixes on anything "techy", flat scale (>4–5 sizes or <2 steps between levels), crushed tracking on display, wide tracking on body, all-caps paragraphs, line length >75ch, line-height <1.4 on body, `...` instead of `…`, no `tabular-nums` on numbers. RTL/Persian: Latin-first font stack, missing Vazirmatn/IRANSans-class font, wrong letter-spacing on Persian (any non-zero tracking breaks joins), mixed digits.

**4. Alignment** — Does everything sit on a shared edge/grid? Flags: icons/SVGs not vertically centered with text, list bullets and ASCII off-baseline, centered everything (centered hero + centered cards + centered CTA), ragged columns, unbalanced two-column openings, mixed left/center alignment in one section, RTL layouts using `left/right` instead of logical `start/end`.

**5. Too Much** — Does every element earn its pixels? Flags: card-in-card (Cardocalypse), cards for content that isn't independently actionable, pulsing "Active/Verified/Live" badges that never change, status dots with no legend, glassmorphism/backdrop-blur/neon glow as decoration, rainbow side-tab borders, emoji as icons/bullets/nav, oversized icon tiles above every heading, decorative grid/stripes/blobs, auto-marquee logos, bounce/elastic easing, fade-up-on-everything, image zoom on hover, redundant text explaining the same field 3×, chat-context leakage ("Built with Next.js", "One campus. One app."), hype copy (Elevate, Seamless, Supercharge, Unleash, Empower, Next-generation, World-class), forced contrast slogans ("Not a feature. A platform."), "Welcome back, Name ✨".

## Report format

```
# UI Slop Report — <target>
Design direction (assumed/stated): <2–3 sentences>
Score: 58/100 — clearly AI-made   (Critical 1 · High 6 · Medium 5 · Low 3)

## Top 3 things to fix first
1. …

## Findings by pillar
### Visual Hierarchy
- [High] src/Hero.tsx:14 — gradient text on H1 + pill badge above it → solid brand color, drop the pill, put the claim in the headline
### Spacing …
### Typography …
### Alignment …
### Too Much …
### Quality / Accessibility …

## Keep (deliberate choices, not slop)
- Inter is the documented brand font in DESIGN.md
```

Be terse: `file:line — issue → fix`. For URL audits, reference the section/element instead of file:line. Write the report in the user's language (Persian if they wrote in Persian), keeping technical identifiers in English.

## References
- `references/tells.md` — full catalog (~70 tells) by pillar, with detection hints and severity.
- `references/fix-playbook.md` — replacement decisions per tell, token/DESIGN.md/AGENTS.md hardening so the slop doesn't come back, RTL notes.
- `scripts/slop_scan.py` — static scanner (stdlib only, CI-friendly).

Sources this skill distills: godobject.dev "10 tells of a slop UI", Fountain Institute "7 signs a UI has been vibe coded", Impeccable anti-pattern catalog (impeccable.style/slop), Taste-Skill (dials: DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY), Vercel Web Interface Guidelines, awesome-design-md (DESIGN.md format), Playwright MCP, plus Hacker News/Reddit/Product Hunt discussions on vibe-coded UI.
