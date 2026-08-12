---
name: company-powerbi-standards
description: >-
  Apply msg's corporate design standards to every Power BI report: brand
  colors, fonts, theme selection (executive vs operational), layout density
  rules, KPI color coding, and delivery format requirements. Load this skill
  before any theme, color, layout, or brand decision is finalized for a Power
  BI report — it always takes priority over generic design defaults. Consumed
  by `powerbi-report-design` (Step 5 — Theme) and `powerbi-dashboard-architect`
  (Corporate Design gate). Triggers: "apply MSG standards", "corporate theme",
  "brand colors", "which theme to use", "MSG design guidelines".
metadata:
  version: 0.1.0
---

# msg Power BI Standards

> **This is msg's real design system** — the default brand shipped with this
> plugin. Every downstream skill in this bundle (`powerbi-report-design`,
> `powerbi-dashboard-architect`, etc.) applies it automatically. If you want
> your **own** brand instead of msg's, copy `../../template/company-powerbi-standards/`
> over this folder and fill in your own `tokens.json` — see that folder's
> `references/contract.md` for exactly what to fill in, and
> `references/contrast-checklist.md` for validating your own colors.

## Purpose

Apply msg corporate design standards and dashboard best practices to every report.

## Consumed By

- `powerbi-report-design` — resolves the theme file here at Step 5 (Theme), before adapting `assets/base.json`.
- `powerbi-dashboard-architect` — loads this skill before any report generation as the top-priority design authority.

## Corporate Colors

See `tokens.json` → `colors` for exact hex values, names, and measured contrast ratios. Usage constraints that aren't obvious from the data alone:

**Do not substitute `secondaryDecorative` for `secondaryAccessible` to "match the brand book."** The brand book's lighter petrol (`secondaryDecorative`) is a real color msg uses, but only in contexts (large fills, backgrounds) where WCAG's stricter thresholds don't apply — it fails AA for both text and graphics. Both shipped theme files already use `secondaryAccessible` for `good` and for any data series a user reads as text/labels — do not override this when adapting or authoring a theme.

## Fonts

See `tokens.json` → `fonts`. Never use decorative fonts.

## Theme Selection

Theme files live in this skill's own `themes/` folder. Resolve the path relative to the consuming skill.

See `tokens.json` → `themeSelection` for the file-to-archetype mapping.

## Layout Rules

See `tokens.json` → `layout` for the max-visuals limit and preferred/avoided structure.

**"Major visual" defined precisely** (do not guess): each `cardVisual`, chart (`barChart`, `columnChart`, `lineChart`, etc.), `tableEx`, `pivotTable`, or `azureMap` counts as 1. Slicers, textboxes, buttons, shapes, and navigation elements do not count toward the limit. A multi-value card showing 6 measures in one visual object is still 1 major visual, not 6. State the counted total explicitly in the design brief before handoff — do not leave it implicit.

## Typography Sizing

Callout (KPI card headline value) sizing is brand-critical — undersized KPI numbers are the most common way an msg report looks unpolished. See `tokens.json` → `themeSelection.<executive|operational>.calloutPt` (already set in the matching theme JSON). Do not shrink these when adapting a theme. If a custom override is required for a specific visual, it must not go below these values.

## Visual Type Rules

Use current visual types only: `cardVisual` (not `card`/`multiRowCard`), `azureMap` (not `map`/`filledMap`), `pivotTable` where a matrix is needed. See `powerbi-report-authoring`'s modern-visual-types guidance before authoring any visual — do not default to a deprecated type because it's familiar.

## Field Naming Rules

Every axis label, column header, legend entry, and card label must show a human-readable display name — never a raw database identifier (`customer_segment`, `Sum of fight_key`, `date_of_enrolment`). Set an explicit `displayName` on every bound field and every aggregation. This applies to pages, slicers, and table/column captions as well as measures — see `tokens.json` → `naming.measurePrefix` for the measure-specific prefix convention.

## Interaction and Tooltip Defaults

See `tokens.json` → `interaction`. Use `powerbi-report-authoring`'s `references/interactivity.md` for drillthrough/bookmark/tooltip mechanics; this skill only sets the msg-specific default, not the implementation.

## KPI Rules

Color assignment: see `tokens.json` → `semantics` (which color token maps to `good`/`bad`/`neutral`). Use color sparingly. Color must never be the only indicator.

Both shipped theme files set `good` and `bad` to colors of equivalent contrast strength so positive/on-target indicators render at the same visual weight as negative ones — do not let that asymmetry creep in when adapting a theme; it makes bad news look more visually prominent than good news by accident.

### Palette Overflow Policy

`dataColors` ships exactly `tokens.json` → `paletteOverflowPolicy.dataColorsCount` entries per theme. Power BI auto-generates a color for any category beyond that via hue/saturation shift — that color will not be on-brand. Before finalizing any chart with more categories than the palette:

- Use one of `tokens.json` → `paletteOverflowPolicy.options` (collapse to "Other", sequential ramp, or gray past the top-N by rank).
- Never let an overflow category silently take Power BI's auto-generated color. State explicitly in the design brief which overflow strategy was used, if any.

(General palette-size theory — why 6-8 is the practical cap — lives in `powerbi-report-design/references/color.md`; this section only states msg's specific count and options.)

## Delivery Rules

See `tokens.json` → `delivery`. Apply the corporate theme automatically. Every report must comply with msg standards.
