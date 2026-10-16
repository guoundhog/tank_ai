"""The AI API intentionally has NO Pygame dependency.

Replace rule-based controllers with a neural network later without changing
physics or renderer. A controller receives observations, returns actions.
"""
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class BulletInfo:
    x: float
    y: float
    vx: float
    vy: float
    owner: str


@dataclass(frozen=True)
class Observation:
    ai_x: float
    ai_y: float
    player_x: float
    player_y: float
    bullets: Tuple[BulletInfo, ...]
    # x, y, width, height per wall
    walls: Tuple[Tuple[float, float, float, float], ...]
    arena: Tuple[float, float, float, float]


@dataclass(frozen=True)
class Action:
    move_x: float = 0.0
    move_y: float = 0.0
    shoot: bool = False
    aim_x: float = 0.0
    aim_y: float = 0.0


class AIController:
    def get_action(self, observation: Observation) -> Action:
        raise NotImplementedError
