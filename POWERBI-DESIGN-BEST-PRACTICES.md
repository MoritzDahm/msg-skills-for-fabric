# Power BI Report Design — Best Practices Baseline

This is a design **style guide**, distilled from the rules the `powerbi-report-design`
skill applies when the agent designs a report (`plugins/powerbi-authoring/skills/powerbi-report-design/`).
Use it as the department's baseline when designing *any* new Power BI report —
whether it's built by the agent or by hand. It covers the *what* and *why* of
design decisions, not file mechanics (see `AGENT-WORKFLOW-SUMMARY.md` for the
end-to-end agent process).

Everything here is a default, not a law. Deviate deliberately, and write down
why — a design decision without a stated rationale is the thing this guide is
trying to prevent.

---

## 1. Start with data, not with visuals

Before choosing a single chart type or color, inspect the semantic model:
tables, columns, measures, relationships, cardinality, magnitudes, and
distributions. Every downstream decision (chart type, slicer grain, whether a
callout earns its space) should trace back to something actually observed in
the data — not a habit or a template default.

## 2. Commit to one design identity per report: tone + signature

Two decisions, made once, that must show up consistently on every page:

- **Tone** — the report's feel (e.g. *Editorial Newsroom*, *Industrial
  Cockpit*, *Corporate Cool*, *Minimal Restrained*, *Clinical Calm*). A tone
  is not a single adjective ("modern", "clean") — it must pin down
  typography pairing, palette/surface, density, gridline/border treatment,
  and iconography. See `references/tone-catalog.md` for the calibration set
  and domain defaults (e.g. finance → Corporate Cool/Editorial Newsroom,
  ops/NOC → Industrial Cockpit, healthcare → Clinical Calm).
- **Signature** — the *one* recurring visual move every page shares, and
  the thing a reader remembers after closing the report (e.g. tabular
  numerals throughout, highlight-and-grey bar treatment, status-coded KPI
  accent bars). It must be specific, recurring, and authorable in Power BI —
  not "good typography" in the abstract. See `references/signatures.md`.

**Failure mode to avoid**: declaring a tone in the brief but shipping the
same typography/palette/borders as every other report. The tone must be
traceable in concrete choices, page by page.

A single report must keep one tone/signature across all its pages. If two
genuinely different audiences need different identities (e.g. an exec page
and an ops wallboard), that's a signal to ship two reports, not one report
wearing two identities.

## 3. Route each page to an archetype — independently, not per report

A single request ("a report covering our business") usually decomposes into
several pages with different audiences and purposes. Route **every page**
against its own audience/purpose signal:

| Signal | Archetype | Typical charts | Interaction budget |
|---|---|---|---|
| C-suite/board, ≤10s scan, "is it on track?" | **Executive Summary** | Card, KPI, one hero line/bar, bullet | Minimal (0–1 clicks) |
| Shift/NOC/wallboard, "is it broken?" | **Operational Monitor** | Card + sparkline, table, RAG indicators | Moderate (3–5) |
| Analyst, hypothesis testing, "why did X happen?" | **Analytical Canvas** (default when unsure) | Scatter, histogram, box plot, small multiples, matrix | Rich (unlimited) |
| Author-driven argument, "here's what happened" | **Narrative Story** | Annotated line, waterfall, before/after bar | Guided (2–3) |
| Ranking/benchmarking/variance, "relative to what?" | **Comparative Benchmark** | Small multiples, grouped bar, slope chart | Moderate (3–5) |

Each archetype also ships 2–3 **layout variants** (A/B/C) selected by data
shape, not habit. For multi-page reports of the same archetype, rotate
variants — 4 pages of Filter-Rail-Analytical-Canvas back to back is a smell
that pages weren't routed independently (`references/archetype-composition.md`).

**Vague requests** (missing audience, purpose, page count, or filter depth):
stop and offer 2–3 concrete, named options before building anything. Don't
silently guess and ship a templatized result.

**Archetype zones are advisory, not a checklist.** Every card, callout, or
context tile must answer a distinct analytical question grounded in a
derived value (delta, variance %, rank shift, threshold, comparison
baseline). If the model can't support a zone, drop it rather than filling it
with a duplicate of an adjacent chart's number.

