## MODIFIED Requirements

### Requirement: Template file deployment
The deploy system SHALL deploy template files from a project type into a target project directory, walking the parent chain and respecting managed-file headers.

#### Scenario: Deploy with inheritance
- **WHEN** `deploy_templates()` is called for project type `web` with `parent: base`
- **THEN** the system resolves the chain `[base, web]`, deploys base/default template first, then web/nextjs template, with child files overriding parent files

#### Scenario: Deploy with modules from multiple ancestors
- **WHEN** user selects modules `data-privacy,integrations` and `data-privacy` belongs to base, `integrations` belongs to web
- **THEN** each module's files are resolved from their respective ancestor's template directory

#### Scenario: Backward compatibility — no parent
- **WHEN** a project type has no parent (e.g., `base` itself)
- **THEN** deployment works exactly as before — single template, no chain resolution

#### Scenario: Backward compatibility — no manifest
- **WHEN** a template directory has no `manifest.yaml`
- **THEN** all files are deployed (walk directory), same as current behavior

#### Scenario: Re-init updates managed files
- **WHEN** `wt-project init` is re-run on an existing project
- **THEN** files with `wt-managed` headers are updated from latest template, files without headers are skipped
