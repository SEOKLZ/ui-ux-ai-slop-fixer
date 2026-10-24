# AI Slop Tells — Catalog

Legend: **S** = static-detectable (scanner), **R** = needs rendered page, **J** = judgment. Severity is default; downgrade if DESIGN.md documents it as intentional.

## 1. Visual Hierarchy
| # | Tell | How to spot | Det. | Sev |
|---|------|-------------|------|-----|
| H1 | Identical card grid | 3/6/9 same-size cards: icon + heading + 2 lines, all equal weight | R/J | High |
| H2 | Flat type hierarchy | H2 ≤ 1.25× body, or weight is the only difference | S/R | High |
| H3 | Gradient text | `bg-clip-text text-transparent bg-gradient-*`, `background-clip:text` on headings/numbers | S | High |
| H4 | Badge/eyebrow above H1 | small pill ("Introducing", "New ✨", "AI-powered") above every headline | S/R | Medium |
| H5 | Hero metric template | huge "10M+" + tiny label + 3 stats row, numbers unsourced | J | Medium |
| H6 | Competing CTAs | 2+ filled primary buttons in one view | R | High |
| H7 | Equal-volume color | 4–6 saturated hues with no dominant (violates 60-30-10 / 70-30-10) | R | High |
| H8 | Glow instead of contrast | radial halo/spotlight behind content to "highlight" it | S | Medium |
| H9 | Every screen is a landing page | functional dashboard/settings opens with a hero + tagline | J | High |
| H10 | Oversized hero headline | 8+ word headline at display size filling the fold | R | Medium |
| H11 | No progressive disclosure | every form, table, panel visible at once | J | Medium |

## 2. Spacing
| # | Tell | How to spot | Det. | Sev |
|---|------|-------------|------|-----|
| SP1 | Uniform padding/radius | `p-6 rounded-2xl` (24px/16px) on every component regardless of size | S | Medium |
| SP2 | Monotonous gaps | same `gap-*`/`space-y-*` between items and between groups | S/R | Medium |
| SP3 | Heading hugs previous section | margin above heading ≤ margin below | R | Medium |
| SP4 | Cramped controls | button/card padding < 8px vertical, text touching edges | R | Critical |
| SP5 | Body touching viewport edge | no horizontal gutter on mobile | R | Critical |
| SP6 | Arbitrary values | `p-[14px]`, `mt-[37px]`, `gap-[22px]` — no scale | S | Low |
| SP7 | Cards flush to scroller edge | horizontal scroller with no start/end padding | R | Low |
| SP8 | Extreme radius | ≥24px radius on small cards/inputs; everything a soft blob | S | Medium |

## 3. Typography
| # | Tell | How to spot | Det. | Sev |
|---|------|-------------|------|-----|
| T1 | Overused font | Inter, Geist, Poppins, Plus Jakarta, Space Grotesk, system-ui as the *only* identity | S | High |
| T2 | Mono-for-tech + `//` | JetBrains Mono/Fira Code headings, `// features`, `> _` cursor | S | Medium |
| T3 | Italic serif display | Instrument Serif / Playfair italic hero on non-editorial product (2025 tell) | S | Medium |
| T4 | Too many sizes | >5 distinct font sizes on one screen | S | Medium |
| T5 | Crushed tracking | `tracking-tighter` / letter-spacing < −0.03em at small sizes | S | Medium |
| T6 | Wide tracking on body | `tracking-wide/widest` on paragraphs | S | Low |
| T7 | Line length | > 75ch body width | R | Medium |
| T8 | Tight leading | body line-height < 1.4 | S | Medium |
| T9 | Tiny text | body < 14px, controls/nav < 12px | S | Critical |
| T10 | All-caps body | `uppercase` on multi-line text | S | Low |
| T11 | Typographic details | `...` vs `…`, straight quotes, no `tabular-nums` on numeric columns, no `text-wrap: balance` on headings (widows) | S | Low |
| T12 | RTL/Persian | Latin-first stack, letter-spacing on Persian, Latin digits in Persian copy, no ZWNJ (نیم‌فاصله), `text-align:left` hard-coded | S | High |

## 4. Alignment
| # | Tell | How to spot | Det. | Sev |
|---|------|-------------|------|-----|
| A1 | Icon/text misalignment | SVG not `items-center` with label; icon baseline off | R | Medium |
| A2 | Unboxed elements drift | lists, ASCII, timetables, SVG decorations off-grid | R | Medium |
| A3 | Center-everything | centered hero + centered cards + centered body paragraphs | R/J | Medium |
| A4 | Mixed alignment | left headings with centered body in same section | R | Medium |
| A5 | Unbalanced columns | two-column opening where one side runs far longer | R | Low |
| A6 | Physical not logical props | `ml-/mr-/left-/text-left` in an RTL-capable UI instead of `ms-/me-/start/end` | S | Medium |
| A7 | No shared grid | section widths/containers differ randomly (`max-w-5xl`, `max-w-6xl`, `max-w-7xl` mixed) | S | Low |

