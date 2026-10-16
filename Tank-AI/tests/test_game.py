import unittest
from game import config as C
from game.bullet import Bullet
from game.game import Game, PlayerInput
from game.tank import Tank
from game.world import World


class TankPhysicsTests(unittest.TestCase):
    def setUp(self):
        self.world = World()

    def test_bound_bounce(self):
        b = Bullet(self.world.right - 7, 200, 510, 0, 'player')
        self.assertTrue(b.update(.02, self.world))
        self.assertLess(b.vx, 0)
        self.assertEqual(b.bounces, 1)
        self.assertLessEqual(b.x + b.radius, self.world.right)

    def test_inner_wall_bounce(self):
        # First obstacle left face starts at x=301.
        b = Bullet(285, 230, 510, 0, 'player')
        for _ in range(5):
            b.update(C.FIXED_DT, self.world)
        self.assertLess(b.vx, 0)
        self.assertGreaterEqual(b.bounces, 1)

    def test_bullet_expiry(self):
        b = Bullet(150, 150, 1, 0, 'player', remaining=.01)
        self.assertFalse(b.update(.02, self.world))

    def test_tank_movement_stops_at_wall(self):
        t = Tank(265, 240, C.PLAYER_SPEED, 'player')
        for _ in range(60):
            t.move(1, 0, C.FIXED_DT, self.world)
        self.assertLessEqual(t.x + t.radius, 301)
        self.assertTrue(self.world.valid_circle(t.x, t.y, t.radius))

    def test_diagonal_movement_normalized(self):
        a = Tank(150, 150, 200, 'player')
        b = Tank(150, 150, 200, 'player')
        a.move(1, 0, .01, self.world)
        b.move(1, 1, .01, self.world)
        self.assertAlmostEqual((a.x-150)**2 + (a.y-150)**2,
                               (b.x-150)**2 + (b.y-150)**2, places=5)

    def test_modes_and_shooting(self):
        g = Game()
        self.assertEqual(g.state, 'menu')
        for mode in (1, 2, 3):
            g.start(mode)
            self.assertEqual(g.mode, mode)
            self.assertEqual(g.state, 'playing')
            g.step(C.FIXED_DT, PlayerInput(aim_x=800, aim_y=340, shoot=True))
            self.assertEqual(g.shots, 1)
            self.assertTrue(any(b.owner == 'player' for b in g.bullets))
            if mode == 3:
                self.assertTrue(any(b.owner == 'enemy' for b in g.bullets))
            else:
                self.assertFalse(any(b.owner == 'enemy' for b in g.bullets))

    def test_ai_does_not_walk_through_walls(self):
        g = Game()
        for mode in (1, 2, 3):
            g.start(mode)
            for _ in range(240):
                if g.state != 'playing':
                    break
                g.step(C.FIXED_DT, PlayerInput())
                self.assertTrue(g.world.valid_circle(
                    g.enemy.x, g.enemy.y, g.enemy.radius))


if __name__ == '__main__':
    unittest.main()
