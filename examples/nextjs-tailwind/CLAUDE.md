# nextjs-tailwind

## Stack
- Next.js 15 (App Router)
- TypeScript (strict mode)
- Tailwind CSS 4
- Vitest + React Testing Library
- ESLint + Prettier
- Node 20 LTS (managed via nvm)

## Commands
- Start dev server: `npm run dev`
- Run tests: `npm test`
- Build for production: `npm run build`
- Start production server: `npm start`
- Install dependencies: `npm install`
- Lint: `npm run lint`
- Format: `npm run format`

## Environment
- Node: 20.x via nvm (`.nvmrc` set)
- Package manager: npm (or pnpm if preferred)
- TypeScript: strict mode enabled in `tsconfig.json`

## Project Structure
- `app/` — App Router pages, layouts, route handlers
  - `layout.tsx` — root layout
  - `page.tsx` — home page
  - `api/` — route handlers
- `components/` — reusable React components
- `lib/` — shared utilities, API clients, types
- `public/` — static assets
- `tests/` — Vitest test files

## Notes
- Tailwind classes — prefer composition via `clsx` over long className chains.
- Server components by default; mark client components with `"use client"`.
- Environment vars live in `.env.local` (gitignored). See `.env.example` for the shape.
- Never commit `.env.local`, `.next/`, or `node_modules/`.
