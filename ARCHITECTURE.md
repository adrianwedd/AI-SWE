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
```python
class SelfAuditor:
    def audit(self):
        pass
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

## Persistence Strategy
State such as tasks and logs are stored on disk. Tasks are kept in `tasks.yml` and
logs are written to the `logs/` directory. Future components may store structured
state in JSON files or use lightweight databases like SQLite.
