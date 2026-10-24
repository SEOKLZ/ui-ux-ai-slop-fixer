#!/usr/bin/env python3
"""slop_scan.py — static detector for AI-slop UI tells.

Usage: python3 slop_scan.py <path> [<path>...] [--json] [--min-severity low|medium|high|critical]
Exit: 0 clean, 2 findings, 1 error. Stdlib only.
A first pass — layout/hierarchy/alignment still need a rendered look.
"""
import json, os, re, sys

EXTS = {".html", ".htm", ".css", ".scss", ".sass", ".less", ".js", ".jsx", ".ts", ".tsx",
        ".vue", ".svelte", ".astro", ".php", ".liquid", ".twig", ".erb", ".md", ".mdx"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".nuxt", "vendor", "coverage", ".impeccable", "out"}
SEV = {"low": 1, "medium": 2, "high": 5, "critical": 10}

I = re.IGNORECASE
RULES = [
    # id, pillar, severity, regex, message -> fix
    ("X9", "Too Much", "high", re.compile(r"from-(purple|violet|indigo|fuchsia)-\d+[^\"'`]*to-(blue|indigo|cyan|purple|violet|pink)-\d+", I),
     "AI purple/blue gradient → solid brand color"),
    ("X9", "Too Much", "high", re.compile(r"#(6366f1|8b5cf6|7c3aed|a855f7|9333ea|4f46e5|6d28d9|c084fc|818cf8)\b", I),
     "default AI indigo/violet hex → brand palette token"),
    ("X10", "Too Much", "medium", re.compile(r"(linear|radial|conic)-gradient\(|bg-gradient-to-", I),
     "gradient — keep only if brand-owned and used once"),
    ("H3", "Visual Hierarchy", "high", re.compile(r"bg-clip-text|background-clip:\s*text|-webkit-text-fill-color:\s*transparent", I),
     "gradient text → solid color, emphasize with size/weight"),
    ("T1", "Typography", "high", re.compile(r"\b(Inter|Geist|Plus Jakarta Sans|Poppins|Space Grotesk)\b(?![-\w])"),
     "overused default font → brand/characterful face (ignore if DESIGN.md says brand)"),
    ("T2", "Typography", "medium", re.compile(r"JetBrains Mono|Fira Code|>\s*//\s*\w|['\"`]//\s+[A-Za-z]", I),
     "mono / '//' tech decoration on UI text → remove"),
    ("T3", "Typography", "medium", re.compile(r"Instrument Serif|font-serif[^\"'`]*italic|italic[^\"'`]*font-serif", I),
     "italic serif display (2025 default) → choose type for this product"),
    ("T5", "Typography", "low", re.compile(r"tracking-tighter|letter-spacing:\s*-0?\.0[4-9]em", I),
     "crushed tracking → loosen, never on Persian"),
    ("T8", "Typography", "medium", re.compile(r"leading-(none|tight)\b|line-height:\s*1(\.0|\.1|\.2)?\s*;", I),
     "tight leading on text → 1.5+ for body"),
    ("T9", "Typography", "critical", re.compile(r"text-\[(9|10|11)px\]|font-size:\s*(9|10|11)px", I),
     "tiny text → ≥14px (body 16px)"),
    ("T11", "Typography", "low", re.compile(r">[^<{]*\w\.\.\.[^<]*<|['\"`](Loading|Saving)\.\.\.", I),
     "'...' → '…'"),
    ("SP1", "Spacing", "medium", re.compile(r"rounded-(2xl|3xl)\b", I),
     "extreme/uniform radius → size-based radius scale"),
    ("SP6", "Spacing", "low", re.compile(r"\b-?(p|px|py|pt|pb|pl|pr|m|mx|my|mt|mb|ml|mr|gap|space-[xy])-\[\d+(\.\d+)?px\]", I),
     "arbitrary spacing value → spacing scale token"),
    ("A6", "Alignment", "low", re.compile(r"\b(text-left|text-right)\b", I),
     "physical alignment → text-start/text-end (RTL-safe)"),
    ("X1", "Too Much", "high", re.compile(r"<(Card|div[^>]*class(Name)?=[\"'][^\"']*\bcard\b)[^>]*>\s*(?:(?!</).)*?<(Card|div[^>]*class(Name)?=[\"'][^\"']*\bcard\b)", I | re.S),
     "card nested in card → flatten with spacing/headings"),
    ("X3", "Too Much", "high", re.compile(r"(w|h|size)-(10|11|12|14|16)[^\"'`]*rounded-(lg|xl|2xl|full)[^\"'`]*(bg-|flex items-center justify-center)", I),
     "icon tile container → inline icon beside heading or none"),
    ("X4", "Too Much", "high", re.compile(r"border-l-(4|8)\b|border-(left|inline-start):\s*[3-9]px\s+solid", I),
     "side-tab accent border → remove unless it encodes status"),
    ("X5", "Too Much", "low", re.compile(r"\bborder\b[^\"'`]*shadow-(xl|2xl)|shadow-(xl|2xl)[^\"'`]*\bborder\b", I),
     "hairline border + wide shadow → choose one"),
    ("X6", "Too Much", "high", re.compile(r"animate-(pulse|ping)|animation:[^;]*\b(pulse|ping)\b", I),
     "pulsing badge/dot → static, label it, or remove"),
    ("X6", "Too Much", "medium", re.compile(r">\s*(Active|Verified|Live|Online|Active Student)\s*<"),
     "static status badge — does this state ever change?"),
    ("X7", "Too Much", "high", re.compile(r"backdrop-blur|backdrop-filter:\s*blur", I),
     "glassmorphism → solid surface + elevation"),
    ("X8", "Too Much", "high", re.compile(r"shadow-(purple|violet|indigo|cyan|fuchsia|pink|blue)-\d+|box-shadow:[^;]*rgba\((99|139|124|168|6|34),\s*(102|92|58|85|182|211)", I),
     "neon/colored glow → remove, use contrast"),
    ("X13", "Too Much", "medium", re.compile(r"blur-(2xl|3xl)|bg-grid|repeating-linear-gradient|aurora|\bblob\b|\borb\b", I),
     "decorative blur/grid/blob/aurora → remove or real imagery"),
    ("X14", "Too Much", "medium", re.compile(r"animate-bounce|cubic-bezier\([^)]*1\.[2-9]|elastic|spring.*bounce|hover:scale-1(05|10)|group-hover:scale|animate-marquee|marquee", I),
     "bounce/hover-zoom/marquee motion → ease-out 150–250ms or none"),
    ("X12", "Too Much", "high", re.compile("[\U0001F300-\U0001FAFF✨⚡✅❌⭐\U0001F680]"),
     "emoji in UI → consistent SVG icon set"),
    ("X17", "Too Much", "high", re.compile(r"\b(elevate|seamless(ly)?|supercharge|unleash|empower|revolutioni[sz]e|next[- ]gen(eration)?|cutting[- ]edge|world[- ]class|enterprise[- ]grade|streamline|effortless(ly)?|game[- ]chang|unlock the power|experience the power)\w*", I),
     "hype copy → concrete user outcome"),
    ("X18", "Too Much", "medium", re.compile(r"\bNot (just )?an? [\w ]{2,20}\.\s+An? [\w ]{2,20}\.", I),
     "forced-contrast slogan → state the fact"),
    ("X16", "Too Much", "medium", re.compile(r"Built with (Next|React|Hugo|Astro|Vite|Tailwind|AI|love)|Powered by AI|Written (in|from) (Neovim|Vim|VS ?Code)", I),
     "chat-context/stack leakage → delete"),
    ("X21", "Too Much", "low", re.compile(r"Welcome (back|to your dashboard)[^<\n]{0,30}[✨\U0001F44B\U0001F680!]", I),
     "welcome fluff → open on the task"),
    ("Q2", "Quality", "critical", re.compile(r"outline-none(?![^\"'`]*focus-visible)|outline:\s*(none|0)\s*;", I),
     "focus outline removed → add focus-visible ring"),
    ("Q4", "Quality", "high", re.compile(r"<(div|span)[^>]*\sonClick=", I),
     "clickable div/span → <button> or <a>"),
    ("Q3", "Quality", "critical", re.compile(r"<img(?![^>]*\balt=)[^>]*>", I),
     "img without alt"),
    ("Q7", "Quality", "low", re.compile(r"transition:\s*all|\btransition-all\b", I),
     "transition: all → list properties"),
    ("Q8", "Quality", "medium", re.compile(r"(bg|text|border|from|to|via)-\[#[0-9a-f]{3,8}\]", I),
     "hard-coded hex in class → semantic token"),
    ("Q9", "Quality", "medium", re.compile(r"from\s+['\"][^'\"]*/legacy/", I),
     "import from legacy/ → design-system package"),
    ("Q12", "Quality", "critical", re.compile(r"user-scalable\s*=\s*no|maximum-scale\s*=\s*1", I),
     "zoom disabled"),
]

