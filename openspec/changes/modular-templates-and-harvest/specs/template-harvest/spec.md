## ADDED Requirements

### Requirement: Harvest skill
A `/wt:harvest` skill SHALL compare a source project's rules against the current template and propose candidates for generalization into optional template modules.

#### Scenario: Diff source vs template
- **WHEN** `/wt:harvest --from /path/to/project` is run
- **THEN** the skill reads `.claude/rules/*.md` from the source project and compares against the template's manifest (core + existing modules), identifying files that are new or richer in the source

#### Scenario: Classify candidates
- **WHEN** candidate files are identified
- **THEN** each candidate is classified as `base` (universal, any project type), `web` (web-specific template), or `skip` (too project-specific to generalize)

#### Scenario: Generalize content
- **WHEN** a candidate is classified as `base` or `web`
- **THEN** the skill strips project-specific paths, entity names, and API references, producing a generalized version

#### Scenario: User review and approval
- **WHEN** generalized candidates are ready
- **THEN** a summary is shown with the original vs generalized content, and the user approves, edits, or skips each candidate

#### Scenario: Write approved modules
- **WHEN** the user approves a candidate
- **THEN** the file is written to the target template directory and `manifest.yaml` is updated with a new optional module entry

### Requirement: Divergence detection
The harvest skill SHALL detect when a template rule file has diverged from (is a subset of) the source project's version.

#### Scenario: Template rule is subset of project rule
- **WHEN** `ui-conventions.md` in the source project has sections not present in the template version
- **THEN** the skill reports the divergence and offers to merge the new sections back into the template's core file

#### Scenario: No divergence
- **WHEN** all template rules are identical or superset of the source project's versions
- **THEN** no divergence is reported
