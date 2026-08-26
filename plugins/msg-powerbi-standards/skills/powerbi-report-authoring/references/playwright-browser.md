# Playwright Browser Verification (Fabric Service)

> Read this when Power BI Desktop is not available (macOS, Linux, or any
> environment without the Desktop Bridge CLI) and you need to visually verify
> a PBIR report by publishing it to Fabric and screenshotting the rendered
> Service page with Playwright. This is the non-Desktop equivalent of
> `powerbi-desktop.md`. Once screenshots exist in `screenshots/`, review them
> with `screenshot-review.md` exactly as you would Desktop-sourced captures —
> that checklist does not change based on screenshot source.

## Core Rule

Report Service rendering is authoritative for visual verification when
Desktop is unavailable, but it requires a publish round-trip. Do not
screenshot after every micro-edit — batch a logical set of PBIR changes,
then run the full loop once:

1. Edit PBIR files.
2. Run `powerbi-report-author validate "<path-to-.Report-dir>"`.
3. Publish to the target Fabric workspace (`powerbi-report-management` skill —
   [Publishing a local .pbip](../../powerbi-report-management/SKILL.md) or
   [Modifying an existing report in Fabric](../../powerbi-report-management/SKILL.md)
   workflow, whichever applies).
4. Resolve the report's `webUrl` from the Fabric Items API response (do not
   hand-construct an `app.powerbi.com` URL — the item metadata already
   returns the correct browser link).
5. Open that URL with the Playwright MCP browser, confirm it is a signed-in
   report render (not a login page — see **Session check**, below).
6. Iterate report pages, waiting for each page's visuals to finish rendering
   before capturing.
7. Save one screenshot per page to `screenshots/`, using the same naming
   convention `screenshot-review.md` expects.
8. Review screenshots against `screenshot-review.md`. If anything is wrong,
   fix PBIR and restart at step 1 for that page.

## Setup

Playwright MCP must be configured with a **persistent browser profile** so
the Microsoft Entra sign-in (often MFA) only has to happen once by hand, not
on every agent run:

```bash
npx @playwright/mcp@latest --user-data-dir ~/.playwright-powerbi-profile
```

The first time you use this profile, open the report URL manually in that
session and complete sign-in. Every subsequent agent-driven run reuses the
same profile's cookies.

## Resolve the report URL

After publish (or when re-verifying an already-published report), get the
item's `webUrl` rather than constructing one:

```bash
az rest --method get \
  --url "https://api.fabric.microsoft.com/v1/workspaces/<workspaceId>/items/<reportId>" \
  --resource https://api.fabric.microsoft.com \
  --headers "x-ms-fabric-skill=powerbi-report-authoring" \
  | jq -r '.properties.webUrl // .webUrl'
```

Confirm the returned URL resolves to a report (not a dataset or dashboard)
before navigating.

## Session check

Before treating any screenshot as a real report render, verify the page
is not a Microsoft login form. A login page and an empty/loading report
canvas can look superficially similar in a raw wait-for-network-idle check,
so check for report-specific chrome (page tab strip, visual containers) or
the absence of a Microsoft sign-in form element, not just "page loaded."

If the session has expired:

- Re-open the report URL manually in the persistent profile to re-authenticate.
- Do not attempt to script the Entra login flow — MFA breaks any scripted
  credential entry, and treating a login screen as a report state produces
  a false "blank page" or "error icon" finding in the checklist below.

## Page iteration and rendering wait

Power BI Service renders one report page at a time and lazy-loads visuals
inside it. For each page:

1. Click the page's tab in the page navigator.
2. Wait for network idle.
3. Wait for visual containers to be present and for chart canvases/SVGs
   inside them to be non-empty — a network-idle event alone does not mean
   visuals have finished drawing.
4. Add a short fixed buffer after the above (chart animation/draw-in can
   continue briefly after the container appears).
5. Capture the screenshot.

If a visual still shows as an empty frame after this wait sequence, do not
assume it is a real "no data" bug on the first pass — retry the wait once.
Only treat it as a genuine issue (per `screenshot-review.md`'s "Chart frame
with no data" row) if it is still empty on retry.

## Screenshots

> **Capture scope:** Match Desktop CLI behavior — capture the report page
> **and** the right-hand filter pane (`outspacePane`) when the filter pane
> is enabled and expanded, so `screenshot-review.md`'s filter-pane checks
> apply identically regardless of capture source.

Save with the same naming convention the Desktop CLI's
`screenshot-all --output-dir screenshots` would have produced, so
`screenshot-review.md` and any other tooling that reads `screenshots/`
does not need to know which capture method produced the files:

```
screenshots/<page-id>.png
```

Use the PBIR page ID (e.g. `ReportSection1a2b3c`), not the display name shown
in the Service page tab, for the filename — the same rule Desktop screenshots
follow.

## After capture

Proceed directly to `screenshot-review.md`. Its checklist, common-problems
table, and interactive "does this look right?" step with the user apply
unchanged — the review process does not know or care that the source was
Playwright against Fabric Service rather than the Desktop Bridge CLI.

## Common problems specific to this path

| Symptom | Likely cause | Fix |
|---|---|---|
| Screenshot shows a Microsoft sign-in form | Persistent profile session expired | Re-authenticate manually in the same profile; do not script MFA. |
| All visuals still empty after retrying the wait | Publish had not actually finished (async git sync / LRO still running) | Confirm the publish operation reached terminal success before navigating, not just that the API call returned. |
| Screenshot looks stale / shows the previous version of the report | Browser cached the report page from an earlier session | Hard-reload (bypass cache) before capturing, or open the URL in a fresh tab. |
| Theme/formatting changes not reflected | Publish succeeded but targeted the wrong report item, or an old `webUrl` was reused from a prior run | Re-resolve `webUrl` from the Items API after every publish rather than caching it across sessions. |
| Report renders correctly but layout differs slightly from expected Desktop appearance | Minor Service vs. Desktop rendering differences exist for some visual types/fonts | Note the discrepancy to the user rather than treating it as a PBIR authoring bug; only re-author if the difference is a real defect, not a rendering-surface quirk. |