# System Architecture

## Components

### Orchestrator
Coordinates the main control loop. It loads persistent state from
`Memory`, asks the `Planner` for the next action, executes it via the
`Executor` and finally allows the `SelfAuditor` to inspect results. The
class simply wires these components together and exposes a `run()`
method that will later contain the orchestration logic.

```python
class Orchestrator:
    def __init__(self, planner, executor, auditor, memory):
        self.planner = planner
        self.executor = executor
        self.auditor = auditor
        self.memory = memory

    def run(self):
        """Entry point for the orchestration loop."""
        pass
```

### CLI
Provides a thin command line wrapper around the `Orchestrator`. The
entrypoint defined in `core.cli` parses arguments, creates a `Memory`
instance and then runs the orchestrator.

```python
from pathlib import Path
from core.orchestrator import Orchestrator
from core.memory import Memory

def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    memory = Memory(Path(args.memory))
    orchestrator = Orchestrator(None, None, None, memory)
    orchestrator.run()
```

### Memory
Simple persistence helper for storing JSON state on disk. The API is a
minimal pair of `load()` and `save()` methods which read from and write
to a configured file path.

```python
from pathlib import Path
import json

class Memory:
    def __init__(self, path: Path):
        self.path = Path(path)

    def load(self):
        """Return stored data or an empty dict if no file exists."""
        pass

    def save(self, data):
        """Write data to disk creating directories as needed."""
        pass
```

### Planner
```python
class Planner:
    def plan(self, tasks):
        pass
```

### Executor
```python
class Executor:
    def execute(self, task):
        pass
```

### SelfAuditor
Evaluates code metrics and decides when refactors are required. Metrics are
obtained via **radon** (cyclomatic complexity and maintainability index) and,
optionally, **wily** for historical trends. The auditor never changes source
files itself. Instead it returns task dictionaries that the `Planner` appends to
`tasks.yml`. Each task describes the module, offending score and a brief
refactor suggestion.

```python
class SelfAuditor:
    def __init__(self, threshold: int = 15):
        self.threshold = threshold

    def analyze(self, paths):
        """Return a mapping of file paths to radon metrics."""

    def audit(self, tasks):
        """Return new task entries when complexity exceeds ``self.threshold``."""
```

After each execution cycle the `Orchestrator` calls `SelfAuditor.audit()` with
the current task list. Any returned entries are appended through the `Planner`,
which rewrites `tasks.yml` so that future iterations can schedule the
recommended refactors.

### Reflector
Coordinates a self-improvement cycle by scanning the repository and appending
new tasks when code complexity exceeds a threshold.

```python
from pathlib import Path
import yaml
from radon.complexity import cc_visit


class Reflector:
    def __init__(self, tasks_path: Path, threshold: int = 10, paths=None):
        self.tasks_path = Path(tasks_path)
        self.threshold = threshold
        self.paths = [Path(p) for p in paths] if paths else None

    def run_cycle(self):
        files = self.paths or list(Path('.').rglob('*.py'))
        metrics = self._analyze(files)
        tasks = self._load_tasks()
        new = self._decide(metrics, tasks)
        if new:
            tasks.extend(new)
            self._save_tasks(tasks)
        return new
```

## Bootstrapping Flow
```mermaid
flowchart TD
    A[Start] --> B[Load tasks.yml]
    B --> C{Valid?}
    C -- No --> D[Log error and exit]
    C -- Yes --> E[Select highest priority pending task]
    E --> F[Log task]
    F --> G[Exit success]
```

## CLI Invocation Flow
```mermaid
flowchart TD
    U[User] --> C[CLI parses arguments]
    C --> O[Create Orchestrator]
    O --> R[Orchestrator.run]
```

## Dependencies
- **PyYAML==6.0.1** - Safe YAML parsing
- **pytest==7.4.0** - Test execution
- **jsonschema==4.21.0** - Validate task schema
- **radon==5.1.0** - Compute code complexity metrics
- **wily==1.25.0** - Track complexity over Git history
- **pylint==3.3.7** - Linting and style checks

## Persistence Strategy
State such as tasks and logs are stored on disk. Tasks are kept in `tasks.yml` and
logs are written to the `logs/` directory. Future components may store structured
state in JSON files or use lightweight databases like SQLite.
