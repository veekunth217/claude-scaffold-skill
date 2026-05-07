'use client'
import { useTheme } from '@/hooks/useTheme'

/**
 * Classic sun/moon toggle.
 * Minimal, accessible, no animation library required.
 */
export function ClassicToggle() {
  const { theme, setTheme } = useTheme()
  const next = theme === 'dark' ? 'light' : 'dark'

  return (
    <button
      aria-label={`Switch to ${next} mode`}
      onClick={() => setTheme(next)}
      className="theme-toggle"
      data-theme-state={theme}
    >
      <span aria-hidden="true">{theme === 'dark' ? '☀️' : '🌙'}</span>
    </button>
  )
}
