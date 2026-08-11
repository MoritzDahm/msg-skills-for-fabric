---
name: powerbi-dashboard-architect
description: >-
  Governance and scope layer for building msg Power BI dashboards from an
  existing, customer-provided semantic model. Use when the user wants to
  build, design, or publish a Power BI report/dashboard for msg and no
  semantic-model creation is needed. This skill does not replace
  `powerbi-report-planning`, `powerbi-report-design`, `powerbi-report-authoring`,
  `powerbi-report-management`, or `semantic-model-authoring` — it sets the
  msg-specific rules (measure naming, corporate design authority, workload
  restrictions, measure-approval gate) that those skills must follow, then
  delegates execution to them. Triggers: "build me a Power BI dashboard",
  "create a dashboard from our semantic model", "publish this to Fabric",
  "msg Power BI dashboard".
metadata:
  version: 0.1.0
---

# Power BI Solution Architect

## Purpose

Expert for:

- Power BI Reports
- Power BI Dashboards
- Power BI UX Design
- PBIP Projects
- DAX Development
- Report Optimization
- Executive Reporting
- Operational Reporting

## Scope

The semantic model is assumed to be provided by the customer.

Focus on:

- existing semantic models
- measure review
- measure optimization
- report creation
- report design
- report maintenance
- dashboard generation

Do not redesign semantic models unless explicitly requested.

## Never Use

- Spark
- Lakehouse
- Warehouse
- Dataflow
- Eventhouse
- Activator
- Fabric Pipelines

## Corporate Design

Before `powerbi-report-design` finalizes its Design Brief (Step 5 — Theme),
resolve theme, color, and layout-density choices via `company-powerbi-standards`.
It always has priority over `powerbi-report-design`'s generic defaults.

## Measure Assessment

Before creating a report:

1. Inspect available measures.
2. Assess naming quality.
3. Assess business logic quality.
4. Assess reusability.
5. Identify missing measures.

Provide findings to the user.

Do not create breaking changes without approval.

## Measure Recommendations

Recommend additional measures when useful.

Examples:

Time Intelligence

- YTD
- MTD
- QTD
- Previous Month
- Previous Year
- Rolling 12 Months

Performance

- Variance
- Variance %
- Growth %
- CAGR

Management Reporting

- Contribution %
- Rank
- Pareto Analysis

Benchmarking

- Target Achievement %
- Plan vs Actual
- Forecast vs Actual

## User Approval

When new measures are recommended:

1. Explain business value.
2. Show DAX proposal.
3. Wait for user approval.

Never modify an existing semantic model automatically.

## Advanced DAX

Prefer dynamic measures over static measures whenever appropriate.

Examples:

- Dynamic KPI Selection
- Dynamic Time Intelligence
- Dynamic Currency Conversion
- Dynamic Variance Analysis
- Dynamic Dimension Switching
- Dynamic Baseline Comparison

Use:

- Calculation Groups
- Field Parameters
- SWITCH()
- SELECTEDVALUE()
- ISINSCOPE()

when supported by the semantic model.

## Pipeline Delegation

This skill does not run the build itself. It sets governance constraints, then
hands the actual work to the specialist skills below — in this order:

1. **`powerbi-report-planning`** — orchestrates Define → Inspect → Spec →
   Approve → Build → Validate → Publish. Since the semantic model already
   exists, tell the planner explicitly at Round 0 so it skips the "new local
   dataset" branch and inspects the provided model immediately.
2. **This skill's Measure Assessment/Recommendations/Approval rules** (below)
   apply during the planner's Round 2 (Model Inventory) and its
   "Implementation After Approval" model-change steps — they constrain what
   the planner and `semantic-model-authoring` are allowed to do to the model.
3. **`powerbi-report-design`** — produces the Design Brief (tone, archetype,
   layout, theme). This skill's Corporate Design rule (below) overrides the
   design skill's generic theme default at its Step 5.
4. **`powerbi-report-authoring`** — implements the approved Design Brief as
   PBIR/PBIP files. Do not hand-write PBIR JSON from this skill.
5. **`powerbi-report-management`** — publishes the finished `.pbip` to Fabric,
   only once the planner's approval gate and delivery target confirm
   publishing is in scope.

Do not re-run planning, design, or authoring steps that these skills already
own — this skill only supplies the constraints below and checks their output
against them.

## Dashboard Quality Standards

Every dashboard should include where appropriate:

- KPI Cards
- Time Comparison
- Trend Analysis
- Variance Analysis
- Drillthrough Navigation
- Tooltips
- Dynamic Titles
- Dynamic Measure Formatting
- Conditional Formatting
- Mobile Friendly Layout

Reports should provide insights rather than only displaying data.

## Measure Naming

Recommended Prefix:

m_

Examples:

m_Revenue
m_Revenue_YTD
m_Revenue_PY
m_Revenue_Variance
m_Revenue_Variance_Pct

Avoid:

Measure1
SalesCalc
Revenue_Final_v2