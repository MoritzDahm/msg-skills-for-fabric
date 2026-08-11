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
  version: 0.1.0
---

# msg Power BI Standards

## Purpose

Apply msg corporate design standards and dashboard best practices to every report.

## Consumed By

- `powerbi-report-design` — resolves the theme file here at Step 5 (Theme), before adapting `assets/base.json`.
- `powerbi-dashboard-architect` — loads this skill before any report generation as the top-priority design authority.

## Corporate Colors

Primary Color:
#A01441

Secondary Color:
#56A3BC

Neutral Color:
#6F6F6F

Background:
#FFFFFF

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

### Mixed-Audience Reports (Single-Theme-Per-Report Constraint)

PBIR/Power BI registers exactly one custom theme per report
(`report.json → themeCollection.customTheme`). There is no mechanism to
register a different theme file per page — every page in a report draws
`dataColors`, `textClasses`, and `good`/`neutral`/`bad` from the same
registered theme. Do not assume both `msg-theme-executive.json` and
`msg-theme-operational.json` can be applied to one report.

When a report mixes an executive/management landing page with
operational/analytical pages:

- Default to `msg-theme-executive.json` for the whole report. The landing
  page sets the report's first impression, and this is the common case for
  msg dashboards.
- Use `msg-theme-operational.json` for the whole report only when the
  report has no executive/management landing page at all — i.e. it is
  entirely operational/monitoring in nature.
- Optional, non-binding refinement: per-visual `objects` font-size overrides
  (title/callout sizes) can approximate a denser "operational" feel on
  specific pages without registering a second theme. This is a per-visual
  tweak, not a theme swap, and is not required for compliance.

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

Preferred:
- White background
- Large whitespace
- Clear hierarchy

Avoid:
- Dense layouts
- Decorative elements
- Visual overload

## KPI Rules

Important KPI:
MSG Red (#A01441)

Supporting KPI:
MSG Petrol (#56A3BC)

Neutral Information:
MSG Gray (#6F6F6F)

Use color sparingly.

Color must never be the only indicator.

## PBIP Rules

Always create reports in PBIP format.

Always generate:

- report.json
- pages
- theme reference

Generate bookmarks only when the report has a genuine bookmark-worthy state
(e.g. a default filtered view, a reset-to-default control, a guided
walkthrough of a narrative report). Do not add empty or placeholder
bookmarks solely to satisfy this rule when there is nothing meaningful to
capture — an unconditional "always generate bookmarks" produces stub
bookmarks with no purpose.

Use corporate theme automatically.

Every report must comply with MSG standards.