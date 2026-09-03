# Changelog

msg's release notes for `msg-powerbi-standards`. Separate from the
upstream-only root `CHANGELOG.md`, which tracks Microsoft's
`skills-for-fabric` releases.

## [0.4.1] - 2026-09-03

### Fixed

- **`powerbi-report-planning`** -- a fully-specified `requirements.md`/brief
  was being read as license to skip the entire skill, not just its
  clarification questions: Round 0's `powerbi-governance` invocation, the
  locked `_brief/report-spec.md`, and the approval gate were all being
  bypassed when the input was already complete. The skill now states
  explicitly, in the MUST/AVOID lists and in Round 0 itself, that a
  complete input only shortcuts which questions get asked -- never these
  process steps.
- **`powerbi-report-design`** -- a customized `assets/base.json` brand
  palette (colors/fonts different from the shipped Okabe-Ito default) was
  being overwritten by tone-catalog-driven colors, because the pre-flight
  checklist's "tone propagated to color" item assumed `base.json` was still
  the generic default. Added a locked-brand check before Step 1, a
  verbatim-reuse rule in Step 5, and an exception in the checklist item so
  a customized brand is treated as fixed, not as a starting template to
  replace.
- **`powerbi-report-design`** -- a detailed, page-by-page requirements file
  was being transcribed onto pages in prompt order instead of being routed
  through Step 2's archetype/layout-variant selection and Step 4's
  grid/space-audit composition, producing cramped, poorly balanced pages.
  The skill now states that a requirements file specifies page content, not
  page layout -- routing and composition still run per page regardless of
  how detailed the input is.

## [0.4.0] - 2026-09-01

### Added

- **`powerbi-governance`** -- change-control and measure-governance skill:
  resolves a change-request reference, reads a local change-log ledger for
  prior history before new work starts, and enforces msg's measure-naming
  convention and approval gate. Invoked by `powerbi-report-planning`,
  `powerbi-report-design`, `semantic-model-authoring`, and
  `powerbi-report-management` at specific steps; has no triggers of its own.
