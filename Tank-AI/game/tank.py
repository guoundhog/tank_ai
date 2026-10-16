"""Tank position and movement rules."""
from dataclasses import dataclass
from math import hypot
from game import config as C
from game.world import World


@dataclass
class Tank:
    x: float
    y: float
    speed: float
    team: str
    radius: float = C.TANK_RADIUS
    facing_x: float = 1.0
    facing_y: float = 0.0
    reload: float = 0.0

    def move(self, dx: float, dy: float, dt: float, world: World):
        length = hypot(dx, dy)
        if length > 1.0:
            dx, dy = dx / length, dy / length
        step_x, step_y = dx * self.speed * dt, dy * self.speed * dt
        # Sliding against obstacles feels much better than stopping completely.
        if world.valid_circle(self.x + step_x, self.y, self.radius):
            self.x += step_x
        if world.valid_circle(self.x, self.y + step_y, self.radius):
            self.y += step_y

    def aim(self, target_x: float, target_y: float):
        vx, vy = target_x - self.x, target_y - self.y
        length = hypot(vx, vy)
        if length > 0.001:
            self.facing_x, self.facing_y = vx / length, vy / length

    def tick(self, dt: float):
        self.reload = max(0.0, self.reload - dt)
