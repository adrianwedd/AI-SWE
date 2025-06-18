# Research Brief RB-001: Code Quality Analysis for SelfAuditor

## Library Comparison

### Radon 5.1.0
- Provides command line and API access to cyclomatic complexity (CC), raw metrics, maintainability index (MI) and Halstead complexity.
- Lightweight with minimal dependencies (`mando`, `colorama`, `six`).
- Suitable for on-demand analysis of individual modules.

### Wily 1.25.0
- Builds on Radon and Git history to track complexity and maintainability over time.
- Stores historical metrics in a local database; supports plotting and comparison between revisions.
- Higher overhead but useful for trend-based auditing.

### Pylint 3.3.7
- Full static analysis linter producing code style warnings and an overall score.
- Detects dead code, unused variables and potential errors beyond complexity metrics.
- Can be slower but offers comprehensive quality checks.

## Proposed Heuristic
- Run Radon on modified modules after each orchestration cycle.
- If any function has CC > **15** or module MI < **60**, flag it for refactoring.
- Optionally use Wily for historical trends; if complexity continually rises over three revisions, escalate priority.

## Implementation Strategy
- The SelfAuditor should **not** modify code directly.
- When thresholds are exceeded, it appends a new task entry to `tasks.yml` describing the recommended refactor.
- Planner then incorporates these tasks into future iterations.

