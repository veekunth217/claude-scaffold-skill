---
name: dark-mode
description: Add dark mode to any frontend project — generates dark variants of CSS tokens, a smooth animated toggle (MJ Black or White tribute), supports system preference, invert mode, and PDF read mode
version: 1.0.0
author: veekunth217
tags: [dark-mode, theme, toggle, css-variables, tailwind, accessibility, ui, animation]
platforms: [claude-code, cursor, codex]
---

# Dark Mode + Black or White Toggle

You are a dark-mode specialist. Add a polished dark mode to any frontend project — with the **Black or White** toggle: a smooth color-morphing animation paying tribute to the Michael Jackson video, designed to be visually striking and screenshot-worthy.

**RULE: Show full plan and wait for `GO` before modifying CSS, components, or theme files.**

---

## What This Does

Three modes, one toggle:

```
☀️  Light    → your default theme
🌑  Dark     → inverted brightness, preserves brand colors
🪞  Invert   → pure inversion (a11y mode)
📖  Read     → sepia/low-contrast (PDF-style for long-form)
```

Plus the **"Black or White" toggle** — a smooth morph animation with a subtle face-silhouette CSS effect. Star bait.

---

## Step 0 — Detect Stack

```bash
# Frontend framework
[ -f package.json ] && grep -E '"(react|vue|svelte|astro)"' package.json | head -3

# Existing theme
[ -f src/styles/tokens.css ] && echo "tokens-exists"
[ -f tailwind.config.ts ] || [ -f tailwind.config.js ] && echo "tailwind"
[ -f src/theme.ts ] && echo "ts-theme"

# Existing dark mode (don't overwrite)
grep -lE 'prefers-color-scheme|\.dark\s*{|data-theme=' src/**/*.{css,tsx,vue} 2>/dev/null | head -3
```

Show:
```
Stack:        [React / Vue / Svelte / vanilla]
Tokens:       [src/styles/tokens.css / generate new]
Tailwind:     [yes — darkMode setting / no]
Existing dark: [found in <files> / none]
```

If existing dark mode found, ask: "Augment what's there or replace it?"

---

## Step 1 — Pick Your Toggle Style

```
Pick a toggle style:

  1. Classic switch     — sun/moon icons, simple slide
  2. Black or White ⭐   — MJ tribute, smooth color-morph animation
                          (recommended — looks great in screenshots)
  3. Three-state        — Light / Dark / System
  4. Five-state         — Light / Dark / Invert / Read / System
```

---

## Step 2 — Pick Modes to Include

```
Which modes do you want?

  ✓ Light + Dark         (always — the basics)
  [ ] Invert mode        (true color inversion — accessibility)
  [ ] Read mode          (sepia/low-contrast — for blog/docs sites)
  [ ] System preference  (respects OS setting via prefers-color-scheme)

> _
```

---

## Step 3 — Show Plan

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DARK MODE PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Toggle:   Black or White (MJ tribute) — smooth color-morph
Modes:    Light, Dark, System
Storage:  localStorage (persists user choice)

FILES TO CREATE / MODIFY:
  + src/styles/tokens-dark.css        (dark variants of all tokens)
  + src/styles/dark-mode.css          (transitions + toggle styles)
  + src/components/ThemeToggle/<files> (the toggle component)
  + src/hooks/useTheme.ts             (state + system pref + storage)
  ± src/styles/tokens.css             (adds [data-theme="dark"] selector)
  ± src/main.tsx / src/App.tsx        (provider wired in)
  ± tailwind.config.ts                (darkMode: 'class' if Tailwind)
  ± index.html                        (early <script> to avoid flash of light)

NOTHING runs until you type GO.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 4 — Generate Dark Variants

If `tokens.css` already exists, generate `tokens-dark.css` by inverting brightness while preserving hue:

**Heuristic:**
- `--color-bg: #FFFFFF` → `#0A0A0A` (near-black, not pure)
- `--color-bg-subtle: #F8FAFC` → `#1A1A1F`
- `--color-text: #0F172A` → `#F1F5F9`
- `--color-text-muted: #475569` → `#94A3B8`
- `--color-primary: #2563EB` → `#3B82F6` (slightly brighter for contrast)
- Shadows lose opacity in dark mode (or use white-shadow for "glow")

Result:

```css
/* tokens-dark.css */
[data-theme="dark"] {
  --color-bg:        #0A0A0A;
  --color-bg-subtle: #1A1A1F;
  --color-text:      #F1F5F9;
  --color-text-muted:#94A3B8;
  --color-primary:   #3B82F6;
  --color-border:    #2A2A2F;
  --shadow-sm:       0 1px 2px 0 rgb(0 0 0 / 0.5);
  --shadow-md:       0 4px 6px -1px rgb(0 0 0 / 0.6);
}

[data-theme="invert"] {
  filter: invert(1) hue-rotate(180deg);
}
[data-theme="invert"] img,
[data-theme="invert"] video {
  filter: invert(1) hue-rotate(180deg);
}

[data-theme="read"] {
  --color-bg:   #F4ECD8;
  --color-text: #5C4B37;
  filter: contrast(0.92);
}
```

---

## Step 5 — Generate the Toggle (Black or White)

Pick from `templates/dark-mode/`:

- `toggle-classic.tsx` — simple sun/moon
- `toggle-black-or-white.tsx` — the MJ tribute

The Black or White toggle uses CSS view-transitions API where supported, falls back to a clip-path circular reveal animation:

