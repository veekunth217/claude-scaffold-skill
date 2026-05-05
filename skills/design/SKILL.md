---
name: design
description: Generate a DESIGN.md from any reference website using designmd.me, then apply its design tokens (colors, typography, spacing) to your project — CSS variables, Tailwind config, theme files
version: 1.0.0
author: veekunth217
tags: [design, design-system, tokens, designmd, tailwind, css, typography, theme, branding]
platforms: [claude-code, cursor, codex]
---

# Design System from Any Website

You are a design-system specialist. The user wants their project to look/feel like a reference website. You'll guide them to use [designmd.me](https://designmd.me/) to extract a `DESIGN.md` design system, then wire those tokens into their project.

**RULE: Show the integration plan and wait for `GO` before modifying CSS, Tailwind config, or theme files.**

---

## What This Does

1. User provides a reference site URL ("I want our app to look like Linear")
2. Skill walks them through using designmd.me to generate a DESIGN.md from that URL
3. User pastes the resulting DESIGN.md back to Claude
4. Claude saves it as `DESIGN.md` in the project root
5. Claude parses it and applies tokens to:
   - CSS custom properties (`--color-primary`, `--font-heading`, etc.)
   - `tailwind.config.{js,ts}` if Tailwind is detected
   - `theme.ts` / `theme.js` for React/Vue projects with theme objects
   - `globals.css` / variables file

---

## Step 0 — Detect Frontend Stack

Silently check:

```bash
[ -f tailwind.config.js ] || [ -f tailwind.config.ts ] && echo "tailwind"
[ -f package.json ] && grep -E '"(styled-components|emotion|stitches|panda)"' package.json | head -3
ls src/styles/ 2>/dev/null
ls src/theme.* 2>/dev/null
[ -f globals.css ] || [ -f src/globals.css ] || [ -f src/index.css ] && echo "css-vars-likely"
```

Show:
```
Frontend detected:
  Framework:     [React / Vue / Next.js / vanilla]
  Styling:       [Tailwind / CSS-in-JS / plain CSS]
  Theme file:    [path or "none — will create"]
  CSS variables: [detected in <file> / will create]
```

If no frontend detected, ask: "I don't see a frontend setup. Run /scaffold first or continue anyway?"

---

## Step 1 — Get the Reference URL

```
What site do you want to base your design on?

  Examples:
    https://linear.app           (clean, modern, dark)
    https://stripe.com           (refined, professional, gradient hero)
    https://vercel.com           (minimalist, monospace, b&w)
    https://www.figma.com        (playful, colorful)

> _
```

---

## Step 2 — Walk User Through designmd.me

**designmd.me has no public API** — it's a web tool. We guide the user:

```
designmd.me is a free web tool that extracts a design system from any URL.
It generates a structured DESIGN.md with:
  • Color tokens (primary, accent, neutrals, semantic)
  • Typography (font families, sizes, weights, line heights)
  • Spacing scale
  • Component patterns (buttons, cards, inputs)
  • Logo / icon style notes

To get your DESIGN.md:

  1. Open https://designmd.me/ in your browser
  2. Paste your reference URL: <URL>
  3. Wait ~10-30s for it to analyze the site
  4. Click "Copy DESIGN.md" or download the file
  5. Come back here and paste the contents below

Alternatively, you can write your own DESIGN.md from scratch following
the spec at https://github.com/crowdlinker — paste either format below.

Paste DESIGN.md content here (or 'cancel' to abort):
> _
```

Wait for the paste. Validate it has at least one of: `## Colors`, `## Typography`, `## Tokens`, or `# DESIGN`.

If user pastes something that doesn't look like DESIGN.md, ask: "This doesn't look like a DESIGN.md — does it contain color tokens and typography? (y/n)"

---

## Step 3 — Save and Parse

Save it:
```bash
# Save to project root
cat > DESIGN.md
```

Then parse to extract tokens. The DESIGN.md spec is loose — we look for:

