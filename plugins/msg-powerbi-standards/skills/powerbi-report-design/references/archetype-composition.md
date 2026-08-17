# Archetype Composition & Variant Rotation

Use this file when a report has more than one page. Greenfield routing
(per-page archetype + variant) lives in `SKILL.md` Step 2; this file
covers the report-level composition patterns and the rule against
mono-archetype reports.

## Common multi-archetype compositions

| Report shape | Page 1 | Page 2 | Page 3+ | Notes |
|---|---|---|---|---|
| **Executive + Drill** | Executive Summary | Analytical Canvas | Comparative Benchmark for ranking pages | Most common; KPI landing → exploration → ranking |
| **Ops + Detail** | Operational Monitor | Analytical Canvas | Narrative Story for post-incident review | NOC board → incident drill → write-up |
| **Story + Evidence** | Narrative Story | Comparative Benchmark | Analytical Canvas for the appendix | Quarterly reviews, board presentations |
| **Multi-domain** ("cover everything" request) | Executive Summary as landing | Comparative Benchmark for entity rankings | Analytical Canvas for filterable exploration; Narrative for historical timeline | Default decomposition when one request spans multiple subject areas (entities + events + locations + actors) |

## Avoid mono-archetype reports

A 4-page report that is 4× Analytical Canvas (or 4× Executive Summary)
usually means each page wasn't routed independently — page 1's
archetype was copied to pages 2–4 by inertia.

When the same archetype is genuinely correct for multiple pages, those
pages must rotate **layout variants** (see *Cross-page variant
rotation* below). When even variant rotation can't differentiate the
pages, that's a signal the pages should be merged or split — not a
signal to ship 4 identical layouts.

## Cross-page variant rotation

When a report has 2+ pages of the **same archetype**, actively pick
**different variants** for each page where the data signals support
it. A 4-page Analytical report should not be 4× Filter-Rail; pick:

- **Filter-Rail** for the dense exploration page,
- **Inline-Slicers** for the focused-question page, and
- **Small-Multiples-Grid** for the cross-entity comparison page.

The selection tables in each archetype file are the mechanism — walk
them per page using *that page's* data shape, not the report's
overall shape. Only repeat a variant when two pages genuinely share
the same data signals AND serve distinct purposes.

| Same-archetype page count | Variant-rotation expectation |
|---|---|
| 1 page | Pick the variant the data calls for; no rotation needed |
| 2 pages | At least one page should differ from the other (≥1 of 2 variants) |
| 3 pages | Use at least 2 distinct variants; prefer all 3 if data supports it |
| 4+ pages | All available variants for that archetype should appear unless every page genuinely has identical data signals |

## Composition vs. tone

The composition pattern is independent of the design identity
(`tone` + `signature`) — an Executive + Drill report can be Editorial
Newsroom OR Industrial Cockpit OR Minimal Restrained. The tone
propagates uniformly across every page; the composition determines
which archetypes those pages occupy.

Pages within one report MUST share a tone and signature. A report
where page 1 is Editorial and page 2 is Industrial reads as two
reports stitched together. If the user requests genuinely different
tones for different audiences (e.g., "an exec page and an ops page"),
that's a signal to produce two reports, not one report with two
identities.

## Vertical logic across page titles

Read only the `page_title` text of every page, top to bottom in
navigation order — nothing else. Together they must compose into the
report's core story: the single decision or takeaway the report was
built to deliver (captured upstream as `core_story` in
`powerbi-report-planning`'s report spec when this skill runs inside
the planner workflow, or drafted directly from the prompt when this
skill runs standalone).

**Fails this check:**

- Titles that are each independently true but don't build an argument
  — "Revenue by Region", "Costs by Quarter", "Headcount Trend" reads as
  three unrelated facts, not a story.
- A thesis that silently flips or contradicts itself page to page
  without that tension being the intentional point of a page ("here's
  where the picture changes").

**Passes this check:**

- "Revenue missed plan by 8%, driven by EMEA" → "EMEA enterprise deals
  slipped past quarter-end" → "Three deals account for 70% of the
  shortfall" — each title narrows or supports the one before it, and
  the sequence reads as one argument, not three dashboards stapled
  together.

Apply this check while drafting titles during Step 2 (Archetype
Router), not as an afterthought once every page is already laid out —
reconciling titles after the fact tends to produce vague relabeling
rather than a real argument. If a report's pages genuinely can't be
made to compose into one story (truly independent subject areas with
no shared decision), that is itself a signal the request should be
split into separate reports rather than forced into one.
