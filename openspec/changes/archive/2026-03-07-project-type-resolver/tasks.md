## 1. ProjectTypeResolver core

- [x] 1.1 Create `wt_project_base/resolver.py` with `ProjectTypeResolver` class — constructor takes `ProjectType` instance and `overlay_path: Path`
- [x] 1.2 Implement `_load_overlay()` — parse YAML, extract custom_rules, disabled_rules, rule_overrides, custom_directives, disabled_directives (all optional, default empty)
- [x] 1.3 Implement `resolve_rules()` — package rules + custom_rules, filter disabled_rules by id, apply rule_overrides (merge config dicts), warn on unknown disabled ids
- [x] 1.4 Implement `resolve_directives()` — package directives + custom_directives, filter disabled_directives by id
- [x] 1.5 Implement `summary()` — return dict with counts: total, from_package, custom, disabled, overridden for both rules and directives

## 2. Local overrides layer

- [x] 2.1 Extend resolver to check for `.local-overrides.yaml` in same directory as overlay — apply as final layer after project-type.yaml
- [x] 2.2 Add `.local-overrides.yaml` to default .gitignore template in wt-project-base

## 3. Feedback system

- [x] 3.1 Create `wt_project_base/feedback.py` with `FeedbackLesson` dataclass — fields: rule_id, issue (enum), context, suggested_fix (type + value), timestamp
- [x] 3.2 Define issue enum: false_positive, too_aggressive, missing_exclude, missing_rule, config_improvement
- [x] 3.3 Implement `FeedbackStore` — load/append/save lessons from `wt/knowledge/lessons/rule-feedback.yaml`
- [x] 3.4 Implement `validate_lesson()` — check required fields, validate issue enum, warn if context contains path-like strings
- [x] 3.5 Implement `export_lessons()` — read all lessons, validate, output clean YAML with header comment, warn on potentially identifying content

## 4. CLI extensions

- [x] 4.1 Add `resolve` subcommand to `wt_project_base/cli.py` — accepts `--project-dir`, loads project type from `wt/plugins/project-type.yaml` type field via entry points, runs resolver, prints annotated rules and directives
- [x] 4.2 Add `feedback record` subcommand — non-interactive mode with `--rule-id`, `--issue`, `--context`, `--fix-type`, `--fix-value` flags
- [x] 4.3 Add `feedback export` subcommand — reads lessons, validates, prints anonymized YAML

## 5. YAML schema update

- [x] 5.1 Update `_save_project_type()` in wt-tools `bin/wt-project` to generate extended YAML with commented-out custom sections as documentation
- [x] 5.2 Add YAML format documentation as comments in the generated file

## 6. Testing with wt-project-web

- [x] 6.1 Create a test overlay YAML in wt-project-web's `wt/plugins/project-type.yaml` with custom_rules, disabled_rules, and rule_overrides
- [x] 6.2 Run `wt-project-base resolve --project-dir /home/tg/code2/wt-project-web` and verify merged output
- [x] 6.3 Record a test feedback lesson and verify export format
- [x] 6.4 Verify backward compat — run resolver on sales-raketa's existing project-type.yaml (no custom sections)
