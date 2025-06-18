from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Task:
    """Simple representation of a unit of work."""

    id: int
    description: str
    component: str
    dependencies: List[int]
    priority: int
    status: str
    command: Optional[str] = None