def iter_files(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
            continue
        for root, dirs, files in os.walk(p):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in files:
                if os.path.splitext(f)[1].lower() in EXTS and not f.endswith(".min.js"):
                    yield os.path.join(root, f)

def scan_file(path):
    try:
        text = open(path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return []
    if "slop-scan-disable-file" in text:
        return []
    lines = text.split("\n")
    out, seen = [], set()
    for rid, pillar, sev, rx, msg in RULES:
        for m in rx.finditer(text):
            ln = text.count("\n", 0, m.start()) + 1
            if "slop-scan-disable" in lines[ln - 1]:
                continue
            key = (rid, ln)
            if key in seen:
                continue
            seen.add(key)
            out.append({"file": path, "line": ln, "rule": rid, "pillar": pillar,
                        "severity": sev, "match": m.group(0)[:60].replace("\n", " "), "message": msg})
    # page-level: heavy card usage / font-size count
    sizes = set(re.findall(r"\btext-(xs|sm|base|lg|xl|[2-9]xl)\b", text))
    if len(sizes) > 6:
        out.append({"file": path, "line": 1, "rule": "T4", "pillar": "Typography", "severity": "medium",
                    "match": ",".join(sorted(sizes)), "message": f"{len(sizes)} font sizes → 4–5 step scale"})
    return out

def main(argv):
    as_json = "--json" in argv
    min_sev = "low"
    if "--min-severity" in argv:
        min_sev = argv[argv.index("--min-severity") + 1].lower()
    paths = [a for i, a in enumerate(argv) if not a.startswith("--") and (i == 0 or argv[i - 1] != "--min-severity")]
    if not paths:
        print(__doc__, file=sys.stderr); return 1
    findings = []
    for f in iter_files(paths):
        findings += scan_file(f)
    findings = [f for f in findings if SEV[f["severity"]] >= SEV[min_sev]]
    counts = {k: sum(1 for f in findings if f["severity"] == k) for k in SEV}
    score = max(0, 100 - sum(SEV[f["severity"]] for f in findings))
    band = "intentional" if score >= 85 else "some reflexes" if score >= 65 else "clearly AI-made" if score >= 40 else "slop"
    if as_json:
        print(json.dumps({"score": score, "band": band, "counts": counts, "findings": findings}, ensure_ascii=False, indent=2))
    else:
        cur = None
        for f in sorted(findings, key=lambda x: (x["file"], x["line"])):
            if f["file"] != cur:
                cur = f["file"]; print(f"\n## {cur}")
            print(f"{f['file']}:{f['line']} [{f['severity']}] {f['rule']} {f['pillar']}: {f['message']}  «{f['match']}»")
        print(f"\nStatic slop score: {score}/100 ({band}) — critical {counts['critical']} · high {counts['high']} · medium {counts['medium']} · low {counts['low']}")
        print("Note: static pass only. Check hierarchy/spacing/alignment on a rendered page.")
    return 2 if findings else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
