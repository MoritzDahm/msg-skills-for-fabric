# Third-Party Notices

This plugin bundles substantial content from
[microsoft/skills-for-fabric](https://github.com/microsoft/skills-for-fabric),
used here under its MIT license. This plugin is an independent redistribution
by msg — it is not published by, affiliated with, or endorsed by Microsoft.

## Vendored from microsoft/skills-for-fabric (MIT License)

- `skills/check-updates/`
- `skills/semantic-model-authoring/`
- `skills/powerbi-report-planning/`
- `skills/powerbi-report-design/`
- `skills/powerbi-report-authoring/`
- `skills/powerbi-report-management/`

These are carried over with msg-specific fixes applied upstream in msg's fork
(for example, `powerbi-report-design`'s theme-selection step was generalized
to not hardcode msg's theme file names — see that skill's own history for
details).

## Original by msg

- `skills/powerbi-dashboard-architect/` — msg's governance layer (measure
  naming, workload restrictions, corporate design gate).
- `skills/company-powerbi-standards/` — msg's corporate Power BI design
  standards (this plugin's default brand).
- `template/company-powerbi-standards/` — the blank, brand-neutral version of
  the above for organizations that want to substitute their own brand.

## Upstream license

```
MIT License

Copyright (c) 2026 Microsoft Corporation

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

msg's own additions (`powerbi-dashboard-architect`, `company-powerbi-standards`,
`template/`) are licensed MIT as well — see this plugin's `plugin.json`.