## 4. Chart selection: match the chart to the question, not the data type

Identify the analytical question first — comparison, composition,
distribution, relationship, trend, ranking, deviation, flow, or status —
then pick the chart that encodes it most directly.

**Encoding accuracy hierarchy** (most → least precise): position on a common
scale → position on non-aligned scale → length → direction/slope → angle →
area → volume → color/hue. When precision matters, prefer bars and dots.
Pies, bubbles, and 3D trade precision for shape — use sparingly, if at all.

| Purpose | Default | Cardinality limit | Avoid |
|---|---|---|---|
| Comparison | Sorted horizontal bar | ≤15–20 categories | Pie, donut, 3D |
| Composition | 100% stacked bar / treemap | ≤5 for donut, else sorted bar/treemap | Pie >5 slices |
| Distribution | Histogram, box plot | — | Single bar showing mean |
| Relationship | Scatter (bubble for 3rd var) | 3–5 color groups | Dual-axis line |
| Trend | Line chart (≥7 points); column for ≤6 periods | ≤5 lines | Smoothed line hiding volatility |
| Ranking | Sorted bar, descending | — | Unsorted bars |
| Deviation | Diverging bar, waterfall | — | Bar with arbitrary baseline |
| Single KPI | Compact card + sparkline | 1 value | Gauge, oversized bare card |
| Geospatial | `azureMap` | 200–500 points, else aggregate | Legacy maps, size-less bubble maps |

**Never**: 3D anything, dual y-axis to merge different units, gauges,
pie/donut past 5 slices, unsorted comparison bars, bars with a non-zero
baseline (except line/dot plots showing relative change).

Full decision matrix, PBI visual crosswalk, and edge cases:
`references/chart-selection.md`.

## 5. Layout: an 8px grid, a 12-column canvas, and earned whitespace

- **Canvas**: greenfield reports default to FHD (1920×1080); brownfield
  redesigns preserve the existing canvas unless a resize is agreed.
- **Grid**: everything (position, size, spacing) snaps to multiples of 8px.
  Misaligned edges read as careless.
- **12-column grid** inside page margins (32px FHD sides, 24px gutters)
  drives visual widths — full-width, 8+4, 6+6, 7+5, thirds, quarters. See
  `references/layout.md` for exact arithmetic.
- **Reading pattern**: F-pattern for dense/analytical pages with a filter
  rail; Z-pattern for sparse executive/narrative pages with a clear headline
  and hero visual.
- **Hierarchy**: top-left carries the heaviest message. Size + contrast +
  position determines what's read first — size should reflect analytical
  priority, not default habit. Never let a bare single-value card become the
  hero/largest region; reserve hero space for charts/tables/maps that
  explain change, ranking, distribution, or drivers.
- **Density**: 7±2 visual groups per page. Group by proximity (8–16px =
  related, ≥32px = separate); avoid boxes/borders to create grouping.
- **Whitespace budget**: analytical/operational/comparative pages ≤15%
  empty content cells; executive/narrative pages up to 20% when it supports
  the story. No region should exceed 45% of content cells unless it's the
  explicit, justified hero.
- **Header/slicer band**: reserve a title/slicer band on every page — title
  anchored left, slicers right. Charts/cards start below the band, never
  under it. Z-order is not a substitute for non-overlapping layout.
- **No overlap**: no two visual bounding boxes may overlap unless the
  overlap is deliberate and non-data-bearing (e.g. a background shape).
