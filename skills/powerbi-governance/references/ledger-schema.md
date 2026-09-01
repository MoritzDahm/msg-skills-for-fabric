# Governance Ledger Schema

The ledger is a single plain-markdown file, **not** a database. It's meant
to be read in full by the agent (Read tool handles it directly) and scanned
by eye/grep for the workspace, model, or report name under discussion — no
YAML/JSON parser or query language required.

## Location

`./_governance/change-log.md`, relative to the project's current working
directory (sibling to `powerbi-report-planning`'s `./_brief/report-spec.md`).
This lives in the customer's project — never inside this skill's own folder.

If the file doesn't exist yet, that means "no governed history for this
project" — do not treat it as an error. Create it from
[`../assets/change-log-template.md`](../assets/change-log-template.md) the
first time an entry needs to be written.

## Read algorithm

1. Read the whole file (it's bounded, human-scale markdown).
2. Scan every entry's `Workspace:`, `Semantic model:`, `Report:`, and
   `Items changed:` lines for the name(s) relevant to the current request.
3. Collect all matches in date order (entries are appended oldest-first, so
   reading top-to-bottom is already chronological).
4. Flag any matched entry with `Status: Reverted` or `Status: Blocked` —
   these are the ones to proactively surface before asking anything else.
5. If nothing matches, say so explicitly ("no prior governance history found
   for `<target>`") rather than staying silent about having checked.

## Entry format

One `##` H2 header per entry: `## <CR reference> — <YYYY-MM-DD>`. Fields are
a fixed-order bullet list immediately under the header. Never delete an
entry; a later change to the same item gets its own new entry, and the
older entry may be updated only to point at the newer one via `Notes`.

Fields, always in this order:

| Field | Values | Notes |
|---|---|---|
| `Requester` | name or email | who asked for the change |
| `Trigger type` | `explicit` \| `implicit-revision` \| `external` | see [cr-intake.md](cr-intake.md) |
| `Workspace` | name (+ id if known) | the Fabric workspace |
| `Semantic model` and/or `Report` | name (+ id if known) | whichever applies; both if the change touched both |
| `Items changed` | bullet list | one bullet per item: `<type> \`<name>\` — <added\|updated\|discarded> (<skill that executed it>)` |
| `Skills executed` | comma-separated skill names | e.g. `semantic-model-authoring, powerbi-report-authoring` |
| `Governance checks` | short prose | which rules were verified (naming, time-intelligence prerequisite, approval) |
| `Status` | `Applied` \| `Reverted` \| `Blocked` \| `Pending-Approval` | current state of this specific change |
| `Notes` | free text | the "why" — reasons, caveats, cross-references to related CRs. This is the field that gets read back to the user later. |

## Example entries

```markdown
## CR-20260901-01 — 2026-09-01

- **Requester:** moritz.dahm@msg.group
- **Trigger type:** explicit (chat request, no external ticket)
- **Workspace:** Sales Analytics (ws id: 8f2e...-workspace)
- **Semantic model:** Sales Model (item id: 3ac1...-model)
- **Items changed:**
  - measure `m_Revenue_Variance` — added (semantic-model-authoring)
- **Skills executed:** semantic-model-authoring
- **Governance checks:** measure naming (m_ prefix) OK; time-intelligence
  date-table prerequisite verified; user approved DAX proposal on 2026-09-01
- **Status:** Applied
- **Notes:** First variance measure for this model; no prior history found
  for this workspace.

## CR-118 — 2026-08-10

- **Requester:** moritz.dahm@msg.group
- **Trigger type:** external (ADO work item #118)
- **Workspace:** Sales Analytics (ws id: 8f2e...-workspace)
- **Semantic model:** Sales Model (item id: 3ac1...-model)
- **Items changed:**
  - measure `m_Revenue_Variance` — discarded (semantic-model-authoring)
- **Skills executed:** semantic-model-authoring
- **Governance checks:** user approved removal; reason recorded below
- **Status:** Reverted
- **Notes:** Removed because finance flagged the variance base period as
  incorrect (compared to budget instead of prior year). Do not re-add
  without confirming the correct base period with finance first.
```
