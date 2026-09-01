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
> semantic models) and adds msg's own governance skill — `powerbi-governance`
> — covering change-control (CR tracking, a local change ledger) and
> measure-naming/approval-gate rules, plus a customizable,
> customer-distributable version of the whole set
> (`plugins/msg-powerbi-standards`). Corporate color/theme/layout authority
> stays inside `powerbi-report-design` itself. Everything else from upstream
> still ships inside `plugins/` for anyone who wants the full multi-workload
> bundle.

## Repository structure

```
skills/                          # Root-level skills — auto-loaded when this repo is
                                  # cloned/opened directly (see CLAUDE.md, AGENTS.md, etc.)
  check-updates/                 # Shared update-check skill used by the others
  powerbi-governance/            # CR tracking, change ledger, measure-naming + approval-gate rules
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
Power BI plus msg's governance skill. **`plugins/`** is what you install
through a plugin marketplace, and still mirrors Microsoft's full catalog
alongside msg's addition.

## Using this repo directly

If you clone this repository (or copy `skills/` into your own project), the
Power BI skillset is picked up automatically by any tool that reads
`CLAUDE.md` (Claude Code), `AGENTS.md` (Codex / Jules / OpenCode),
`.cursorrules` (Cursor), `.windsurfrules` (Windsurf), or `GEMINI.md` (Gemini
CLI) — no install step required. `powerbi-governance`'s change-control and
measure-naming rules apply automatically wherever `powerbi-report-planning`,
`powerbi-report-design`, `semantic-model-authoring`, or
`powerbi-report-management` invoke it — it has no triggers of its own. Just
open the project and ask for a Power BI task:

```text
Build me an executive dashboard from this semantic model.
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

## msg Power BI Governance

`powerbi-governance` is the skill that gives every Power BI change made in
this repo a DevOps-style paper trail: it resolves a change-request (CR)
reference for each change (from an external ticket, a chat ask, or an
implicit revision of already-approved work), reads a local change-log
ledger for prior history on the target workspace/model/report before new
work starts — proactively surfacing anything previously reverted or
blocked — and enforces msg's measure-naming and approval-gate rules.
All of that is configurable in one place — `skills/powerbi-governance/settings.md`
— including the ledger path, the CR id format, and the measure-naming
prefix (`m_` by default); nothing else needs editing to change them.
`powerbi-report-planning`, `powerbi-report-design`,
`semantic-model-authoring`, and `powerbi-report-management` invoke it
deterministically at specific steps; it has no build/design/publish
triggers of its own, so it never competes with those skills for the same
request. Corporate color/theme/layout
authority is **not** part of this skill — that stays entirely inside
`powerbi-report-design`.

- **msg's own use** — already active. It lives at `skills/powerbi-governance/`
  and is picked up automatically by this repo (see "Using this repo directly"
  above). To customize it, edit `skills/powerbi-governance/settings.md` —
  see `references/ledger-schema.md` and `references/cr-intake.md` for the
  exact ledger format and CR-intake logic those settings feed into.
- **Customers / other organizations** — use `plugins/msg-powerbi-standards/`
  instead, which bundles `powerbi-governance` alongside the rest of the
  Power BI authoring skills.

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
  manually: copy `plugins/msg-powerbi-standards/skills/powerbi-governance/`
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
| `msg-powerbi-standards` | msg's Power BI toolkit: the upstream authoring skills plus `powerbi-governance` for change-control (CR tracking, change ledger) and measure-naming rules. |

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
For issues with msg's additions (`powerbi-governance`,
`msg-powerbi-standards`), open an issue against this fork.

For security vulnerabilities, do not open a public issue. See
[SECURITY.md](SECURITY.md) for the private reporting path.

## License

This project is licensed under the [MIT License](LICENSE), same as upstream.
