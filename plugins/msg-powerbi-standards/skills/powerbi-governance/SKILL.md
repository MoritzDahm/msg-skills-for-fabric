---
name: powerbi-governance
description: >-
  Change-control and measure-governance authority for msg Power BI work:
  resolves a change-request (CR) reference, reads the on-disk governance
  ledger (`./_governance/change-log.md`) for prior history on the target
  workspace/model/report before new work starts — proactively surfacing
  anything previously reverted or blocked — and enforces msg's measure-naming
  convention and approval gate for semantic-model changes. Corporate
  color/theme/layout design authority is NOT part of this skill; that stays
  entirely with `powerbi-report-design`. This skill is invoked BY
  `powerbi-report-planning`, `powerbi-report-design`, `semantic-model-authoring`,
  and `powerbi-report-management` at specific steps — it has no
  report/dashboard-building triggers of its own. Use directly only when the
  user explicitly asks to (1) look up what changed and why for a
  workspace/model/report, (2) record or close a change-request entry by
  hand, or (3) look up msg's measure-naming convention outside of an
  authoring flow. Triggers: "what changed in this workspace", "show the
  change log", "why was this measure removed", "record this change", "log a
  change request", "what's our measure naming convention".
metadata:
  version: 0.1.0
---

> **Update Check — ONCE PER SESSION (mandatory)**
> The first time this skill is used in a session, run the **check-updates** skill before proceeding.
> - **GitHub Copilot CLI / VS Code**: invoke the `check-updates` skill.
> - **Claude Code / Cowork / Cursor / Windsurf / Codex**: compare local vs remote package.json version.
> - Skip if the check was already performed earlier in this session.

# Power BI Governance Skill

**Not This Skill** — this skill does not build, design, author, or publish
reports or semantic models, and it does not own corporate color/theme/layout
decisions. For building/planning a report end to end use
`powerbi-report-planning`; for visual design and theme use
`powerbi-report-design`; for PBIR file mechanics use
`powerbi-report-authoring`; for Fabric publish/CRUD use
`powerbi-report-management`; for measures/tables/relationships use
`semantic-model-authoring`. This skill supplies the CR reference, the
prior-history read-back, and msg's measure-naming/approval-gate rules those
skills consult at specific steps, and it owns the ledger file they write to
afterward.

## Must/Prefer/Avoid

### MUST

- Read `./_governance/change-log.md` (in the project's cwd, not this skill's
  own folder) and surface any matching prior entries — especially
  `Reverted`/`Blocked` ones — before any new governed change starts.
- Resolve a CR reference (external, generated, or implicit-revision) before
  handing control back to the calling skill; never let a change proceed with
  no CR reference.
- Treat a request to modify anything the ledger already shows as `Applied`
  (or an already-approved/locked `report-spec.md`) as a new change needing
  its own CR — do not silently apply the edit.
- Apply the `m_` measure-naming prefix and the approval gate (explain value →
  show DAX → wait for approval) to every new/changed measure. This
  convention takes priority over `semantic-model-authoring`'s own generic
  `references/naming-conventions.md` measure guidance whenever governance is
  invoked — say so explicitly so it isn't mistaken for a contradiction.
- Append one ledger entry per change once the calling skill reports the
  change landed, was blocked, or was rejected — never leave a resolved CR
  unlogged.
- Verify a marked Date table with a contiguous, unique-per-row date column
  exists before approving any time-intelligence measure (YTD/MTD/QTD/
  prior-period); if missing, recommend a calendar table via
  `semantic-model-authoring` and get approval rather than accepting a
  hand-rolled FILTER workaround.

### PREFER

- Generate the ledger file from `assets/change-log-template.md` on first use
  in a project rather than hand-rolling the header.
- Keep the CR-confirmation question to one line; don't re-ask for details
  the user already gave in the same turn.
- Cross-reference reverted/blocked entries by CR id in `Notes` rather than
  duplicating the reasoning across entries.

