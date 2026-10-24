# Fix Playbook

Every fix = **remove the reflex + make a product-specific decision**. Write the decision down (one line) in the report.

## Before fixing: lock the direction
1. Product, audience, context of use, desired character (from DESIGN.md / PRODUCT.md / brand, else inferred).
2. Pick dials (Taste-Skill style, 1–10): `DESIGN_VARIANCE` (layout experimentation), `MOTION_INTENSITY`, `VISUAL_DENSITY`. Dashboards: variance 3, motion 2, density 7. Marketing: variance 6, motion 4, density 3. Admin/forms: 2/1/6.
3. Palette budget: 1 dominant brand hue, 1 accent, neutrals tinted toward the brand (never pure #000/#888), semantic success/warning/danger. Apply ~60-30-10.

## Visual Hierarchy
- **One focal point per view.** Decide the primary task; make it the largest/highest-contrast element. Demote everything else via size, weight, color — not glow.
- **Identical card grid →** group by importance: lead item large, rest as a compact list; or a two-column text layout with icons inline.
- **Gradient text →** solid brand color or plain heading color; emphasize with size/weight.
- **Eyebrow pill →** delete, or move real info (version/date) into the subtitle.
- **Competing CTAs →** one filled primary, others secondary (outline/ghost) or text links.
- **Dashboard opening with a hero →** remove tagline; open on the data/primary action. Greeting at most a small line, no emoji.
- **Progressive disclosure →** tabs/accordions/"Advanced" sections; show only what the current step needs.

## Spacing
- Adopt a 4/8 scale (4, 8, 12, 16, 24, 32, 48, 64, 96). Map arbitrary values to the nearest step.
- **Proximity rule:** gap inside a group < gap between groups (≈ 1:2 to 1:3). Space above a heading ≥ 1.5–2× space below it.
- Vary padding by component size: chip 4–8, button 8–12 × 16–20, card 16–24, section 64–128.
- Radius scale by size: inputs/buttons 6–10, cards 8–12, modals 12–16. Pick sharp (0–4) if brand is technical/editorial. One scale, documented.
- Mobile gutter ≥ 16px; scrollers get matching start/end padding.

## Typography
- **Replace Inter/Geist only if no brand reason.** Choose by character: humanist sans for friendly, grotesk for neutral-precise, serif for editorial/trust, slab for industrial. Pair ≤ 2 families. Keep brand fonts.
- Persian/RTL: Vazirmatn, Estedad, Shabnam, IRANSans/IRANYekan (licensed), Peyda. Put the Persian face first in the stack; `letter-spacing: 0` on Persian; use Persian digits in Persian copy (`font-feature-settings: "ss01"` or font variant); keep ZWNJ; `dir="rtl"` and logical properties.
- Scale: 4–5 sizes, ratio ~1.2–1.333 (e.g. 14/16/20/28/40). Body 16px min, line-height 1.5–1.7 (Persian 1.8–2), measure 60–75ch.
- Display: slight negative tracking only ≥ 32px; never on Persian.
- Remove `//` prefixes and mono headings unless the product *is* a code tool, and even then use mono for code, not section titles.
- `…`, curly quotes, `tabular-nums` on numbers, `text-wrap: balance` on headings.

## Alignment
- Icons with text: `inline-flex items-center gap-2`; size icons to cap-height (16–20px) with consistent stroke.
- Pick one alignment axis per section (left/start for content-heavy, center only for short hero statements).
- One container width system (e.g. content 68ch, page max 1200px) used everywhere.
- RTL: `ms-/me-/ps-/pe-/start-/end-`, `text-start`, mirrored directional icons only (arrows, not logos/play buttons).

## Too Much (subtract first)
- **Ask of each decoration: does it communicate state, structure or action?** If not, delete.
- Card-in-card → flatten: outer becomes section with spacing + heading; inner keep card only if independently actionable.
- Non-actionable cards → plain blocks separated by spacing or a 1px divider.
- Icon tile above heading → icon inline beside heading or no icon.
- Side-tab borders → remove; keep only where it maps to status/priority/selection, using semantic colors.
- Pulsing badges/dots → remove if state never changes; otherwise static dot + text label, motion only on real transitions.
- Glassmorphism/neon → solid surfaces with defined elevation levels (bg, surface, raised); dark mode depth via lighter surfaces, not glow.
- Purple→blue gradients → solid brand color; gradient only if the brand truly owns one, used once.
- Emoji → consistent SVG icon set (Lucide, Phosphor, Tabler, Heroicons) at one stroke/size; emoji only in human messaging.
- Motion → transform/opacity, 150–250ms, ease-out, no bounce; respect `prefers-reduced-motion`; animate only on interaction or meaningful state change.
- Decorative bg (grids, blobs, stripes, aurora) → remove or replace with real imagery/screenshots of the product.

## Copy
- Replace hype words with what the user can do + the concrete outcome ("Send invoices in Rial and Toman" not "Supercharge your billing").
- Delete chat-context leakage and "Built with X" lines unless the audience is developers choosing a stack.
- Kill gray filler subtitles; if kept, make them carry a fact (number, constraint, audience).
- Specific button labels ("Save address", "ثبت سفارش") not "Continue"/"Get started" everywhere.
- Error messages state the fix. Empty states explain what goes here + primary action.
- Persian: natural register, no translated-English slogans, proper نیم‌فاصله.

## States (Q5) — add for every interactive component touched
default · hover · focus-visible · active · disabled · loading (`aria-busy`, "در حال ذخیره…") · empty · error (inline, focus first error) · success.

## Make it stick (system hardening)
If the user owns the repo and wants slop to stop recurring, offer:
1. **DESIGN.md** (look & feel — Google Stitch / awesome-design-md format): direction, palette with roles, type scale, spacing & radius scale, elevation, motion, voice, do/don't.
2. **AGENTS.md** (how to build): never hard-code hex/px; use semantic tokens (`--ds-*`); no Tailwind arbitrary values; no imports from `legacy/`; import library components instead of rebuilding; always ship loading/empty/error/disabled + focus + ARIA; run the scanner/linter before finishing.
3. **Tokens, 3 layers (DTCG JSON → Style Dictionary → `tokens.css`):** primitives (`blue-600`) → semantics (`background.interactive.primary`) → component (`button.primary.bg`).
4. **Enforcement loop:** lint (ESLint `no-restricted-imports`, Biome/GritQL rules for arbitrary values and raw colors, `slop_scan.py`) → feed diagnostics back to the agent → repeat to zero → gate in CI.
5. **Golden examples:** `docs/components/*.md` or `src/design-system/examples/` with props, allowed states, do/don't.

Rollout for teams: Phase 1 audit + tokens + font (wk 1–3) · Phase 2 DESIGN.md/AGENTS.md + linters (wk 4–6) · Phase 3 CI gate + closed loop (wk 7+). KPIs: token coverage >70%, zero arbitrary-value merges.
