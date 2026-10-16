"""Pure-Python collision geometry, independent of Pygame."""
from dataclasses import dataclass
from math import hypot
from game import config as C


@dataclass(frozen=True)
class Wall:
    x: float
    y: float
    width: float
    height: float

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.width

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.height

    def closest_point(self, x, y):
        return (max(self.left, min(x, self.right)),
                max(self.top, min(y, self.bottom)))

    def touches_circle(self, x, y, radius):
        px, py = self.closest_point(x, y)
        return (x - px) ** 2 + (y - py) ** 2 < radius ** 2

    def distance_to(self, x, y):
        px, py = self.closest_point(x, y)
        return hypot(px - x, py - y)


class World:
    def __init__(self):
        self.left = C.ARENA_LEFT
        self.top = C.ARENA_TOP
        self.right = C.ARENA_RIGHT
        self.bottom = C.ARENA_BOTTOM
        # Keep these in one place, so training and rendering see identical walls.
        self.walls = [
            Wall(301, 169, 32, 173),
            Wall(667, 350, 32, 177),
            Wall(458, 297, 84, 30),
            Wall(465, 453, 70, 26),
        ]

    def valid_circle(self, x, y, radius):
        if (x - radius < self.left or x + radius > self.right
                or y - radius < self.top or y + radius > self.bottom):
            return False
        return not any(w.touches_circle(x, y, radius) for w in self.walls)

    def clearance(self, x, y):
        """Approximate free distance to the nearest wall/boundary."""
        free = min(x - self.left, self.right - x,
                   y - self.top, self.bottom - y)
        for w in self.walls:
            free = min(free, w.distance_to(x, y))
        return free
