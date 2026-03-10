# wt-project-web

Web project type plugin for [wt-tools](https://github.com/anthropics/wt-tools). Provides web-specific verification rules, orchestration directives, and project templates on top of [wt-project-base](https://github.com/anthropics/wt-project-base).

## Quick Start

```bash
# Install
pip install wt-project-web

# Initialize a Next.js project
wt-project-web init --type nextjs --target /path/to/project

# List available templates
wt-project-web list
```

## What It Provides

### Templates
- **Next.js App Router** (`nextjs`) — Full-stack Next.js with Prisma, next-intl, shadcn/ui
- **Generic SPA** (`spa`) — Minimal starting point for any SPA framework

### Convention Rules (12 path-scoped rule files)

| Rule File | Covers |
|-----------|--------|
| `ui-conventions` | shadcn/ui, responsive breakpoints, toast, skeleton, empty states |
| `functional-conventions` | Server actions, API route handlers, Prisma, multi-step forms |
| `auth-conventions` | NextAuth v5, roles, middleware, bcrypt |
| `data-model` | Prisma schema, migrations, seeding, state machines |
| `deployment` | Migration-first deploy, health check, env var documentation |
| `testing-conventions` | Testing diamond, Playwright E2E, cold-visit tests, port isolation |
| `integrations` | Webhooks, API clients, retry with backoff |
| `seo-conventions` | Metadata, Open Graph, JSON-LD, sitemap, robots, canonical/hreflang |
| `accessibility` | WCAG 2.1 AA, semantic HTML, ARIA, focus, contrast, reduced motion |
| `performance` | Core Web Vitals, next/image, next/font, caching, bundle hygiene |
| `security` | CSP, HSTS, CORS, rate limiting, input validation, NEXT_PUBLIC_ safety |
| `error-handling` | Error boundaries, not-found pages, loading states, global-error |

### Verification Rules (11 web-specific)

| Rule | Severity | Check |
|------|----------|-------|
| `i18n-completeness` | error | All locale files must have the same keys |
| `route-registered` | warning | New pages should appear in navigation |
| `cross-cutting-consistency` | warning | Sidebar, routes, and i18n stay in sync |
| `migration-safety` | error | Schema changes need migration files |
| `ghost-button-text` | warning | Ghost buttons must be icon-only |
| `functional-test-coverage` | warning | Feature changes need Playwright tests |
| `page-metadata` | warning | Public pages must export metadata for SEO |
| `image-alt-text` | warning | Images must have alt text for accessibility |
| `env-example-sync` | warning | New env vars must be in .env.example |
| `error-boundary-exists` | warning | App must have error.tsx, global-error.tsx, not-found.tsx |
| `no-public-secrets` | error | NEXT_PUBLIC_ must not prefix secret-like vars |

Plus base rules from `wt-project-base` (file-size-limit, no-secrets-in-source, todo-tracking).

### Orchestration Directives (7 web-specific)

| Directive | Action | Trigger |
|-----------|--------|---------|
| `no-parallel-i18n` | serialize | Changes modifying locale files |
| `consolidate-i18n` | warn | Multiple changes touch locale files |
| `db-generate` | post-merge | Schema changes → `pnpm db:generate` |
| `db-seed` | post-merge | Schema changes → `pnpm db:seed` |
| `cross-cutting-review` | flag-for-review | Cross-cutting file modifications |
| `playwright-setup` | warn | First Playwright test file created |
| `env-example-review` | flag-for-review | .env.example modifications |

Plus base directives from `wt-project-base` (install-deps, no-parallel-lockfile, config-review).

## Plugin Architecture

```
wt-project-base          Universal rules (file size, secrets, TODOs)
  └── wt-project-web      Web domain rules (i18n, routing, DB, components)
        └── your-org-web   Organization-specific rules (your conventions)
```

Each layer inherits from its parent. Customize via `wt/plugins/project-type.yaml` without writing Python.

## Documentation

- [Plugin Architecture](docs/plugin-architecture.md) — Three-layer hierarchy and customization
- [Template Reference](docs/template-reference.md) — Template files and sections
- [Verification Rules Reference](docs/verification-rules-reference.md) — All rules with check types
