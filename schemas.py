from __future__ import annotations

from dataclasses import dataclass


# Directions are numbered clockwise, starting at north.
ORIENTATION_NAMES = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
DIRECTIONS = (
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1),
)


@dataclass(frozen=True)
class State:
    row: int
    column: int
    orientation: int


@dataclass
class Node:
    state: State
    parent: Node | None
    action: str | None
    depth: int
    cost: int
    heuristic: int = 0


@dataclass
class Result:
    final: Node | None
    last_examined: Node | None
    explored: int
    frontier: int
