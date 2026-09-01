# Change-Request (CR) Intake

## 1. Classify the request

- **External** — the user supplies an ADO work item number, a GitHub issue
  URL, or some other ticket reference in the prompt. Use it verbatim as the
  CR reference (e.g. `CR-118` for ADO work item #118, or the literal issue
  URL if there's no short id). Do not generate a new id in this case.
- **Explicit, no external ticket** — the user asks for a change in chat with
  no ticket mentioned. Generate a CR reference:

  ```
  CR-YYYYMMDD-NN
  ```

  `YYYYMMDD` is today's date; `NN` is a two-digit sequence number. Read the
  ledger first (Step 2 of the main workflow) and pick the next unused `NN`
  for today's date so ids never collide within the same day.

- **Implicit (revision of prior work)** — the user asks to modify something
  the ledger already shows as `Applied`, or asks to re-edit an already
  approved/locked `report-spec.md`. **Do not silently apply the edit.**
  Treat it as a new change needing its own CR reference, generated the same
  way as "explicit, no ticket" unless the user then supplies an external
  ticket for it.

## 2. Read the ledger before asking anything

Follow [ledger-schema.md](ledger-schema.md)'s read algorithm. Find every
entry that matches the target workspace/model/report by name.

## 3. Surface relevant history proactively

This is not optional — it's the core value of this skill. Before asking the
intake question, tell the user what the ledger shows, especially anything
`Reverted` or `Blocked`. Example:

> Note: `m_Revenue_Variance` was removed on 2026-08-10 per CR-118 because
> the base period was wrong — still want to re-add it, and is that fixed
> this time?

If nothing matches, say so plainly: "No prior governance history found for
`<target>`."

## 4. Ask the intake gate

Exactly one question, adapted to context:

> This looks like a change to `<item/workspace/model>`. I don't see an
> external ticket for it, so I'll track it as `<generated CR id>`. Confirm:
> what's changing and why, in one line? (Or tell me the ADO/GitHub reference
> if this already has one.)

Wait for the answer. The answer's text becomes the ledger entry's `Notes`
field. Do not let the calling skill proceed to its next step until this is
answered.

## 5. Hand off

Return the resolved CR reference (and, for measure changes, the
naming/approval-gate findings from the main SKILL.md) to whichever skill
invoked this one, so it threads through the rest of that skill's own
workflow and, eventually, into the ledger entry (Workflow step 6 in
[../SKILL.md](../SKILL.md)).

Optionally, if `git-integration-operations-cli` is being used to commit the
change, the same CR reference can be included in its `commitToGit` `comment`
field — this is a nice-to-have cross-reference, not a requirement this
skill enforces.
