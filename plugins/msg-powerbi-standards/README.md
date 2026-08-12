# msg-powerbi-standards

Built by **msg**: a complete, self-sufficient Power BI toolkit — semantic
model authoring, report planning/design/authoring/management, Fabric
publishing, msg's governance rules, and msg's corporate design standards —
built on top of [Microsoft's skills-for-fabric](https://github.com/microsoft/skills-for-fabric).
Install this one plugin and you can plan, design, author, and publish a
Power BI report to Fabric end to end, styled to msg's brand by default.

> **Relationship to Microsoft's skills-for-fabric:** this plugin vendors
> several skills from Microsoft's public `skills-for-fabric` project
> (MIT-licensed — see `THIRD_PARTY_NOTICES.md`) plus msg's own additions. It
> is an independent redistribution by msg — not published by, affiliated
> with, or endorsed by Microsoft.

## Installing via marketplace

This folder is self-contained: it carries both a plugin manifest
(`.claude-plugin/plugin.json`) and its own marketplace manifest
(`.claude-plugin/marketplace.json`, mirrored under `.github/plugin/` for
Copilot CLI) under a separate marketplace named `msg-collection` — distinct
from Microsoft's `fabric-collection`.

**Once this folder is published as its own repository** (`repository` in
`plugin.json` and `marketplace.json` is currently a placeholder — fill it in
first), installation looks exactly like the upstream bundles:

```bash
/plugin marketplace add <msg-org>/<msg-repo>
/plugin install msg-powerbi-standards@msg-collection
```

That single install gives you everything — no separate install of
Microsoft's `powerbi-authoring` plugin needed.

**Until then**, `marketplace.json` here is inert from inside the parent
monorepo — `/plugin marketplace add` resolves a manifest at the target
repository's *root*, and this one is nested under `plugins/msg-powerbi-standards/`.
Extract this folder to its own repo first (the manifests need no path changes
to work there), or install manually by copying the whole `skills/` folder
below into your project's skills directory.

## What's in here

```
skills/
  check-updates/                 # vendored — shared update-check skill
  semantic-model-authoring/      # vendored — DAX, TMDL, semantic model authoring
  powerbi-report-planning/       # vendored — guided requirements -> build workflow
  powerbi-report-design/         # vendored — visual design guidance
  powerbi-report-authoring/      # vendored — PBIR/PBIP file mechanics
  powerbi-report-management/     # vendored — Fabric report item CRUD (publish, update)
  powerbi-dashboard-architect/   # msg original — governance layer (measure naming,
                                  # workload restrictions, corporate design gate)
  company-powerbi-standards/     # msg original — msg's real brand (the default)
    SKILL.md                     # orchestration + policy prose — NO literal brand
                                  # values, only references to tokens.json
    tokens.json                  # msg's actual colors, fonts, sizes, policy numbers
    themes/
      theme-executive.json       # Power BI theme JSON for exec/board-level pages
      theme-operational.json     # Power BI theme JSON for ops/monitoring pages
    references/
      contract.md                # exactly what the consumer skills expect from
                                  # this skill — read before restructuring
      contrast-checklist.md      # how to verify colors pass WCAG AA

template/
  company-powerbi-standards/     # blank, brand-neutral copy of the skill above —
                                  # use this if you want YOUR brand instead of msg's

THIRD_PARTY_NOTICES.md           # attribution for vendored Microsoft content
.mcp.json                        # powerbi-modeling-mcp registration (semantic model MCP)
```

## Quick start

**Want msg's own look?** Do nothing — `skills/company-powerbi-standards/` is
already msg's real brand and every other skill in this bundle uses it
automatically.

**Want your own brand?**

```bash
rm -rf skills/company-powerbi-standards
cp -R template/company-powerbi-standards skills/company-powerbi-standards
```

Then edit `skills/company-powerbi-standards/tokens.json` — see "Rebranding"
below.

## Why the standards skill is split this way

A rebrand should be a one-file edit, not a hunt across prose and JSON:

1. **One source of truth.** All literal values live in `tokens.json`.
   `SKILL.md` refers to token keys (`colors.primary`), never a hex code.
2. **No restated theory.** `SKILL.md` states only *this brand's* choices and
   any deviation from the generic default; it points to
   `powerbi-report-design/references/{color,typography,accessibility}.md`
   for the underlying rationale instead of re-explaining it.
3. **A real worked example is the default**, not a separate copy — so
   there's never a stale "example" drifting out of sync with what's actually
   shipped.

## Rebranding (replacing msg's standards with your own)

1. Copy the template over the default (see "Quick start" above).
2. Edit `skills/company-powerbi-standards/tokens.json` with your
   organization's brand colors, fonts, and policy numbers. Check every color
   pair against `references/contrast-checklist.md` before committing it — a
   color that fails WCAG AA for text should be marked decorative-only, exactly
   like `secondaryDecorative` in the placeholder tokens.
3. Regenerate the two theme JSON files to match `tokens.json`. Use the
   field-mapping table in `references/contract.md` — a small, fixed set of
   fields (`dataColors`, `good`/`neutral`/`bad`, `textClasses.*`,
   `foreground`/`background`).
4. Update `SKILL.md`'s frontmatter (`description`, trigger phrases) to name
   your organization instead of leaving the placeholder language.
5. Keep the skill named `company-powerbi-standards`. `powerbi-report-design`
   and `powerbi-dashboard-architect` look it up by that exact name — rename it
   only if you also update those two skills' `SKILL.md` files.
6. Decide whether you also want `powerbi-dashboard-architect` (msg's own
   governance layer — measure-naming prefix, workload restrictions,
   msg-branded triggers). If not, remove `skills/powerbi-dashboard-architect/`
   and its entry from `plugin.json`/`marketplace.json`; the rest of the
   bundle works fine without it.

## What NOT to do

- Don't hardcode a literal hex/pt value anywhere in `SKILL.md` — if you catch
  yourself typing a color code outside `tokens.json` or the theme JSON files,
  stop and add a token for it instead.
- Don't restate WCAG contrast math, palette-size theory, or typography scale
  rationale here — that's `powerbi-report-design`'s job, and a second copy
  will eventually disagree with the first.
- Don't assume the two shipped theme files (`theme-executive.json` /
  `theme-operational.json`) are your only options — `tokens.json` →
  `themeSelection` can name as many theme files and archetype mappings as you
  actually need.

## Keeping vendored skills in sync

`check-updates`, `semantic-model-authoring`, `powerbi-report-planning`,
`powerbi-report-design`, `powerbi-report-authoring`, and
`powerbi-report-management` are copied from msg's fork of
`microsoft/skills-for-fabric` (`skills/` at that fork's root), not symlinked
or submoduled — updates from upstream don't flow in automatically. Re-copy
those six folders from the fork when you want to pick up upstream fixes, and
re-apply any msg-specific patches (currently: `powerbi-report-design`'s
Step 5 no longer hardcodes msg's theme file names).

## License

MIT — see the plugin manifest (`.claude-plugin/plugin.json`) and
`THIRD_PARTY_NOTICES.md` for vendored-content attribution.
