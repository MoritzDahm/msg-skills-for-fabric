# msg Power BI Governance Settings

> Edit this file to customize `powerbi-governance`'s behavior. `SKILL.md` and
> its `references/` files point at the sections below instead of restating
> values — edit here, not in prose. Re-read this file on every invocation;
> do not cache its values across sessions. See
> [references/contract.md](references/contract.md) for which consuming
> skill relies on which section.

## Ledger

- **Path:** `./_governance/change-log.md`
- **Template:** `assets/change-log-template.md`

## Change-Request (CR) Reference

- **Generated ID format:** `CR-{YYYYMMDD}-{NN}` — date plus a two-digit
  daily sequence number, incremented past any id already used that day.
- **Recognized external ticket references** (used verbatim as the CR
  reference instead of generating one):
  - ADO work items — e.g. "#118", "work item 118"
  - GitHub issue URLs — e.g. `https://github.com/org/repo/issues/42`

## Measure Governance

- **Naming prefix:** `m_` — examples: `m_Revenue`, `m_Revenue_YTD`,
  `m_Revenue_Variance`. Avoid: `Measure1`, `SalesCalc`, `Revenue_Final_v2`.
- **Approval gate required:** Yes. Explain business value, show the DAX
  proposal, wait for explicit approval before creating or modifying any
  measure. Never auto-modify an existing semantic model.
- **Time-intelligence prerequisite enforced:** Yes. Verify a marked Date
  table with a contiguous, unique-per-row date column before approving any
  YTD/MTD/QTD/prior-period measure; if missing, recommend a calendar table
  via `semantic-model-authoring` and get approval rather than accepting a
  hand-rolled FILTER workaround.

## Ledger Entry Fields

Fixed order for every entry: Requester, Trigger type, Workspace, Semantic
model / Report, Items changed, Skills executed, Governance checks, Status,
Notes.

Additional organization-specific fields (appended after Notes) — add a
bullet per field, or leave empty:

- _(none configured)_

## Out-of-Scope Workloads

This skill and its consumers never touch these under governance scope:
Spark, Lakehouse, Warehouse, Dataflow, Eventhouse, Activator, Pipelines.
