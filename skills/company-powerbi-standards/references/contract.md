# Contract — What Consuming Skills Expect

`powerbi-report-design`, `powerbi-report-planning`, and `powerbi-dashboard-architect`
treat any skill named `company-powerbi-standards` as an optional, top-priority
override. They never hardcode a company's colors, fonts, or file names — they
only rely on this skill existing (or not) and answering the questions below.
Keep answering these questions in whatever form you like; nothing downstream
parses this file's exact prose structure.

| Consumer asks | Answered by |
|---|---|
| "Is a company standards skill installed at all?" | Presence of a skill literally named `company-powerbi-standards` — do not rename the skill unless you also update the three consumer skills that reference it by name. |
| "Which theme file governs this page's archetype?" | `tokens.json` → `themeSelection.<executive\|operational>.file` + `.archetypes` |
| "Is this theme file complete and safe to use as-is (no re-merge with `assets/base.json`)?" | Yes, by convention — every theme file this skill ships must carry its own `$schema` and full `visualStyles` safeguards. |
| "What callout font size must a KPI card use?" | `tokens.json` → `themeSelection.<key>.calloutPt` |
| "What prefix do new measures get?" | `tokens.json` → `naming.measurePrefix` |
| "How many major visuals may a page hold?" | `tokens.json` → `layout.maxMajorVisualsPerPage` |
| "Do executive KPI cards drill through by default?" | `tokens.json` → `interaction.executiveKpiDefaultsToDrillthrough` |
| "What format must the delivered report use?" | `tokens.json` → `delivery.format` / `delivery.requiredParts` |

## Rules for editing this skill

- Literal hex/font/size values live **only** in `tokens.json`. `SKILL.md` refers
  to token keys (`colors.primary`), never restates the hex. This is what keeps
  a rebrand a one-file edit instead of a hunt across prose and JSON.
- If you change a color, font, or callout size in `tokens.json`, regenerate the
  matching theme JSON file(s) so they stay in sync — see the field mapping
  below. Nothing enforces this automatically; a drift between `tokens.json`
  and the shipped theme JSON is the exact bug this restructuring exists to
  prevent, so check it by hand after every edit.
- Do not restate generic design theory here (WCAG contrast math, palette
  category-count theory, typography scale rationale). That lives in
  `powerbi-report-design/references/accessibility.md`, `color.md`, and
  `typography.md`. This skill only states this company's specific choices and
  any deviation from the generic default.

## `tokens.json` → theme JSON field mapping

| `tokens.json` path | Theme JSON field |
|---|---|
| `colors.primary.hex` | `dataColors[0]`, `bad` |
| `colors.secondaryAccessible.hex` | `dataColors[1]`, `good` |
| `colors.neutral.hex` | `dataColors[2]`, `neutral` |
| `colors.background` | `background` |
| `colors.foreground.hex` | `foreground`, `textClasses.*.color` |
| `fonts.primary` | `textClasses.*.fontFace` |
| `themeSelection.<key>.calloutPt` | `textClasses.callout.fontSize` |
