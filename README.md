# UI/UX AI Slop Fixer

An Agent Skill that **detects and fixes the "vibe-coded" look** in AI-generated interfaces. It catches purple gradients, Inter everywhere, cards nested in cards, icon tiles above every heading, pulsing "Active" badges, glassmorphism, emoji icons, "Supercharge your workflow" copy, and missing states.

It works with Claude Code, Claude.ai, Cursor, Codex, and any other agent that loads `SKILL.md` files. It also includes a dependency-free Python scanner that you can run in CI.

```
$ python3 slop_scan.py examples/
examples/slop-demo.html:4 [high] X9  Too Much: AI purple/blue gradient → solid brand color
examples/slop-demo.html:6 [high] H3  Visual Hierarchy: gradient text → solid color, emphasize with size/weight
examples/slop-demo.html:8 [high] X7  Too Much: glassmorphism → solid surface + elevation
...
Static slop score: 8/100 (slop) — critical 2 · high 13 · medium 3 · low 1
```

## Why another anti-slop skill?

Deleting a tell doesn't fix the design. If you remove the purple gradient and reach for the next safe default (a cream background, an italic serif hero, neobrutalism), you get next year's slop. This skill makes the agent **state a design direction first** and replace each reflex with a decision that fits *this* product.

What's different:

- **Five pillars:** Visual Hierarchy · Spacing · Typography · Alignment · Too Much, plus a Quality/a11y layer that is never optional.
- **About 70 tells**, each with a severity and a detection method (static, rendered, or judgment) → [`tells.md`](skills/ui-ux-ai-slop-fixer/references/tells.md)
- **A fix playbook** with concrete replacements, spacing/type/radius scales, and the interaction states to add → [`fix-playbook.md`](skills/ui-ux-ai-slop-fixer/references/fix-playbook.md)
- **Era drift:** the 2022, 2025 and 2026 defaults, so a fix doesn't land on the next one.
- **RTL/Persian support:** font stacks, zero letter-spacing on Persian, Persian digits, ZWNJ, and logical properties.
- **Make it stick:** `DESIGN.md` + `AGENTS.md` templates, 3-layer design tokens, and a linter → agent → CI loop.
- **Scoring:** 100 − (Critical×10 + High×5 + Medium×2 + Low×1).

## Install

**Claude Code / Codex / Cursor (skills CLI)**
```bash
npx skills add https://github.com/USERNAME/ui-ux-ai-slop-fixer
```

**Manual**
```bash
git clone https://github.com/USERNAME/ui-ux-ai-slop-fixer
cp -r ui-ux-ai-slop-fixer/skills/ui-ux-ai-slop-fixer ~/.claude/skills/
```

**Claude.ai:** zip the `skills/ui-ux-ai-slop-fixer` folder and upload it under Settings → Capabilities → Skills.

## Use

- *"Audit this page for AI slop"*: you get a scored report grouped by pillar, as `file:line — issue → fix`.
- *"De-slop the dashboard"*: the agent audits, makes surgical edits, then re-verifies.
- When the agent builds a new UI, the skill runs as a pre-flight checklist.

The scanner also works on its own:
```bash
python3 skills/ui-ux-ai-slop-fixer/scripts/slop_scan.py src/ [--json] [--min-severity high]
```
Exit code `2` means findings were reported, so you can use it to gate a CI step. See [`.github/workflows/slop-scan.yml`](.github/workflows/slop-scan.yml). To silence one line, add `slop-scan-disable`; to skip a whole file, add `slop-scan-disable-file`.

> The static scan is only a first pass. Hierarchy, spacing and alignment problems mostly need a rendered page. If Playwright MCP or a browser tool is available, the skill takes screenshots at 375px and 1440px.

## Not a ban list

If your `DESIGN.md` says Inter is the brand font, Inter is not a finding. Slop rules are judgment calls. Quality rules (contrast, focus states, alt text, overflow) apply to everyone, every time.

## Credits

This skill distills and builds on:
[10 tells of a slop UI](https://godobject.dev/blog/10-tells-of-slop/) (Pranav Desai) ·
[7 Signs a UI Has Been Vibe Coded](https://www.thefountaininstitute.com/blog/signs-vibe-coded-ui) (Fountain Institute) ·
[Impeccable](https://github.com/pbakaus/impeccable) ·
[Taste-Skill](https://github.com/leonxlnx/taste-skill) ·
[Vercel Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines) ·
[awesome-design-md](https://github.com/voltagent/awesome-design-md) ·
[Playwright MCP](https://github.com/microsoft/playwright-mcp)
Hacker News, Reddit and Product Hunt discussions of vibe-coded UI also shaped it.
If you want a full design workflow with live browser iteration, use Impeccable alongside this skill.

## Contributing

Spotted a new tell? Open an issue with a screenshot, how to detect it, and the fix. PRs that add scanner rules should include a test case in `examples/`.

## License

MIT © Ali — [Rokamino](https://rokamino.com)

---

<div dir="rtl">

### فارسی

اسکیلی برای شناسایی و اصلاح ظاهر «اسلاپ هوش مصنوعی» در رابط کاربری. پنج محور را بررسی می‌کند: سلسله‌مراتب بصری، فاصله‌گذاری، تایپوگرافی، ترازبندی و «زیادی» (المان‌های اضافه). به صفحه امتیاز می‌دهد و بعد اصلاح‌ها را بر اساس هویت همان محصول انجام می‌دهد. از رابط‌های فارسی و راست‌به‌چپ هم پشتیبانی می‌کند.

</div>
