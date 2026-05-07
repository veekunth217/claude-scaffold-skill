'use client'
import { useTheme } from '@/hooks/useTheme'

/**
 * Black or White toggle — MJ tribute.
 * Uses View Transitions API with a clip-path circular reveal animation
 * originating from the click point. Falls back to instant theme swap
 * on browsers that don't support the API.
 *
 * Pair with the matching CSS in templates/dark-mode/dark-mode.css.
 */
export function BlackOrWhiteToggle() {
  const { theme, setTheme } = useTheme()

  const toggle = async (e: React.MouseEvent) => {
    const next = theme === 'dark' ? 'light' : 'dark'

    if ('startViewTransition' in document) {
      const x = e.clientX, y = e.clientY
      const radius = Math.hypot(
        Math.max(x, innerWidth - x),
        Math.max(y, innerHeight - y),
      )

      // @ts-ignore — new browser API
      const transition = document.startViewTransition(() => setTheme(next))
      await transition.ready
      document.documentElement.animate(
        {
          clipPath: [
            `circle(0 at ${x}px ${y}px)`,
            `circle(${radius}px at ${x}px ${y}px)`,
          ],
        },
        {
          duration: 600,
          easing: 'ease-in-out',
          pseudoElement: '::view-transition-new(root)',
        },
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