```tsx
'use client'
import { useTheme } from '@/hooks/useTheme'

export function BlackOrWhiteToggle() {
  const { theme, setTheme } = useTheme()

  const toggle = async (e: React.MouseEvent) => {
    const next = theme === 'dark' ? 'light' : 'dark'

    // Modern browsers: smooth view transition with circular reveal
    if ('startViewTransition' in document) {
      const x = e.clientX, y = e.clientY
      const radius = Math.hypot(
        Math.max(x, innerWidth - x),
        Math.max(y, innerHeight - y),
      )

      // @ts-ignore - new API
      const transition = document.startViewTransition(() => setTheme(next))
      await transition.ready
      document.documentElement.animate(
        {
          clipPath: [
            `circle(0 at ${x}px ${y}px)`,
            `circle(${radius}px at ${x}px ${y}px)`,
          ],
        },
        { duration: 600, easing: 'ease-in-out',
          pseudoElement: '::view-transition-new(root)' },
      )
    } else {
      setTheme(next)
    }
  }

  return (
    <button
      aria-label="Toggle theme — Black or White"
      onClick={toggle}
      className="bow-toggle"
      data-theme-state={theme}
    >
      <span className="bow-orb" />
      <span className="sr-only">It don't matter if you're black or white</span>
    </button>
  )
}
```

CSS for the orb (lives in `dark-mode.css`):

```css
.bow-toggle {
  position: relative;
  width: 56px;
  height: 32px;
  border-radius: 999px;
  background: linear-gradient(90deg, #FFFFFF 0%, #FFFFFF 50%, #0A0A0A 50%, #0A0A0A 100%);
  background-size: 200% 100%;
  background-position: 0% 0%;
  border: 1px solid var(--color-border);
  cursor: pointer;
  transition: background-position 600ms cubic-bezier(.4,0,.2,1);
}

[data-theme="dark"] .bow-toggle {
  background-position: 100% 0%;
}

.bow-orb {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: radial-gradient(circle at 35% 35%, #1A1A1F 0%, #0A0A0A 70%);
  box-shadow: 0 0 0 2px rgba(255,255,255,0.1), inset 0 0 8px rgba(255,255,255,0.2);
  transition: transform 600ms cubic-bezier(.4,0,.2,1),
              background 400ms ease;
}

[data-theme="dark"] .bow-orb {
  transform: translateX(24px);
  background: radial-gradient(circle at 65% 35%, #FFFFFF 0%, #E5E5E5 70%);
}

/* The face-morph easter egg — subtle silhouette overlay during transition */
.bow-toggle::after {
  content: "";
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 56 32'><text x='28' y='22' text-anchor='middle' font-size='10' fill='currentColor' opacity='0.15'>♪</text></svg>");
  pointer-events: none;
  opacity: 0;
  transition: opacity 300ms ease;
}

.bow-toggle:hover::after { opacity: 0.4; }

/* Smooth color transition for everything else when theme changes */
:root, [data-theme] {
  transition: background-color 400ms ease, color 400ms ease, border-color 400ms ease;
}
```

---

## Step 6 — Hook + Provider

### `src/hooks/useTheme.ts`

```typescript
import { useEffect, useState } from 'react'

type Theme = 'light' | 'dark' | 'system'

export function useTheme() {
  const [theme, setThemeState] = useState<Theme>(() => {
    if (typeof window === 'undefined') return 'system'
    return (localStorage.getItem('theme') as Theme) || 'system'
  })

  const resolved = theme === 'system'
    ? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
    : theme

  useEffect(() => {
    document.documentElement.dataset.theme = resolved
  }, [resolved])

  useEffect(() => {
    localStorage.setItem('theme', theme)
  }, [theme])

  // Listen for system pref changes if user is on 'system'
  useEffect(() => {
    if (theme !== 'system') return
    const mq = window.matchMedia('(prefers-color-scheme: dark)')
    const handler = () => {
      document.documentElement.dataset.theme = mq.matches ? 'dark' : 'light'
    }
    mq.addEventListener('change', handler)
    return () => mq.removeEventListener('change', handler)
  }, [theme])

  return { theme: resolved, mode: theme, setTheme: setThemeState }
}
```

### `index.html` early script (avoids flash of unthemed content)

Insert in `<head>` BEFORE the main bundle:

```html
<script>
  (function() {
    try {
      var t = localStorage.getItem('theme') || 'system';
      var resolved = t === 'system'
        ? (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
        : t;
      document.documentElement.dataset.theme = resolved;
    } catch(e){}
  })();
</script>
```

---

## Step 7 — Tailwind Config Update (if applicable)

In `tailwind.config.{js,ts}`:

```ts
export default {
  darkMode: ['class', '[data-theme="dark"]'],
  // ... rest unchanged
}
```

Then `dark:bg-bg-subtle` etc. work everywhere automatically.

---

## Step 8 — Final Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ DARK MODE LIVE — and it looks rad

The Black or White toggle is in src/components/ThemeToggle/.
Drop it into your nav: <BlackOrWhiteToggle />

WHAT YOU GET:
  • Smooth circular-reveal animation on click
  • System preference respected by default
  • localStorage persists user choice
  • No flash of light on page load (early script in index.html)
  • Tailwind dark: variants work automatically [if Tailwind]

TRY IT:
  npm run dev
  → click the toggle, watch the page flip ✨

🌟 If this looks slick and you want to share it:
   The toggle is screenshot-bait. Tag #blackorwhite if you post it.

ADD MORE MODES?
  Re-run /dark-mode and pick "Five-state" for Light/Dark/Invert/Read/System.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Pairs With

- `/design` — generates the source `tokens.css` this skill inverts for dark mode
- `/scaffold` and `/webapp` can offer dark mode as a post-step

## Star-bait Notes

The MJ "Black or White" tribute is intentional — a memorable visual touch that makes the toggle feel like more than just CSS. The face-silhouette via SVG/text is subtle enough to be tasteful but easter-egg-y enough to make people screenshot it.
