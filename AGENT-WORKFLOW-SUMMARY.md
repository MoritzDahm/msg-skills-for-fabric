# How the Agent Builds a Power BI Report — Summary for Review

This summarizes the instructions Microsoft ships in `plugins/powerbi-authoring/skills/`
for building a Power BI report end-to-end. It is meant so you can validate what the
agent is being told to do **before** it acts on your reports. It does not cover the
`msg-powerbi-standards` plugin (your org's fork/overlay) — only the base
`powerbi-authoring` skills in this folder.

Four skills partition the work. Each owns one concern and hands off to the next:

```
powerbi-report-planning  →  powerbi-report-design  →  powerbi-report-authoring  →  powerbi-report-management
   (requirements/approval)     (visual design)           (PBIR file mechanics)        (publish to Fabric)
```

---

## 1. Planning (`powerbi-report-planning`) — requirements → locked spec → build

Used for "build me a dashboard" style requests. Not used for small edits to an
existing report (that goes straight to Authoring).

**Flow:** Define → Inspect → Spec → Approve → Build → Validate → Publish

- Runs **3–5 clarification rounds**, one question at a time, only asking what
  can't already be inferred from the prompt or inspected files:
  1. **Round 0 — Setup/dependencies**: which semantic model/dataset, and what
     tooling is available (Desktop, MCP, Node.js, etc.). Missing tools degrade
     the plan to "blocked/manual" rather than being silently skipped.
  2. **Round 1 — Audience & job-to-be-done**: who it's for (execs / analysts /
     operators / external / enthusiasts) and what decision it supports.
  3. **Round 2 — Model inventory & scope**: inspects the semantic model (via
     MCP, a modeling skill, or raw TMDL files) to catalog tables, measures,
     dimensions, risks (nulls, high-cardinality fields, broken relationships),
     and infers a first-build scope rather than re-asking what's already stated.
  4. **Round 3 — Narrative & page plan**: delegates to the Design skill for
     page archetypes; produces a numbered page list with visuals/fields/slicers
     per page.
  5. **Round 4 — Design identity, accessibility, delivery target**: delegates
     tone/signature choice to Design; asks where the report should land (local
     only, existing Fabric workspace, new model+report, update existing, or
     decide later).
- **Design Contract Gate**: before writing the spec, requires a canonical
  `Design Brief:` YAML block from the Design skill with a full mechanical
  layout for every page (grid regions, placements, an empty-space audit, a
  titled header, slicers placed top-right/filter rail, no bare oversized KPI
  card as the hero visual). If this is incomplete, it stops and fixes it
  first — it will not ask for approval on a shaky contract.
- **Output**: one file, `./_brief/report-spec.md`, containing both a
  human-readable spec (audience, scope, page plan, design identity, model
  requirements) and the embedded machine-readable YAML design contract. This
  is the single approval artifact.
- **Approval gate**: asks exactly one question — *"Approve this report spec so
  I can start building?"* — with options to approve or revise audience/scope/
  design. **Nothing is built before you approve.**
- **After approval**, it executes the full build itself: connects to the
  model, creates/validates any new measures, exports to TMDL, scaffolds the
  PBIP/PBIR project, hands off to Authoring to generate pages/visuals,
  validates, opens Power BI Desktop, reloads, screenshots every page, fixes
  issues it finds, and **only publishes to Fabric if you chose a delivery
  target that includes publishing**.

---

## 2. Design (`powerbi-report-design`) — what the report should look like

A design-only skill: it never writes report files, only produces a design
contract for the Authoring skill to implement.

**Workflow:**
1. **Data-first investigation** — inspects the model/fields before any design
   decision (distributions, cardinality, magnitudes).
2. **Design identity** — commits to one **tone** (e.g. "Editorial Newsroom")
   and one recurring **signature visual move** that must actually show up in
   typography/palette/layout choices, not just be named.
3. **Archetype routing per page** (not per report) — a single report often
   mixes archetypes across pages:
   - **Executive Summary** — C-suite, ≤10s scan, "is it on track?"
   - **Operational Monitor** — shift/NOC wallboard, "is it broken?"
   - **Analytical Canvas** — analyst hypothesis testing (default when unsure)
   - **Narrative Story** — author-driven, guided argument
   - **Comparative Benchmark** — ranking/variance, "relative to what?"
   Vague prompts trigger a stop-and-ask with 2–3 concrete named options rather
   than guessing. Each archetype also has 2–3 layout variants chosen by data
   signal, not by default habit.
4. **Chart selection** — matches each analytical question to a chart type
   using an encoding-strength hierarchy (position → length → angle → area →
   hue); explicitly checks for degenerate charts (flat lines, two-bar charts).
5. **Visual configuration** — sort order, color strategy, labels, conditional
   formatting per visual type.
6. **Theme** — adapts a base theme to the identity, preserving safeguards
   (textbox padding, card spacing, table styling) rather than blunt wildcard
   overrides; preserves an existing theme unless a rebrand was requested.
