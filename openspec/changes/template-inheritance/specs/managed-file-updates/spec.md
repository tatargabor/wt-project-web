## ADDED Requirements

### Requirement: Managed-file header
Template-deployed files SHALL include a managed-file header comment that identifies the file as template-managed.

#### Scenario: Markdown file header
- **WHEN** a `.md` file is deployed from a template
- **THEN** the file content is prefixed with `<!-- wt-managed: <type>/<template> -->\n` before the original content

#### Scenario: YAML file header
- **WHEN** a `.yaml` or `.yml` file is deployed from a template
- **THEN** the file content is prefixed with `# wt-managed: <type>/<template>\n` before the original content

#### Scenario: Header identifies source
- **WHEN** `rules/ui-conventions.md` is deployed from web/nextjs template
- **THEN** the header reads `<!-- wt-managed: web/nextjs -->`

### Requirement: Update behavior based on managed header
On re-init (or `--update` flag), the deploy system SHALL check for managed-file headers to determine update behavior.

#### Scenario: Managed file exists — update
- **WHEN** a target file exists and contains a `wt-managed` header
- **THEN** the file is overwritten with the latest template version (including updated header)

#### Scenario: User-owned file — skip
- **WHEN** a target file exists but does NOT contain a `wt-managed` header
- **THEN** the file is skipped with message `Skipped (user-owned): <path>`

#### Scenario: File does not exist — deploy
- **WHEN** a target file does not exist
- **THEN** the file is deployed with managed header

#### Scenario: First init (no --update flag)
- **WHEN** init runs for the first time (no existing files)
- **THEN** all files are deployed with managed headers, same as current behavior plus headers

### Requirement: User opt-out from management
Users SHALL be able to take ownership of a managed file by removing the managed header.

#### Scenario: Remove header to take ownership
- **WHEN** a user edits `rules/ui-conventions.md` and removes the `<!-- wt-managed: web/nextjs -->` line
- **THEN** subsequent re-init skips this file, treating it as user-owned

#### Scenario: Re-add header to return to managed
- **WHEN** a user adds back `<!-- wt-managed: web/nextjs -->` to a file they previously took ownership of
- **THEN** subsequent re-init updates this file from the template again