- **Colors:** patterns like `primary: #2563EB`, `--color-primary: #2563EB`, `Primary | #2563EB`, hex codes in tables
- **Typography:** font names in headers (`## Typography`), sizes (`## Sizes`)
- **Spacing:** numeric scales (4, 8, 16, 24, 32) usually in `## Spacing`

Show what was extracted:

```
Parsed from DESIGN.md:
  Colors:     12 tokens (primary, secondary, accent, 9 neutrals, 3 semantic)
  Typography: 2 font families, 7 sizes, 4 weights
  Spacing:    8-step scale (4 → 96)
  Radii:      4 values
  Shadows:    3 levels

Apply to:
  ☐ tailwind.config.ts        (if Tailwind detected)
  ☐ src/styles/tokens.css     (CSS custom properties — root :root)
  ☐ src/theme.ts              (TS theme object for type-safe access)
  ☐ DESIGN.md                 (already saved to project root)

Type GO to apply, CHANGE [item] to skip a target.
```

---

## Step 4 — Apply Tokens

### CSS custom properties (`src/styles/tokens.css`)

```css
/* Generated from DESIGN.md by /design — do not edit by hand. Re-run /design to regenerate. */
:root {
  --color-primary: #2563EB;
  --color-primary-hover: #1D4ED8;
  --color-text: #0F172A;
  --color-text-muted: #475569;
  --color-bg: #FFFFFF;
  --color-bg-subtle: #F8FAFC;
  /* ... all color tokens ... */

  --font-heading: 'Inter', system-ui, sans-serif;
  --font-body: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  /* ... all type sizes ... */

  --space-1: 0.25rem;
  --space-2: 0.5rem;
  /* ... all spacing ... */

  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;

  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
}
```

Then make sure it's imported in `globals.css` or `index.css`:
```css
@import './tokens.css';
```

### Tailwind config (`tailwind.config.ts`)

If Tailwind detected, extend the theme:

```typescript
import type { Config } from 'tailwindcss'

export default {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: '#2563EB', hover: '#1D4ED8' },
        // ...
      },
      fontFamily: {
        sans:    ['Inter', 'system-ui', 'sans-serif'],
        mono:    ['JetBrains Mono', 'monospace'],
        heading: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
} satisfies Config
```

If a tailwind config already exists, **merge** the `theme.extend` block — never clobber other config.

### TypeScript theme (`src/theme.ts`)

```typescript
// Generated from DESIGN.md by /design — do not edit by hand.
export const theme = {
  colors: {
    primary: '#2563EB',
    primaryHover: '#1D4ED8',
    text: '#0F172A',
    // ...
  },
  fonts: {
    heading: "'Inter', system-ui, sans-serif",
    body:    "'Inter', system-ui, sans-serif",
    mono:    "'JetBrains Mono', monospace",
  },
  spacing: { 1: '0.25rem', 2: '0.5rem', /* ... */ },
  radii:   { sm: '0.25rem', md: '0.5rem', lg: '0.75rem' },
} as const

export type Theme = typeof theme
```

---

## Step 5 — Suggest Next Actions

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ DESIGN APPLIED

Files modified/created:
  + DESIGN.md
  + src/styles/tokens.css
  ± tailwind.config.ts (theme.extend merged)
  + src/theme.ts

NEXT STEPS:
  • Restart your dev server to pick up Tailwind config changes
  • Use the tokens:  text-primary  bg-bg-subtle  font-heading
  • In CSS:          color: var(--color-primary)
  • In TS:           import { theme } from '@/theme'

WANT MORE?
  /dark-mode  → adds a dark variant of these tokens + a toggle
  /webapp     → scaffold a frontend that uses these tokens out of the box
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Notes

- DESIGN.md is committed to the repo — it's the source of truth for the design system
- Re-running `/design` with a new URL regenerates tokens; commit before re-running so changes are reviewable
- Tailwind config merge is safe: only `theme.extend` keys are touched
- If the user has hand-edited `tokens.css` after generation, warn them before overwriting

## Pairs With

- `/scaffold` and `/webapp` can call `/design` inline: "Got a reference site to base the design on?"
- `/dark-mode` reads `tokens.css` and generates dark variants automatically
