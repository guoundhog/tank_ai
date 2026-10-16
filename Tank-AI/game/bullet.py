"""Ricocheting bullets. All collisions/physics are pure Python."""
from dataclasses import dataclass
from math import hypot
from game import config as C
from game.world import World, Wall


@dataclass
class Bullet:
    x: float
    y: float
    vx: float
    vy: float
    owner: str
    remaining: float = C.BULLET_LIFETIME
    radius: float = C.BULLET_RADIUS
    bounces: int = 0

    def _reflect_wall(self, wall: Wall, old_x: float, old_y: float):
        r = self.radius
        # Identify the face crossed during this short fixed-time step.
        if old_x + r <= wall.left and self.x + r >= wall.left and self.vx > 0:
            self.x = wall.left - r
            self.vx = -abs(self.vx)
        elif old_x - r >= wall.right and self.x - r <= wall.right and self.vx < 0:
            self.x = wall.right + r
            self.vx = abs(self.vx)
        elif old_y + r <= wall.top and self.y + r >= wall.top and self.vy > 0:
            self.y = wall.top - r
            self.vy = -abs(self.vy)
        elif old_y - r >= wall.bottom and self.y - r <= wall.bottom and self.vy < 0:
            self.y = wall.bottom + r
            self.vy = abs(self.vy)
        else:
            # Fallback for an edge/corner overlap: push out along least penetration.
            choices = [
                (abs(self.x + r - wall.left), 'left'),
                (abs(wall.right - (self.x - r)), 'right'),
                (abs(self.y + r - wall.top), 'top'),
                (abs(wall.bottom - (self.y - r)), 'bottom'),
            ]
            _, face = min(choices)
            if face == 'left':
                self.x, self.vx = wall.left - r, -abs(self.vx)
            elif face == 'right':
                self.x, self.vx = wall.right + r, abs(self.vx)
            elif face == 'top':
                self.y, self.vy = wall.top - r, -abs(self.vy)
            else:
                self.y, self.vy = wall.bottom + r, abs(self.vy)
        self.bounces += 1

    def update(self, dt: float, world: World):
        self.remaining -= dt
        if self.remaining <= 0:
            return False
        old_x, old_y = self.x, self.y
        self.x += self.vx * dt
        self.y += self.vy * dt
        r = self.radius
        if self.x - r < world.left:
            self.x, self.vx = world.left + r, abs(self.vx)
            self.bounces += 1
        elif self.x + r > world.right:
            self.x, self.vx = world.right - r, -abs(self.vx)
            self.bounces += 1
        if self.y - r < world.top:
            self.y, self.vy = world.top + r, abs(self.vy)
            self.bounces += 1
        elif self.y + r > world.bottom:
            self.y, self.vy = world.bottom - r, -abs(self.vy)
            self.bounces += 1
        for wall in world.walls:
            if wall.touches_circle(self.x, self.y, r):
                self._reflect_wall(wall, old_x, old_y)
                break
        return True

    def touches_tank(self, tank):
        return hypot(self.x - tank.x, self.y - tank.y) < self.radius + tank.radius
