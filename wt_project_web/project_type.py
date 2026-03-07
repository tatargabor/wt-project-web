"""Web project type plugin for wt-tools."""

from pathlib import Path
from typing import List, Optional

from wt_project_web.base import (
    OrchestrationDirective,
    ProjectType,
    ProjectTypeInfo,
    TemplateInfo,
    VerificationRule,
)


class WebProjectType(ProjectType):
    """Web application project type.

    Provides knowledge templates, verification rules, and orchestration
    directives for web projects (Next.js, generic SPA).
    """

    @property
    def info(self) -> ProjectTypeInfo:
        return ProjectTypeInfo(
            name="web",
            version="0.1.0",
            description="Web application project knowledge (i18n, routing, DB, components)",
            parent="base",
        )

    def get_templates(self) -> List[TemplateInfo]:
        return [
            TemplateInfo(
                id="nextjs",
                description="Next.js App Router with Prisma, next-intl, shadcn/ui",
                template_dir="templates/nextjs",
            ),
            TemplateInfo(
                id="spa",
                description="Generic single-page application (minimal starting point)",
                template_dir="templates/spa",
            ),
        ]

    def get_verification_rules(self) -> List[VerificationRule]:
        return [
            VerificationRule(
                id="i18n-completeness",
                description="All UI strings must exist in all locale files",
                check="cross-file-key-parity",
                severity="error",
                config={"files": {"pattern": "messages/*.json"}},
            ),
            VerificationRule(
                id="route-registered",
                description="New page routes should be registered in navigation config",
                check="file-mentions",
                severity="warning",
                config={
                    "source": {
                        "pattern": "src/app/**/page.tsx",
                        "exclude": ["src/app/api/**", "src/app/login/**", "src/app/register/**"],
                    },
                    "target": "cross-cutting.sidebar",
                },
            ),
            VerificationRule(
                id="cross-cutting-consistency",
                description="Sidebar items, route labels, and i18n keys must be in sync",
                check="cross-reference",
                severity="warning",
                config={
                    "groups": [
                        {
                            "name": "navigation",
                            "files": [
                                {"role": "sidebar"},
                                {"role": "route_labels"},
                                {"role": "i18n"},
                            ],
                            "key_pattern": "route-segment",
                        }
                    ]
                },
            ),
            VerificationRule(
                id="migration-safety",
                description="Schema changes must have corresponding migrations",
                check="schema-migration-sync",
                severity="error",
                config={
                    "schema_file": "prisma/schema.prisma",
                    "migrations_dir": "prisma/migrations/",
                    "design_doc": "docs/design/data-model.md",
                },
            ),
            VerificationRule(
                id="file-size-limit",
                description="Source files should not exceed 400 lines",
                check="file-line-count",
                severity="warning",
                config={
                    "pattern": "src/**/*.{tsx,ts}",
                    "max_lines": 400,
                },
            ),
            VerificationRule(
                id="ghost-button-text",
                description="Ghost buttons must be icon-only (no text content)",
                check="pattern-absence",
                severity="warning",
                config={
                    "pattern": "src/components/**/*.tsx",
                    "forbidden": r'variant="ghost".*>[^<]*<',
                },
            ),
        ]

    def get_orchestration_directives(self) -> List[OrchestrationDirective]:
        return [
            OrchestrationDirective(
                id="no-parallel-i18n",
                description="Serialize changes that modify locale files to prevent merge conflicts",
                trigger='change-modifies("messages/*.json")',
                action="serialize",
                config={"with": 'changes-modifying("messages/*.json")'},
            ),
            OrchestrationDirective(
                id="consolidate-i18n",
                description="Warn when multiple changes each modify locale files",
                trigger='plan-has-multiple-changes-modifying("messages/*.json")',
                action="warn",
                config={
                    "message": "Multiple changes modify locale files — consider consolidating into a single i18n change"
                },
            ),
            OrchestrationDirective(
                id="db-generate",
                description="Regenerate Prisma client after schema changes",
                trigger='change-modifies("prisma/schema.prisma")',
                action="post-merge",
                config={"command": "pnpm db:generate"},
            ),
            OrchestrationDirective(
                id="install-deps",
                description="Install dependencies after package.json changes",
                trigger='change-modifies("package.json")',
                action="post-merge",
                config={"command": "pnpm install"},
            ),
            OrchestrationDirective(
                id="cross-cutting-review",
                description="Flag changes to cross-cutting files for extra review",
                trigger="change-modifies-any(cross_cutting_files.sidebar, cross_cutting_files.i18n, cross_cutting_files.route_labels)",
                action="flag-for-review",
            ),
        ]
