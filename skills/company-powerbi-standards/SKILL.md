---
name: company-powerbi-standards
description: >-
  Apply msg corporate design standards to every Power BI report: brand colors,
  fonts, theme selection (executive vs operational), layout density rules, KPI
  color coding, and PBIP delivery requirements. Load this skill before any
  theme, color, layout, or brand decision is finalized for a Power BI report —
  it always takes priority over generic design defaults. Consumed by
  `powerbi-report-design` (Step 5 — Theme) and `powerbi-dashboard-architect`
  (Corporate Design gate). Triggers: "apply MSG standards", "corporate theme",
  "brand colors", "which theme to use", "MSG design guidelines".
metadata:
  version: 0.2.0
---

# msg Power BI Standards

## Purpose

Apply msg corporate design standards and dashboard best practices to every report.

## Consumed By

- `powerbi-report-design` — resolves the theme file here at Step 5 (Theme), before adapting `assets/base.json`.
- `powerbi-dashboard-architect` — loads this skill before any report generation as the top-priority design authority.

## Corporate Colors

Primary Color (MSG Red):
#A01441 — contrast vs white 7.86:1, passes WCAG AA for text and graphics.

Secondary Color, decorative use only (MSG Petrol Light):
#56A3BC — contrast vs white 2.85:1. **Fails WCAG AA for both text (needs ≥4.5:1) and large/graphic elements (needs ≥3:1).** Never use for text, data labels, axis labels, KPI indicators, or as a `good:`/`bad:` theme color. Restricted to large decorative fills/backgrounds where no contrast requirement applies (e.g. a subtle page-background tint).

Secondary Color, accessible (MSG Petrol Dark):
#3D7A8F — contrast vs white 4.8:1, passes WCAG AA for text. Use this shade — not Petrol Light — for any text, data label, chart series intended to carry a measure value, or `good:`/`bad:` theme indicator.

Neutral Color:
#6F6F6F — contrast vs white 5.02:1, passes WCAG AA for text.

Background:
#FFFFFF

Foreground/body text:
#202020 — contrast vs white 16.29:1.

**Do not substitute Petrol Light for Petrol Dark to "match the brand book."** The brand book's lighter petrol is a real color the company uses, but only in contexts (large fills, backgrounds) where WCAG's stricter thresholds don't apply. Every one of the two shipped theme files (`msg-theme-executive.json`, `msg-theme-operational.json`) already uses Petrol Dark for `good` and for any data series a user reads as text/labels — do not override this when adapting or authoring a theme.

## Fonts

Always use:

- Aptos
- Segoe UI (fallback)

Never use decorative fonts.

## Theme Selection

Theme files live in this skill's own folder: `skills/company-powerbi-standards/`.
Resolve the path relative to the consuming skill — for `powerbi-report-design`
and `powerbi-report-authoring` (both under `skills/<name>/`), that is
`../company-powerbi-standards/<file>.json`.

Use:

msg-theme-executive.json

for:

- Management Dashboards
- Executive Dashboards
- Steering Reports
- Board Reports

Use:

msg-theme-operational.json

for:

- Operational Reporting
- Service Dashboards
- Support Reports
- Detailed Monitoring Reports

## Layout Rules

Keep layouts simple and uncluttered.

Preferred structure:

Top Row:
- KPI Cards

Middle Row:
- Trend Analysis

Bottom Row:
- Detailed Breakdown

Maximum:
- 6 major visuals per page

**"Major visual" defined precisely** (do not guess): each `cardVisual`, chart (`barChart`, `columnChart`, `lineChart`, etc.), `tableEx`, `pivotTable`, or `azureMap` counts as 1. Slicers, textboxes, buttons, shapes, and navigation elements do not count toward the limit. A multi-value card showing 6 measures in one visual object is still 1 major visual, not 6. State the counted total explicitly in the design brief before handoff — do not leave it implicit.

Preferred:
- White background
- Large whitespace
- Clear hierarchy

Avoid:
- Dense layouts
- Decorative elements
- Visual overload

## Typography Sizing

Callout (KPI card headline value) sizing is brand-critical — undersized KPI numbers are the most common way an MSG report looks unpolished:

- Executive theme: 28pt callout (already set in `msg-theme-executive.json`)
- Operational theme: 22pt callout (already set in `msg-theme-operational.json`)

Do not shrink these when adapting a theme. If a custom override is required for a specific visual, it must not go below these values.

## Visual Type Rules

Use current visual types only: `cardVisual` (not `card`/`multiRowCard`), `azureMap` (not `map`/`filledMap`), `pivotTable` where a matrix is needed. See `powerbi-report-authoring`'s modern-visual-types guidance before authoring any visual — do not default to a deprecated type because it's familiar.

## Field Naming Rules

Every axis label, column header, legend entry, and card label must show a human-readable display name — never a raw database identifier (`customer_segment`, `Sum of fight_key`, `date_of_enrolment`). Set an explicit `displayName` on every bound field and every aggregation. This applies to pages, slicers, and table/column captions as well as measures — see `powerbi-dashboard-architect`'s Measure Naming section for the measure-specific `m_` prefix convention.

## Interaction and Tooltip Defaults

Every executive KPI card gets a drillthrough to its detail page unless the report has no detail page for that metric. Use `powerbi-report-authoring`'s `references/interactivity.md` for drillthrough/bookmark/tooltip mechanics; this skill only sets the MSG-specific default (KPI → drillthrough), not the implementation.

## KPI Rules

Important KPI:
MSG Red (#A01441)

Supporting KPI:
MSG Petrol Dark (#3D7A8F) — not Petrol Light. Both shipped theme files set `good: "#3D7A8F"` so positive/on-target indicators render at the same contrast strength as negative ones. Do not let `good` and `bad` end up at different contrast levels — an asymmetry there makes bad news look more visually prominent than good news by accident.

Neutral Information:
MSG Gray (#6F6F6F)

Use color sparingly.

Color must never be the only indicator.

### Palette Overflow Policy

`dataColors` ships exactly 6 entries per theme. Power BI auto-generates a 7th-and-beyond series color via hue/saturation shift the moment a chart has more categories than the palette — that color will not be on-brand. Before finalizing any chart:

- If the category count is ≤6, use `dataColors` directly.
- If >6, either (a) collapse extra categories into "Other" before charting, or (b) use a sequential single-hue ramp from Petrol Dark (dark) to Petrol Light (light) for ranked/ordinal categories, or (c) apply Gray (#6F6F6F) to every category past the top 6 by rank, reserving color for top performers only.
- Never let a 7th+ category silently take Power BI's auto-generated color. State explicitly in the design brief which overflow strategy was used, if any.

## PBIP Rules

Always create reports in PBIP format.

Always generate:

- report.json
- pages
- bookmarks
- theme reference

Use corporate theme automatically.

Every report must comply with MSG standards.