"""Command line interface for AI-SWA orchestration."""

import argparse
from pathlib import Path
import sys

from .orchestrator import Orchestrator
from .memory import Memory
from .planner import Planner
from .executor import Executor
from .reflector import Reflector


def build_parser() -> argparse.ArgumentParser:
    """Create and return the command line parser."""
    parser = argparse.ArgumentParser(description="AI-SWE orchestration CLI")
    parser.add_argument(
        "--memory",
        default="state.json",
        help="Path to persistent state file",
    )
    return parser


def main(argv=None):
    """Run the orchestrator using arguments from ``argv``."""
    parser = build_parser()
    args = parser.parse_args(argv)

    memory = Memory(Path(args.memory))
    try:
        memory.save(memory.load())
    except Exception as exc:  # pragma: no cover - unexpected I/O errors
        print(f"Error accessing memory: {exc}", file=sys.stderr)
        return 1

    planner = Planner()
    executor = Executor()
    reflector = Reflector()
    orchestrator = Orchestrator(planner, executor, reflector, memory)
    print("Orchestrator running")
    orchestrator.run()
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
