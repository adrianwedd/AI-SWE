# Repository Guidelines for Codex Agent

These instructions apply to all files in this repository.

## Workflow
- Follow the Iterative Development Protocol described in `README.md`.
- Keep `tasks.yml` up to date, marking tasks as `done` once implemented.

## Commit Messages
- Use descriptive commit messages.
- For planning updates use `docs(planning): ...`.
- For features use `feat(component): ...`.
- For task completion use `chore(tasks): ...`.

## Testing
- Run `pytest --maxfail=1 --disable-warnings -q` before every commit.
- Ensure a clean working tree (`git status`) before committing.

