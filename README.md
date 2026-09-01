# msg Skills for Fabric

This repository is **msg's fork** of Microsoft's
[skills-for-fabric](https://github.com/microsoft/skills-for-fabric) —
reusable AI assistant instructions that help GitHub Copilot CLI, Claude Code,
and compatible AI coding tools work with Microsoft Fabric.

> **Upstream:** All Fabric workload skills (Lakehouse, Warehouse, Eventhouse,
> Dataflows, semantic models, PBIP authoring, migrations, etc.) originate from
> [microsoft/skills-for-fabric](https://github.com/microsoft/skills-for-fabric)
> and remain under Microsoft's ownership and MIT license. This fork is not
> published by, affiliated with, or endorsed by Microsoft.
>
> **What msg added:** this fork narrows the root-level `skills/` folder to
> the Power BI workflow (report planning, design, authoring, management, and
> semantic models) and adds msg's own corporate design-standards skill —
> `company-powerbi-standards` — plus a customizable, customer-distributable
> version of it (`plugins/msg-powerbi-standards`). Everything else from
> upstream still ships inside `plugins/` for anyone who wants the full
> multi-workload bundle.

## Repository structure

```
skills/                          # Root-level skills — auto-loaded when this repo is
                                  # cloned/opened directly (see CLAUDE.md, AGENTS.md, etc.)
  check-updates/                 # Shared update-check skill used by the others
  semantic-model-authoring/      # DAX, TMDL, semantic model authoring
  powerbi-report-planning/       # Guided requirements -> build workflow
  powerbi-report-design/         # Visual design guidance (tone, archetype, layout, color)
  powerbi-report-authoring/      # PBIR/PBIP file mechanics
  powerbi-report-management/     # Fabric report item CRUD (publish, update)

plugins/                         # Marketplace-installable bundles
  fabric-skills/                 # Full upstream bundle: every Fabric workload
  fabric-authoring/              # Upstream: APIs, automation, notebooks, ingestion
  fabric-consumption/            # Upstream: read-only querying and exploration
  fabric-operations/             # Upstream: performance/health diagnostics
  powerbi-authoring/             # Upstream: Power BI semantic models + PBIP workflows
  msg-powerbi-standards/         # msg's own plugin — see "msg Power BI Standards" below

common/                          # Shared reference docs used across CLI-style skills
mcp-setup/                       # MCP server registration guidance
prompt_examples/                 # Example prompts to try after installing a bundle
CLAUDE.md, AGENTS.md,
.cursorrules, .windsurfrules,    # Root-level instructions auto-picked up by each tool
GEMINI.md
```

The distinction that matters: **`skills/`** is what you get for free the
moment you clone this repo into a project — it is deliberately scoped to
Power BI plus the msg standards skill. **`plugins/`** is what you install
through a plugin marketplace, and still mirrors Microsoft's full catalog
alongside msg's addition.

## Using this repo directly

If you clone this repository (or copy `skills/` into your own project), the
Power BI skillset and msg's corporate standards are picked up automatically
by any tool that reads `CLAUDE.md` (Claude Code), `AGENTS.md` (Codex / Jules /
OpenCode), `.cursorrules` (Cursor), `.windsurfrules` (Windsurf), or
`GEMINI.md` (Gemini CLI) — no install step required. Just open the project
and ask for a Power BI task:

```text
Build me an executive dashboard from this semantic model, using our corporate design standards.
```

## Installing via plugin marketplace (GitHub Copilot CLI)

The upstream bundles are still installable exactly as Microsoft ships them.
Add the public marketplace:

```bash
/plugin marketplace add microsoft/skills-for-fabric
```

Install the main Fabric bundle, or a focused one:

```bash
# Everything
/plugin install fabric-skills@fabric-collection

# Authoring: APIs, automation, notebooks, schemas, ingestion, and deployment
/plugin install fabric-authoring@fabric-collection

# Consumption: interactive querying, discovery, exploration, and monitoring
/plugin install fabric-consumption@fabric-collection

# Operations: diagnostics and performance investigation
/plugin install fabric-operations@fabric-collection

# Power BI authoring: semantic models, Power BI report skills, and PBIP workflows
/plugin install powerbi-authoring@fabric-collection
```

Copilot CLI installs plugins as complete bundles. To limit installed skills,
choose a focused bundle instead of filtering the full bundle.

> The persona bundles `fabric-authoring`, `fabric-consumption` and `fabric-operations` are retired. Every skill they carried ships in `fabric-skills`. The three ids still resolve as deprecated aliases of `fabric-skills`, so an existing install keeps working through `/plugin update`; new installs should use `fabric-skills`.

### Update installed plugins

```bash
/plugin update fabric-skills@fabric-collection
```

Replace `fabric-skills` with the focused bundle name to update that bundle.
From a terminal, update every installed plugin with:

```bash
copilot plugin update --all
```

### Automatic update checking

Installed Fabric bundles include a non-blocking `check-updates` skill. The
first Fabric skill invoked in a session detects the marketplace plugin, direct
plugin, or positively identified skills-for-fabric Git clone that supplied it.
When a network check is due, it reads the version and changelog from the same
repository `main` ref and shows update guidance verified for the current agent
host without executing it. Automatic checks run at most once every seven UTC
days per installation; an explicit check bypasses that cache.

```bash
/powerbi-authoring:check-updates
```

## msg Power BI Standards

`company-powerbi-standards` is the skill that makes every Power BI report
generated in this repo follow msg's brand — colors, fonts, theme selection,
layout density, KPI color coding, and delivery format. `powerbi-report-design`
and `powerbi-dashboard-architect` look for a skill with exactly this name and
treat it as the top-priority design authority whenever it's installed;
without it, they fall back to generic design defaults.

- **msg's own use** — already active. It lives at `skills/company-powerbi-standards/`
  and is picked up automatically by this repo (see "Using this repo directly"
  above). Its brand values live in `tokens.json`, not scattered across prose —
  see `skills/company-powerbi-standards/references/contract.md` if you're
  changing it.
- **Customers / other organizations** — use `plugins/msg-powerbi-standards/`
  instead. It ships a blank, brand-neutral template (`skills/company-powerbi-standards/`
  inside the plugin) plus msg's own filled-in version as a drop-in reference
  (`examples/msg/`). See that plugin's `README.md` for the exact customization
  steps.

  It's already set up as its **own marketplace**, separate from Microsoft's —
  `msg-collection`, not `fabric-collection` — so installing it never implies
  installing Microsoft's bundles too:

  ```bash
  /plugin marketplace add <msg-org>/<msg-repo>
  /plugin install msg-powerbi-standards@msg-collection
  ```

  This only works once `plugins/msg-powerbi-standards/` is published as its
  own repository (its manifests are self-contained and need no path changes
  to do so) — the `repository` field in its `plugin.json`/`marketplace.json`
  is still a placeholder pending that decision. Until then, install it
  manually: copy `plugins/msg-powerbi-standards/skills/company-powerbi-standards/`
  into your project's skills folder alongside Microsoft's `powerbi-authoring`
  bundle.

## What is included

| Bundle / folder | Use it for |
|--------|------------|
| `fabric-skills` | Complete Microsoft Fabric skill bundle: authoring, consumption, operations, migration, and end-to-end architecture skills. |
| `fabric-authoring` | Creating and managing Fabric items through REST APIs, CLI automation, notebooks, T-SQL, KQL, Dataflows Gen2, Eventstreams, and semantic models. |
| `fabric-consumption` | Read-only exploration and query workflows across Warehouses, Lakehouses, Power BI semantic models, Eventhouse/KQL databases, Eventstreams, Dataflows Gen2, and catalog search. |
| `fabric-operations` | Performance and health diagnostics, including warehouse query insights and slow-query investigation. |
| `powerbi-authoring` | Authoring Power BI semantic models, reports, and PBIP workflows, including report planning, design, authoring, and management. |
| `msg-powerbi-standards` | msg's corporate Power BI design-standards skill — a customizable template plus msg's own worked example. |

See [CHANGELOG.md](CHANGELOG.md) for upstream release notes.

## Try an example prompt

- [Analytics PDF report](prompt_examples/NYC_AnalyzeExistingDataCreatePDF.txt)
- [Document my workspace](prompt_examples/DocumentMyWorkspace.txt)
- [NYC Taxi medallion architecture](prompt_examples/NYCTaxi_MedallionArchitecture.txt)
- [Dashboard app](prompt_examples/DashboardApp.txt)

## Authentication

Most Fabric operations require Azure authentication. Start with:

```bash
az login
az account get-access-token --resource https://api.fabric.microsoft.com
```

SQL, Spark, Power BI, and KQL workflows may require workload-specific
endpoints or token audiences. The installed skills provide the detailed
commands and API patterns for each workload.

## MCP servers

Skills provide guidance and patterns. MCP servers provide live tool access to
data sources and APIs. Some bundles include MCP configuration where
supported, and you can register additional Fabric MCP servers if your
environment provides them.

See [MCP setup](mcp-setup/README.md).

## Other AI coding tools

GitHub Copilot CLI plugin installation is the recommended path for the
upstream bundles. This repository also includes root-level configuration
files for compatible AI coding tools — [CLAUDE.md](CLAUDE.md) for Claude
Code, [.cursorrules](.cursorrules) for Cursor, [.windsurfrules](.windsurfrules)
for Windsurf, and [AGENTS.md](AGENTS.md) for Codex / Jules / OpenCode. They
are picked up automatically when the repo is cloned.

Gemini CLI also auto-discovers [GEMINI.md](GEMINI.md) when the repo is cloned.

## Issues and security

For issues with the upstream Fabric skills, use Microsoft's
[GitHub issue tracker](https://github.com/microsoft/skills-for-fabric/issues).
For issues with msg's additions (`company-powerbi-standards`,
`msg-powerbi-standards`), open an issue against this fork.

For security vulnerabilities, do not open a public issue. See
[SECURITY.md](SECURITY.md) for the private reporting path.

## License

This project is licensed under the [MIT License](LICENSE), same as upstream.
