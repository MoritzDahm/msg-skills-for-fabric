# msg-powerbi-standards

Built by **msg**: a customizable Power BI corporate-standards skill for the
[Microsoft skills-for-fabric](https://github.com/microsoft/skills-for-fabric)
Power BI skills (`powerbi-report-design`, `powerbi-report-planning`,
`powerbi-dashboard-architect`). Those skills already know how to look for a
skill named `company-powerbi-standards` and treat it as the top-priority
design authority when present — install nothing and they fall back to generic
defaults; install this, filled in with your own brand, and every report they
generate follows your standards instead.

> **Relationship to Microsoft's skills-for-fabric:** this plugin is an
> independent extension built by msg to plug into Microsoft's public
> `skills-for-fabric` project. It is not published by, affiliated with, or
> endorsed by Microsoft — it simply targets the extension point that project's
> Power BI skills already expose. You need `skills-for-fabric`'s
> `powerbi-authoring` plugin installed for this to have any effect.

## Installing via marketplace

This folder is deliberately self-contained: it carries both a plugin manifest
(`.claude-plugin/plugin.json`) and its own marketplace manifest
(`.claude-plugin/marketplace.json`, mirrored under `.github/plugin/` for
Copilot CLI) that lists only this one plugin, under a separate marketplace
named `msg-collection` — distinct from Microsoft's `fabric-collection`, so
installing msg's standards never implies installing or being bundled with
Microsoft's plugins.

**Once this folder is published as its own repository** (`repository` in
`plugin.json` and `marketplace.json` is currently a placeholder — fill it in
first), installation looks exactly like the upstream bundles:

```bash
/plugin marketplace add <msg-org>/<msg-repo>
/plugin install msg-powerbi-standards@msg-collection
```

**Until then**, `marketplace.json` here is inert from inside this monorepo —
`/plugin marketplace add` resolves a manifest at the target repository's
*root*, and this one is nested under `plugins/msg-powerbi-standards/`, not at
`MoritzDahm/msg-skills-for-fabric`'s root (that root still serves Microsoft's
`fabric-collection`). For now, either extract this folder to its own repo (the
manifests need no path changes to work there), or install it manually by
copying `skills/company-powerbi-standards/` into your project's skills folder
— see your tool's docs for local/dev marketplace testing if it supports a
filesystem path.

## What's in here

```
skills/company-powerbi-standards/
  SKILL.md                       # orchestration + policy prose — contains NO literal
                                  # brand values, only references to tokens.json
  tokens.json                    # the ONE file you edit — every color, font,
                                  # size, and policy number lives here (blank template)
  themes/
    theme-executive.json         # Power BI theme JSON for exec/board-level pages
    theme-operational.json       # Power BI theme JSON for ops/monitoring pages
  references/
    contract.md                  # exactly what the three consumer skills expect
                                  # from this skill — read before restructuring
    contrast-checklist.md        # how to verify your own colors pass WCAG AA
                                  # before you commit them to tokens.json

examples/msg/
  SKILL.md, tokens.json, themes/*.json, README.md
                                  # msg's own real brand, fully filled in —
                                  # a ready-to-copy drop-in, or a worked
                                  # reference while you build your own
```

## Quick start

**Want msg's own look?** See `examples/msg/README.md` — it's a three-file
copy.

**Want your own brand?** Follow the steps below; use `examples/msg/` as a
reference for what a filled-in version looks like.

## Why it's split this way

A brand rebrand should be a one-file edit, not a hunt across prose and JSON.
So:

1. **One source of truth.** All literal values live in `tokens.json`.
   `SKILL.md` refers to token keys (`colors.primary`), never a hex code.
2. **No restated theory.** `SKILL.md` states only *your organization's*
   choices and any deviation from the generic default; it points to
   `powerbi-report-design/references/{color,typography,accessibility}.md`
   for the underlying rationale instead of re-explaining it.
3. **A real worked example ships alongside the blank template** (`examples/msg/`)
   so "what does a filled-in `tokens.json` actually look like" is never a
   guess.

## Setup (your own brand)

1. **Install this plugin** alongside `powerbi-authoring` (from
   `skills-for-fabric`) in your project.
2. **Edit `skills/company-powerbi-standards/tokens.json`** with your
   organization's brand colors, fonts, and policy numbers. Check every color
   pair against `skills/company-powerbi-standards/references/contrast-checklist.md`
   before committing it — a color that fails WCAG AA for text should be
   marked decorative-only, exactly like `secondaryDecorative` in the
   placeholder tokens.
3. **Regenerate the two theme JSON files** to match `tokens.json`. Use the
   field-mapping table in `references/contract.md` — it's a small, fixed set
   of fields (`dataColors`, `good`/`neutral`/`bad`, `textClasses.*`,
   `foreground`/`background`).
4. **Update `SKILL.md`'s frontmatter** (`description`, trigger phrases) to
   name your organization instead of leaving the placeholder language.
5. **Keep the skill named `company-powerbi-standards`.** The three consumer
   skills look it up by that exact name — rename it only if you also update
   those references (search their `SKILL.md` files for
   `company-powerbi-standards`).

## What NOT to do

- Don't hardcode a literal hex/pt value anywhere in `SKILL.md` — if you catch
  yourself typing a color code outside `tokens.json` or the theme JSON files,
  stop and add a token for it instead.
- Don't restate WCAG contrast math, palette-size theory, or typography scale
  rationale here — that's `powerbi-report-design`'s job, and a second copy
  will eventually disagree with the first.
- Don't assume the two example theme files (`theme-executive.json` /
  `theme-operational.json`) are your only options — `tokens.json` →
  `themeSelection` can name as many theme files and archetype mappings as
  your organization actually needs.

## License

MIT — see the plugin manifest (`.claude-plugin/plugin.json`).