### AVOID

- Do not resolve theme, color, palette, or layout-density choices — that's
  `powerbi-report-design`'s domain even when this skill is invoked alongside
  it.
- Do not redesign or restructure a semantic model beyond the specific change
  under governance; the model is assumed customer-provided.
- Do not touch non-Power-BI workloads (Spark, Lakehouse, Warehouse,
  Dataflow, Eventhouse, Activator, Pipelines) under this skill's scope.
- Do not modify an existing semantic model automatically — the approval gate
  is mandatory even for msg's own recommended measures.

## Workflow

1. **Resolve target** — take the workspace / semantic model / report name
   from whichever skill invoked this one.
2. **Read the ledger** — see [references/ledger-schema.md](references/ledger-schema.md).
   If `./_governance/change-log.md` doesn't exist yet, note "no prior
   history" and move on; otherwise scan for entries matching the target and
   summarize them to the user, calling out any `Reverted`/`Blocked` status
   and its `Notes` reason *before* anything else — this is the proactive
   history surfacing, not an optional afterthought.
3. **CR intake** — see [references/cr-intake.md](references/cr-intake.md) for
   the full external/explicit/implicit classification logic. Ask the
   one-line confirm-and-describe question, wait for the answer, and resolve
   a CR reference.
4. **Apply measure-governance rules** — when the calling skill is
   `semantic-model-authoring` (directly, or via `powerbi-report-planning`'s
   Implementation-After-Approval step), enforce the `m_` naming prefix, the
   time-intelligence Date-table prerequisite, and the approval gate before
   any measure is created or modified.
5. **Hand back** the resolved CR id (and any naming/approval findings) to
   the calling skill so it can proceed.
6. **Write the ledger entry** — once the calling skill reports the change's
   outcome (applied / blocked / rejected / reverted), append one entry per
   [references/ledger-schema.md](references/ledger-schema.md) to
   `./_governance/change-log.md`, creating the file from
   `assets/change-log-template.md` if it doesn't exist yet.

## Measure Naming

Prefix: `m_`. Examples: `m_Revenue`, `m_Revenue_YTD`, `m_Revenue_Variance`,
`m_Revenue_Variance_Pct`. Avoid: `Measure1`, `SalesCalc`, `Revenue_Final_v2`.

## Measure Assessment (before building on an existing model)

1. Inspect available measures.
2. Assess naming quality, business-logic quality, and reusability.
3. Identify missing measures (time intelligence, variance, contribution %,
   rank, target-achievement, etc.) and recommend them where useful.
4. Report findings to the user; never apply changes without approval.

## Gotchas

- The old `company-powerbi-standards`/`powerbi-dashboard-architect` skills
  tried to own both design authority and measure governance, and their own
  triggers ("build me a dashboard", "publish this to Fabric") collided with
  `powerbi-report-planning`/`powerbi-report-authoring`'s triggers. Keep this
  skill's triggers narrow — resist adding build/design verbs even if it
  seems convenient.
- Fabric's own deploy/commit APIs don't give traceability for free:
  `deployment-pipelines-authoring-cli`'s deploy `note` field is write-only
  (never returned by the API), and `git-integration-operations-cli` exposes
  no commit-history read API. The ledger file is the only durable record —
  don't assume either API surfaces history back later.
- Threading the CR id into `deployment-pipelines-authoring-cli`'s deploy
  `note` field is a natural future extension but is out of scope for this
  skill today.

## Validation Checklist

- [ ] `./_governance/change-log.md` read (or confirmed absent) before any
      new work started
- [ ] Relevant prior entries (especially Reverted/Blocked) surfaced to the
      user before the CR question
- [ ] CR reference resolved (external / generated / implicit) and confirmed
      with the user
- [ ] Measure naming (`m_` prefix) and approval gate applied, if measures
      were touched
- [ ] Ledger entry appended after the change's outcome is known
