"""Deterministic-step world logic. Import this module to simulate without a screen."""
from dataclasses import dataclass
from math import hypot
from typing import Optional
from ai.base import Action, Observation, BulletInfo
from ai.survival import SurvivalAI
from ai.risky_dodge import RiskyDodgeAI
from ai.battle import BattleAI
from game import config as C
from game.bullet import Bullet
from game.tank import Tank
from game.world import World

MODE_LABELS = {
    1: 'SURVIVAL',
    2: 'NEAR MISS',
    3: 'DUEL',
}


@dataclass(frozen=True)
class PlayerInput:
    move_x: float = 0.0
    move_y: float = 0.0
    aim_x: float = C.WIDTH / 2
    aim_y: float = C.HEIGHT / 2
    shoot: bool = False


class Game:
    def __init__(self):
        self.world = World()
        self.state = 'menu'
        self.mode = 1
        self.player = Tank(*C.PLAYER_START, C.PLAYER_SPEED, 'player')
        self.enemy = Tank(*C.AI_START, C.AI_SPEED, 'enemy')
        self.bullets = []
        self.elapsed = 0.0
        self.shots = 0
        self.ai_controller = SurvivalAI()
        self.ai_elapsed = 0.0
        self.last_ai_action = Action()

    def start(self, mode: int):
        if mode not in MODE_LABELS:
            raise ValueError(f'Invalid mode: {mode}')
        self.mode = mode
        self.state = 'playing'
        self.player = Tank(*C.PLAYER_START, C.PLAYER_SPEED, 'player')
        self.enemy = Tank(*C.AI_START, C.AI_SPEED, 'enemy', facing_x=-1.0)
        self.bullets = []
        self.elapsed = 0.0
        self.shots = 0
        self.ai_elapsed = C.AI_DECISION_INTERVAL  # Decide on first step.
        self.last_ai_action = Action()
        self.ai_controller = {1: SurvivalAI, 2: RiskyDodgeAI, 3: BattleAI}[mode]()

    def observation(self):
        return Observation(
            ai_x=self.enemy.x, ai_y=self.enemy.y,
            player_x=self.player.x, player_y=self.player.y,
            bullets=tuple(BulletInfo(b.x, b.y, b.vx, b.vy, b.owner)
                          for b in self.bullets),
            walls=tuple((w.x, w.y, w.width, w.height)
                        for w in self.world.walls),
            arena=(self.world.left, self.world.top,
                   self.world.right, self.world.bottom),
        )

    def _shoot(self, tank):
        if tank.reload > 0 or len(self.bullets) >= C.MAX_BULLETS:
            return False
        dx, dy = tank.facing_x, tank.facing_y
        muzzle = tank.radius + C.BULLET_RADIUS + 5
        self.bullets.append(Bullet(
            x=tank.x + dx*muzzle,
            y=tank.y + dy*muzzle,
            vx=dx*C.BULLET_SPEED,
            vy=dy*C.BULLET_SPEED,
            owner=tank.team,
        ))
        tank.reload = (C.SHOOT_COOLDOWN if tank.team == 'player'
                       else C.AI_SHOOT_COOLDOWN)
        if tank.team == 'player':
            self.shots += 1
        return True

    def step(self, dt: float, player_input: Optional[PlayerInput] = None):
        if self.state != 'playing':
            return
        if player_input is None:
            player_input = PlayerInput()
        self.elapsed += dt
        self.player.tick(dt)
        self.enemy.tick(dt)
        self.player.move(player_input.move_x, player_input.move_y, dt, self.world)
        self.player.aim(player_input.aim_x, player_input.aim_y)
        if player_input.shoot:
            self._shoot(self.player)

        self.ai_elapsed += dt
        if self.ai_elapsed >= C.AI_DECISION_INTERVAL:
            self.ai_elapsed %= C.AI_DECISION_INTERVAL
            self.last_ai_action = self.ai_controller.get_action(self.observation())
        ai = self.last_ai_action
        self.enemy.move(ai.move_x, ai.move_y, dt, self.world)
        self.enemy.aim(ai.aim_x, ai.aim_y)
        if ai.shoot:
            self._shoot(self.enemy)

        living_bullets = []
        for bullet in self.bullets:
            if not bullet.update(dt, self.world):
                continue
            # A bullet can only damage the *other* team. No instant self-hits.
            target = self.enemy if bullet.owner == 'player' else self.player
            if bullet.touches_tank(target):
                self.state = 'won' if bullet.owner == 'player' else 'lost'
                return
            living_bullets.append(bullet)
        self.bullets = living_bullets