7. **Canonical design contract** — emits the `Design Brief:` YAML consumed by
   Planning/Authoring, including a strict per-page mechanical layout
   (canvas size, 12-column grid, region boxes, placements, a `space_audit`
   with no unplaced regions).
8. **Review & handoff** — self-checks against a pre-flight checklist and known
   anti-patterns before handing off.

**Called-out failure modes it explicitly guards against** (worth knowing since
these are common report-quality complaints):
- Tone declared but not visually reflected.
- Overlapping/clipped controls; slicers overlapping charts.
- Redundant KPI callouts that just repeat a chart's number.
- Defaulting to a full date-range slicer when a simple Year picker would do.
- Raw database field names left on axes/legends/headers (e.g. `method_category`
  instead of "Method").
- Decimal rates shown as `0.53` instead of `53%`.
- Monochrome bar charts when category contrast was intended.

---

## 3. Authoring (`powerbi-report-authoring`) — turning the design into PBIR files

This is the file-mechanics layer: creates/edits the actual PBIR/PBIP JSON
(pages, visuals, filters, slicers, themes, formatting) via a CLI, not by
hand-guessing JSON from memory.

- **Requires two CLIs** (Node.js 20+): `@microsoft/powerbi-report-authoring-cli`
  and `@microsoft/powerbi-desktop-bridge-cli`, installed globally.
- **Never guesses PBIR schema** — looks up visual types, roles, formatting
  objects, and enum values via CLI commands (`catalog describe`,
  `formatting describe-object`, `formatting search`) before writing JSON.
- **Always uses modern visual types**, refusing legacy ones:
  - `cardVisual` instead of `card`/`multiRowCard`
  - `tableEx` instead of `table`; `pivotTable` instead of `matrix`
  - `azureMap` instead of `map`/`filledMap`
- **Edit → Validate → Reload → Screenshot loop** for every rendered change:
  1. Edit PBIR JSON
  2. `powerbi-report-author validate` — fix all errors before proceeding
  3. Check Power BI Desktop status (won't reload over unsaved user changes)
  4. Reload the open PBIP in Desktop
  5. Screenshot every affected page and review it against a checklist
  6. Only then reports the change complete
- Maintains a long table of known pitfalls (wrong filter syntax, missing
  `nativeQueryRef`, reused IDs, wrong role names, schema-version edits,
  PowerShell JSON corruption, color/contrast traps, theme caching quirks,
  etc.) that it checks itself against before/while editing.
- For large builds, keeps design brief + model inventory + cross-page
  consistency centralized in one agent rather than fully delegating PBIR
  generation to sub-agents (to avoid inconsistent output across pages).

---

## 4. Management (`powerbi-report-management`) — publishing to Fabric

Pure **transport** layer: gets/creates/updates/deletes report items in a
Fabric workspace via the REST API. It explicitly does **not** author any PBIR
content itself — every file must come from the Authoring skill.

- **Local-first, publish-only-on-request**: edits to a local `.pbip` stay
  local; nothing is pushed to Fabric unless you explicitly ask to
  publish/upload/push — even if the report was previously published.
- **Publishing workflow** when you do ask to publish a local `.pbip`:
  1. Confirms the target workspace once (reused for both model + report).
  2. **Explicitly asks**: publish the local semantic model too, or bind to an
     existing workspace model? (Never chosen silently.)
  3. Resolves the semantic model ID either way.
  4. **Always diffs PBIR bindings against the resolved model's actual TMDL**
     (table/column/measure names) before publishing — this exists because a
     model deploy can silently rename things and break visuals otherwise.
  5. Rewrites `definition.pbir` from local `byPath` to Fabric's required
     `byConnection` form.
  6. Checks whether a report of that name already exists in the workspace and
     asks whether to overwrite, publish under a new name, or cancel.
  7. Base64-encodes and uploads all PBIR parts, polls the long-running
     operation to completion (never retries a create after `202`, to avoid
     duplicate reports).
  8. Cleans up temporary local files.
  9. Surfaces the workspace/report URL — it cannot programmatically verify
     rendering itself; that needs a browser.
- Only supports the modern **PBIR** format; refuses legacy `PBIR-Legacy`
  reports.

---

## What this means in practice for a "build me a report" request

1. You'll be asked a handful of targeted questions (audience, scope, design
   feel, delivery target) — not a long interview, and not silence.
2. You'll see one spec document (`_brief/report-spec.md`) with both the
   plain-English plan and the exact technical design contract, and you must
   explicitly approve it before anything is built.
3. After approval, the agent builds the model changes, report pages/visuals,
   validates the files, opens Power BI Desktop, reloads, and screenshots the
   result to self-check — all locally.
4. Nothing is pushed to your Fabric workspace unless your approved delivery
   target said so, and even then it asks again about the semantic-model
   handling before publishing.