## 5. Too Much
| # | Tell | How to spot | Det. | Sev |
|---|------|-------------|------|-----|
| X1 | Cardocalypse | card inside card inside card | S/R | High |
| X2 | Cards for non-actionable content | static text wrapped in bordered/shadowed boxes | J | Medium |
| X3 | Fingernail cards / icon tile | small rounded-square icon container above every heading | S | High |
| X4 | Side-tab accent border | `border-l-4 border-<color>` on cards, rainbow per card | S | High |
| X5 | Hairline + wide shadow | `border` + `shadow-xl/2xl` on same element | S | Low |
| X6 | Pulsing badges / status dots | `animate-pulse`/`animate-ping` dots; "Active", "Verified", "Live", "Online" that never change | S | High |
| X7 | Glassmorphism | `backdrop-blur` + translucent bg as decoration; glass panels on glass | S | High |
| X8 | Neon/dark glow | colored `box-shadow` glows, `drop-shadow` neon, cyan-on-dark | S | High |
| X9 | AI palette | purple→blue/indigo gradients (`#6366f1 #8b5cf6 #7c3aed #a855f7 #3b82f6`, `from-purple-* to-blue-*`) | S | High |
| X10 | Gradients everywhere | gradient on buttons + bg + borders + text simultaneously | S | High |
| X11 | Rainbow vomit | many unrelated accent hues with no semantic map | R | High |
| X12 | Emoji slop | emoji as icons, bullets, nav items, section headers, in buttons | S | High |
| X13 | Decorative noise | grid-line bg, repeating stripes, floating blobs, orbs, aurora | S | Medium |
| X14 | Motion everywhere | fade-up on every section, bounce/elastic easing, hover image zoom, wiggling icons, marquee | S | Medium |
| X15 | Rough SVG/placeholder art | hand-coded mascot, circle-and-block "illustrations", unDraw-style filler | J | Medium |
| X16 | Chat-context leakage | "Built with Hugo", "Written from Neovim", "Powered by AI", "One campus. One app." — prompt words in UI | J | High |
| X17 | Hype copy | Elevate, Seamless, Supercharge, Unleash, Empower, Revolutionize, Next-generation, Cutting-edge, World-class, Enterprise-grade, Streamline, Effortless | S | High |
| X18 | Forced-contrast slogans | "Not X. Y.", "Less X. More Y." repeated; "theater" dismissals | S | Medium |
| X19 | Gray subtitle filler | every H1 followed by "Experience the power of…" gray paragraph | J | Medium |
| X20 | Redundant UX writing | label + placeholder + helper + tooltip saying the same thing; same word repeated in one card | J | Low |
| X21 | Welcome-fluff | "Welcome back, [Name] ✨", "Let's get started 🚀" | S | Low |
| X22 | Modal abuse | multi-column settings crammed into a scrolling modal | J | Medium |
| X23 | Em-dash overuse | — in most sentences of UI copy | S | Low |
| X24 | Layout template | hero → logos → 3 features → metrics → testimonials → CTA band → fat 4-col footer, regardless of content | J | Medium |

## 6. Quality / Accessibility (not slop-specific, always fix)
| # | Issue | Det. | Sev |
|---|-------|------|-----|
| Q1 | Low contrast (< 4.5:1 body, < 3:1 large); gray text on colored bg | S/R | Critical |
| Q2 | `outline-none` without `focus-visible` replacement | S | Critical |
| Q3 | Icon-only buttons without `aria-label`; images without `alt` | S | Critical |
| Q4 | `<div onClick>` instead of `<button>`/`<a>` | S | High |
| Q5 | Missing states: empty, loading, error, disabled, hover, focus | J | High |
| Q6 | No `prefers-reduced-motion` handling | S | Medium |
| Q7 | `transition: all` | S | Low |
| Q8 | Hard-coded colors (`#FF3B30`) breaking dark mode/rebrand | S | Medium |
| Q9 | Imports from `legacy/` or reinvented library components | S | Medium |
| Q10 | Text overflow, no `min-w-0`/truncate, horizontal scroll on mobile | R | High |
| Q11 | Skipped heading levels | S | Medium |
| Q12 | `user-scalable=no` / `maximum-scale=1` | S | Critical |
| Q13 | Content stuck at `opacity:0` waiting on JS reveal | R | Critical |

## Era drift (so you don't swap one slop for the next)
- **2022–24:** purple gradients, glassmorphism, neon glow, emoji, Inter.
- **2025:** cream/beige backgrounds, Instrument Serif italic heroes, eyebrow pills, bento grids, grainy gradients.
- **2026:** GPT-style neobrutalism (thick black borders, hard offset shadows, yellow/pink blocks), all looking identical.
A fix that lands on any of these by reflex is still slop.
