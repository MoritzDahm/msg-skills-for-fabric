# Contrast Checklist — Validating Your Own Colors

Run every color you're about to put in `tokens.json` through this before
committing it. This is what separates `secondaryAccessible` (text-safe) from
`secondaryDecorative` (decorative-only) in the placeholder tokens — the two
colors can come from the same brand book; only the contrast math decides which
bucket a color belongs in.

## WCAG AA thresholds

| Use | Minimum contrast vs. its background |
|---|---|
| Normal text, data labels, axis labels | 4.5 : 1 |
| Large text (≥18pt, or ≥14pt bold), KPI callout numbers | 3 : 1 |
| Graphical objects and UI components (icons, chart marks meant to be read as data, `good`/`bad` indicators) | 3 : 1 |
| Decorative fills with no informational content | No requirement |

## How to compute contrast ratio

Relative luminance of a color (`R`, `G`, `B` each 0–255, normalized to 0–1):

```text
for each channel c in {R, G, B}:
  c_srgb = c / 255
  c_lin  = c_srgb / 12.92                              if c_srgb <= 0.03928
         = ((c_srgb + 0.055) / 1.055) ^ 2.4             otherwise

L = 0.2126 * R_lin + 0.7152 * G_lin + 0.0722 * B_lin
```

Contrast ratio between two colors (`L1` = lighter, `L2` = darker):

```text
contrast = (L1 + 0.05) / (L2 + 0.05)
```

Any tool that implements this formula works — a script, a browser devtools
contrast checker, or an online WCAG contrast calculator. Record the resulting
ratio directly in `tokens.json` (`contrastOnWhite`) so the next person doesn't
have to recompute it.

## Decision rule for each brand color

1. Compute contrast against `colors.background` (usually white).
2. ≥4.5:1 → safe for text/data labels → candidate for `secondaryAccessible`,
   `primary`, `neutral`, or `foreground`.
3. ≥3:1 but <4.5:1 → safe for large text and graphical marks only, not body
   text or data labels.
4. <3:1 → decorative only (`secondaryDecorative`-style) — large fills and
   backgrounds where no contrast requirement applies. Set `wcagAA_text: false`
   and `wcagAA_graphics: false` explicitly in `tokens.json` so downstream
   skills know never to use it for a `good:`/`bad:` theme slot, text, or a
   data-bearing chart series.

## Additional checks

- **Color vision deficiency (CVD):** two colors that are distinguishable to
  full-color vision can collapse into the same perceived color under
  protanopia/deuteranopia. If your `good`/`bad` pair both sit in the
  red-green range, verify with a CVD simulator and consider pairing with an
  icon or label rather than color alone.
- **`good` vs `bad` parity:** compute contrast for both and keep them within
  roughly the same range. If `good` is 4.8:1 and `bad` is 7.9:1, the bad-news
  color will visually dominate the good-news color purely from contrast
  strength — that reads as bias even if neither individually fails AA.
