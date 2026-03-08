## ADDED Requirements

### Requirement: Parent chain resolution
The deploy system SHALL resolve the full parent chain of a project type by following `ProjectTypeInfo.parent` links via entry points, producing an ordered list from root ancestor to the requested type.

#### Scenario: Single parent
- **WHEN** project type `web` has `parent: base`
- **THEN** the resolved chain is `[base, web]`

#### Scenario: No parent
- **WHEN** project type `base` has `parent: None`
- **THEN** the resolved chain is `[base]`

#### Scenario: Deep chain
- **WHEN** project type `nextjs-saas` has `parent: web` and `web` has `parent: base`
- **THEN** the resolved chain is `[base, web, nextjs-saas]`

#### Scenario: Unknown parent
- **WHEN** a project type references a parent that is not installed
- **THEN** a warning is printed and deployment continues with only the requested type (graceful degradation)

### Requirement: Parent-first template deployment
The deploy system SHALL deploy templates in parent-first order, with child templates overriding parent files when filenames collide.

#### Scenario: No file collision
- **WHEN** base/default has `rules/data-privacy.md` and web/nextjs has `rules/ui-conventions.md`
- **THEN** both files are deployed to the target project

#### Scenario: File collision
- **WHEN** base/default has `project-knowledge.yaml` and web/nextjs also has `project-knowledge.yaml`
- **THEN** the web/nextjs version is deployed (child wins), overriding the base version

#### Scenario: Template resolution per ancestor
- **WHEN** base has template `default` (auto-selected, single template) and web has template `nextjs` (specified by user)
- **THEN** each ancestor uses its own template resolution — base auto-selects `default`, web uses the user-specified `nextjs`

### Requirement: Module merging across ancestors
The deploy system SHALL merge optional modules from all ancestors and present them together during init.

#### Scenario: Modules from multiple ancestors
- **WHEN** base/default offers module `data-privacy` and web/nextjs offers module `integrations`
- **THEN** both modules are presented to the user with their source indicated: `data-privacy (base)`, `integrations (web)`

#### Scenario: Module ID collision
- **WHEN** base and web both define a module with ID `analytics`
- **THEN** the child's (web) definition wins, and a warning is logged

#### Scenario: Module deployment routes to source
- **WHEN** user selects module `data-privacy` (from base) and `integrations` (from web)
- **THEN** `data-privacy` files are resolved from base/default template directory and `integrations` files from web/nextjs template directory