- **Slicer placement by count**: 1–3 slicers → inline with the title row
  (zero width cost to charts below); 4+ slicers → a vertical filter rail
  (only when it fills ≥50% of the rail's height — otherwise keep inline).
- **Slicer grain**: don't default to a full-date `Between` picker just
  because a date column exists. Executive/annual-grain pages get a
  Year dropdown/tile unless day/month exploration is genuinely needed.

## 6. Color: encode meaning, never decorate

- **Match palette family to data family**: sequential for ordered magnitude,
  diverging for ± from a midpoint, categorical for nominal groups. Never use
  a rainbow/categorical palette on ordered data — it implies no order and
  misleads.
- **Cap categorical palettes at 7–8 hues.** Beyond that, group the tail into
  "Other." Prefer CVD-safe palettes: Okabe-Ito, Set2, Cividis, Viridis (see
  `references/color.md` for hex ramps).
- **Color is never the sole channel** — always pair with label, icon, or
  shape (WCAG 1.4.1). Never rely on red/green alone (~8% of males have
  red-green CVD).
- **Reserve semantic colors**: green = good, red = bad, amber = warning,
  grey = neutral/context. Never flip these without an explicit, documented
  reason. Alert fatigue (>3 red conditional-format rules) makes every
  highlight meaningless.
- **Same measure → same color, everywhere it appears** (card, line, bar,
  map, table). A breakdown of that measure uses a light→dark gradient of the
  same hue. A different measure gets the next unused palette slot. This
  creates a visual link between a KPI card and its trend/breakdown charts.
- **Restraint beats vibrance** — most of the canvas should be neutral;
  color should draw the eye to what matters, not fill the page.
- **Every color in the report should trace to the theme** (`dataColors`,
  `good`/`neutral`/`bad`) — no hardcoded inline hex values.

## 7. Typography: 3–4 tiers, Segoe UI by default, weight before size

- **Type ramp**: page title (H1) → visual title (H2) → KPI value (H3) →
  body/axis/label → caption. Never exceed 4 distinct font sizes on one page;
  differentiate with weight before reaching for size.
- **Segoe UI is the safe default** — native to Power BI, renders
  consistently across Desktop/Service/mobile/embedded. Only deviate for a
  documented brand or tone requirement, and always specify a fallback chain.
  Never use serif/decorative fonts for axis labels, data labels, or matrix
  cells.
- **Numbers right-align; text left-aligns.** Use tabular-looking/consistent
  digit widths wherever a reader compares magnitudes (KPI rows, tables,
  aligned labels).
- **9pt is the normal floor** for visible text; 8pt only for non-critical
  captions/footnotes with strong contrast.
- **Number formatting**: thousands separators, unit abbreviations on
  cards/axes (`$1.2M` not `$1,200,000`), percentages as `12%`/`0.3%` (never
  raw decimals like `0.53`), consistent formatting across every page.
- Full type ramp, per-archetype calibration, and PBI formatting keys:
  `references/typography.md`.

## 8. Interactivity: overview first, insight on load, state always visible

- **The primary insight must be visible on page load** — never hidden
  behind a click, drill-through, or bookmark.
- **Every interaction must change something perceptible**; remove
  interactions that don't.
- **Match interaction budget to archetype**: Executive = 0–1 clicks;
  Narrative = guided 2–3 step bookmarks; Operational/Comparative = 3–5
  (slicers, cross-filter, drill-through); Analytical = unlimited (full
  drill-down, personalize, export).
- **Cross-filter defaults**: cards/KPIs → *Filter*; most charts → *Highlight*
  (preserves context); fixed reference/benchmark visuals → *None*.
- **Titles are answers, not chart types.** "APAC revenue grew 23% YoY," not
  "Revenue by Region."
- **Drill-through always gets a back button.** Bookmarks capped at 5–8 with
  descriptive names and a "reset to default" option. Multi-page reports (4+)
  need a page navigator or nav buttons.
- **Slicer state must always be visible** — never rely on an invisible
  filter to explain "missing" data.
- Full taxonomy and PBI feature grounding: `references/interactivity.md`.

## 9. Accessibility is a design requirement, not a QA afterthought

- **Contrast floors**: 4.5:1 for body text, 3:1 for large text and non-text
  elements (chart bars, lines, icons). Check every foreground/background
  pair; mid-range hues on white commonly fail body-text contrast.
- **Alt text describes the insight, not the chart type**: "Revenue rose 12%
  QoQ," not "This is a bar chart." Use DAX-driven alt text where the insight
  changes with filters.
- **Tab order matches the reading order**, not the order visuals were
  created in. Set it explicitly in the Selection pane.
- **Touch/click targets ≥24×24px.** Design must survive 200% zoom without
  clipping or overlap.
- **CVD-safe by construction**: simulate deuteranopia/protanopia/tritanopia
  before shipping; if two colors become indistinguishable, add a label,
  icon, or pattern.
- Per-archetype priority: Executive → alt-text quality (often consumed via
  email/read-aloud); Operational → keyboard + target size (kiosks, no
  mouse); Analytical → "show as table" fallback; Narrative → reading order;
  Comparative → CVD-safe color.
- Full WCAG 2.1/2.2 checklist and testing protocol: `references/accessibility.md`.

## 10. Anti-patterns — the recurring failure list

Check for these before calling any report finished
(`references/anti-patterns.md` has the full catalog with severity and fixes):

| Category | Watch for |
|---|---|
| **Chartjunk** | 3D effects, drop shadows, saturated background fills |
| **Misleading encoding** | Non-zero bar baselines, dual y-axis, pie >5 slices, gauges, radar charts, unshared small-multiple axes |
| **Cognitive overload** | >6 KPI cards, >12 visuals/page, >3 red conditional-format rules, >4 slicers visible, a detail matrix on an executive page |
| **Color misuse** | Rainbow on ordered data, >8 categorical hues, red/green as the only signal, low-contrast labels, pastel for "critical" status |
| **Interactivity theater** | Headline behind a click, invisible filter state, drill-through with no back button, >10 bookmarks, auto-cycling carousels |
| **Archetype mismatch** | 30-visual executive page, operational page missing a "last refreshed" timestamp, narrative page with no thesis statement, comparative pages with unsynchronized slicers |
| **Templatizing** | Every page defaulting to layout variant A, every page in a multi-page report sharing one archetype regardless of audience |
| **Raw field leakage** | Database field names (`method_category`, `Sum of fight_key`) left on axes/legends/headers instead of human-readable display names |

## 11. Pre-publish checklist

Run before delivering any report — human-authored or agent-authored:

1. **Layout** — ≤7 visual groups/page; everything on the 8px grid;
   consistent gutters; margins ≥24px; reserved header/slicer band respected.
2. **Color** — ≤8 categorical hues; no rainbow on ordered data; every
   text/background pair passes WCAG; no red/green-only signaling; CVD
   simulation passes; all colors from the theme.
3. **Typography** — ≤4 font sizes; numbers right-aligned/tabular; consistent
   number formatting; nothing below 8pt.
4. **Charts** — every chart answers a stated question; bars start at 0; no
   dual axes; no pie >5 slices; bar charts sorted by value.
5. **Interactivity** — primary insight visible on load; filter state
   visible; drill-through has a back button; ≤8 bookmarks.
6. **Accessibility** — alt text on every non-decorative visual; tab order
   matches reading order; keyboard navigation works end-to-end; touch
   targets ≥24×24px.
7. **Archetype fit** — visual density, interaction budget, typography tier,
   and palette all match the page's archetype.

---

## Where to go deeper

This document is a summary. For hands-on authoring, the
`powerbi-report-design` skill's reference files carry the full decision
tables, worked examples, and Power BI-specific mechanics:

| Topic | File |
|---|---|
| Tone calibration set | `skills/powerbi-report-design/references/tone-catalog.md` |
| Signature gallery | `skills/powerbi-report-design/references/signatures.md` |
| Archetype pages | `skills/powerbi-report-design/references/archetypes/*.md` |
| Multi-page composition | `skills/powerbi-report-design/references/archetype-composition.md` |
| Chart selection | `skills/powerbi-report-design/references/chart-selection.md` |
| Layout & grid | `skills/powerbi-report-design/references/layout.md` |
| Color strategy | `skills/powerbi-report-design/references/color.md` |
| Typography | `skills/powerbi-report-design/references/typography.md` |
| Interactivity | `skills/powerbi-report-design/references/interactivity.md` |
| Accessibility | `skills/powerbi-report-design/references/accessibility.md` |
| Anti-pattern catalog | `skills/powerbi-report-design/references/anti-patterns.md` |
| Design contract template | `skills/powerbi-report-design/references/design-brief.md` |
| Redesign/brand-swap rules | `skills/powerbi-report-design/references/brownfield.md` |

For the msg-specific overlay (corporate theme, measure-naming, approval
gates), see the `msg-powerbi-standards` plugin