"""All screen drawing stays here. Import pygame ONLY for presentation."""
import math
import pygame
from game import config as C
from game.game import MODE_LABELS

BG = (13, 19, 30)
FIELD = (22, 35, 49)
GRID = (34, 52, 67)
BORDER = (71, 110, 130)
WHITE = (230, 240, 244)
MUTED = (151, 171, 186)
GREEN = (68, 217, 149)
GREEN_DARK = (24, 110, 78)
RED = (250, 105, 103)
RED_DARK = (123, 49, 63)
GOLD = (255, 214, 109)


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.SysFont('segoeui,arial', 52, bold=True)
        self.hud_font = pygame.font.SysFont('segoeui,arial', 22, bold=True)
        self.text_font = pygame.font.SysFont('segoeui,arial', 20)
        self.small_font = pygame.font.SysFont('segoeui,arial', 15)
        self.mono_font = pygame.font.SysFont('consolas,monospace', 17)
        self.field_surface = pygame.Surface((C.WIDTH, C.HEIGHT)).convert()
        self._make_field()

    def _text(self, text, x, y, font=None, color=WHITE, center=False):
        font = font or self.text_font
        surface = font.render(str(text), True, color)
        rect = surface.get_rect()
        if center:
            rect.center = (int(x), int(y))
        else:
            rect.topleft = (int(x), int(y))
        self.screen.blit(surface, rect)

    def _make_field(self):
        self.field_surface.fill(BG)
        field = pygame.Rect(int(C.ARENA_LEFT), int(C.ARENA_TOP),
                            int(C.ARENA_RIGHT-C.ARENA_LEFT),
                            int(C.ARENA_BOTTOM-C.ARENA_TOP))
        pygame.draw.rect(self.field_surface, FIELD, field, border_radius=8)
        for x in range(int(C.ARENA_LEFT)+16, int(C.ARENA_RIGHT), 32):
            pygame.draw.line(self.field_surface, GRID,
                             (x, int(C.ARENA_TOP)), (x, int(C.ARENA_BOTTOM)), 1)
        for y in range(int(C.ARENA_TOP)+16, int(C.ARENA_BOTTOM), 32):
            pygame.draw.line(self.field_surface, GRID,
                             (int(C.ARENA_LEFT), y), (int(C.ARENA_RIGHT), y), 1)
        pygame.draw.rect(self.field_surface, BORDER, field, width=3, border_radius=8)
        pygame.draw.line(self.field_surface, (41, 62, 77),
                         (0, 70), (C.WIDTH, 70), 1)

    def _wall(self, wall):
        rect = pygame.Rect(round(wall.x), round(wall.y),
                           round(wall.width), round(wall.height))
        pygame.draw.rect(self.screen, (7, 13, 21), rect.move(4, 6), border_radius=4)
        pygame.draw.rect(self.screen, (99, 121, 133), rect, border_radius=4)
        pygame.draw.rect(self.screen, (133, 155, 162), rect.inflate(-5, -5),
                         width=2, border_radius=2)
        if rect.width > 45:
            pygame.draw.line(self.screen, (153, 168, 174),
                             (rect.left+10, rect.top+8),
                             (rect.right-10, rect.top+8), 1)

    def _tank(self, tank, body, dark):
        # Both tank chassis and turret rotate towards their target.
        x, y = tank.x, tank.y
        dx, dy = tank.facing_x, tank.facing_y
        side_x, side_y = -dy, dx

        def local(u, v):
            return (round(x + u*dx + v*side_x),
                    round(y + u*dy + v*side_y))

        pygame.draw.circle(self.screen, (9, 15, 22), (round(x+3), round(y+4)), 23)
        for sign in (-1, 1):
            track = [local(-17, sign*12), local(17, sign*12),
                     local(17, sign*20), local(-17, sign*20)]
            pygame.draw.polygon(self.screen, dark, track)
            pygame.draw.polygon(self.screen, (96, 109, 117), track, 1)
        chassis = [local(-16, -15), local(16, -15),
                   local(18, 0), local(16, 15), local(-16, 15)]
        pygame.draw.polygon(self.screen, body, chassis)
        pygame.draw.polygon(self.screen, (222, 233, 235), chassis, 1)
        pygame.draw.line(self.screen, dark, local(1, 0), local(33, 0), 11)
        pygame.draw.line(self.screen, (230, 233, 226), local(14, 0), local(34, 0), 4)
        pygame.draw.circle(self.screen, dark, local(0, 0), 10)
        pygame.draw.circle(self.screen, body, local(0, 0), 7)
        pygame.draw.circle(self.screen, (220, 234, 231), local(0, 0), 7, 1)

    def _bullets(self, bullets):
        for b in bullets:
            color = GOLD if b.owner == 'player' else (255, 128, 117)
            mag = max(1.0, math.hypot(b.vx, b.vy))
            tx = b.x - b.vx/mag*13
            ty = b.y - b.vy/mag*13
            pygame.draw.line(self.screen, color,
                             (round(tx), round(ty)), (round(b.x), round(b.y)), 3)
            pygame.draw.circle(self.screen, (250, 246, 230),
                               (round(b.x), round(b.y)), round(b.radius))

    def _arena(self, game):
        self.screen.blit(self.field_surface, (0, 0))
        for wall in game.world.walls:
            self._wall(wall)
        self._bullets(game.bullets)
        self._tank(game.player, GREEN, GREEN_DARK)
        self._tank(game.enemy, RED, RED_DARK)
        self._text('YOU', game.player.x, game.player.y - 36,
                   self.small_font, GREEN, center=True)
        self._text('AI', game.enemy.x, game.enemy.y - 36,
                   self.small_font, RED, center=True)

    def _hud(self, game, fps=None, show_debug=False):
        self._text('TANK AI', 32, 18, self.hud_font, WHITE)
        self._text(f'MODE {game.mode}: {MODE_LABELS[game.mode]}',
                   183, 23, self.mono_font, GREEN)
        self._text(f'TIME {game.elapsed:05.1f}s', 575, 23,
                   self.mono_font, WHITE)
        self._text(f'SHOTS {game.shots:02d}', 768, 23,
                   self.mono_font, WHITE)
        self._text('WASD Move    Mouse Aim    Click Fire    P Pause    R Restart    Esc Menu',
                   35, C.HEIGHT-25, self.small_font, MUTED)
        if show_debug and fps is not None:
            self._text(f'FPS {fps:.0f}  |  BULLETS {len(game.bullets)}',
                       710, 52, self.small_font, GOLD)

    def _overlay(self, main_text, line1, line2):
        shade = pygame.Surface((C.WIDTH, C.HEIGHT), pygame.SRCALPHA)
        shade.fill((3, 8, 16, 208))
        self.screen.blit(shade, (0, 0))
        self._text(main_text, C.WIDTH/2, 232, self.title_font, WHITE, center=True)
        self._text(line1, C.WIDTH/2, 306, self.text_font, MUTED, center=True)
        self._text(line2, C.WIDTH/2, 345, self.text_font, GREEN, center=True)

    def render(self, game, paused=False, fps=None, show_debug=False):
        self._arena(game)
        self._hud(game, fps, show_debug)
        if game.state == 'menu':
            self._overlay('TANK DODGE LAB', 'Choose your AI opponent',
                          '1  SURVIVAL     2  NEAR MISS     3  DUEL')
            self._text('Rule-based AI prototypes  |  Neural models come later',
                       C.WIDTH/2, 398, self.small_font, MUTED, center=True)
            self._text('WASD Move   /   Mouse Aim   /   Hold Left Click to Fire',
                       C.WIDTH/2, 440, self.small_font, WHITE, center=True)
        elif game.state == 'won':
            self._overlay('YOU WIN!', f'{game.elapsed:.1f} seconds  |  {game.shots} shots',
                          'R  Retry    |    Esc  Menu')
        elif game.state == 'lost':
            self._overlay('GAME OVER', 'You were hit by the enemy tank.',
                          'R  Retry    |    Esc  Menu')
        elif paused:
            self._overlay('PAUSED', 'Take a break.', 'P  Continue    |    Esc  Menu')
        pygame.display.flip()
