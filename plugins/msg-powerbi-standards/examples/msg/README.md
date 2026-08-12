# Example: msg's own brand, as a drop-in

This folder is msg's real Power BI design system, packaged in the exact shape
the plugin's skill expects. Two ways to use it:

## Option A — Use it as-is

Copy these three files over the blank template:

```bash
cp examples/msg/SKILL.md               skills/company-powerbi-standards/SKILL.md
cp examples/msg/tokens.json             skills/company-powerbi-standards/tokens.json
cp examples/msg/themes/theme-executive.json    skills/company-powerbi-standards/themes/theme-executive.json
cp examples/msg/themes/theme-operational.json  skills/company-powerbi-standards/themes/theme-operational.json
```

Every downstream Power BI skill in the `powerbi-authoring` plugin now applies
msg's brand automatically.

## Option B — Use it as a reference while building your own

Keep the blank template in `skills/company-powerbi-standards/` and read this
folder side by side while you fill in your own `tokens.json` — every section
of `SKILL.md` here shows a real, filled-in example of what the placeholder
version asks for (a real hex code with a real measured contrast ratio, a real
theme-selection mapping, a real palette overflow policy, etc.).

Do not literally keep msg's colors in your own report unless you are actually
building for msg — this is a worked example of the *mechanism*, not a brand
you're licensed to reuse.
