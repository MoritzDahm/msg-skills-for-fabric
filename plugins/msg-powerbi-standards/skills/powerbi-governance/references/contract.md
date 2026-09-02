# Settings Contract

Lookup table of "what a consumer needs to know" → "where it lives in
[../settings.md](../settings.md)". Consumers should resolve values by
reading the named section, not by hardcoding the literal value in their own
prose — that's the whole point of centralizing settings here.

| Consumer | Question | `settings.md` section | Required |
|---|---|---|---|
| `powerbi-governance` itself | Where does the ledger live, and what template seeds a new one? | Ledger | Yes |
| `powerbi-governance` itself | How are CR ids generated, and which external ticket formats are recognized verbatim? | Change-Request (CR) Reference | Yes |
| `semantic-model-authoring` | What's the measure-naming prefix? Is the approval gate mandatory? Is the time-intelligence prerequisite enforced? | Measure Governance | Yes (pre-change + post-outcome) |
| `powerbi-report-planning`, `powerbi-report-management` | What fields does a ledger entry need, and are there extra org-specific fields to include? | Ledger Entry Fields | Yes (pre-change + post-outcome) |
| `powerbi-report-planning` | Which workloads are out of scope for this governance layer? | Out-of-Scope Workloads | Yes |

Nothing enforces this automatically — this is a convention, not a schema
validator. If you rename a section heading in `settings.md`, update this
table and the `SKILL.md`/reference pointers that name it, or a consumer
will silently fail to find the section it's looking for.
