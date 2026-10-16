"""Windows entry point. Run: python main.py"""
import pygame
from game import config as C
from game.game import Game, PlayerInput
from game.renderer import Renderer


def read_controls():
    keys = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return PlayerInput(
        move_x=float(keys[pygame.K_d]) - float(keys[pygame.K_a]),
        move_y=float(keys[pygame.K_s]) - float(keys[pygame.K_w]),
        aim_x=float(mouse_x), aim_y=float(mouse_y),
        shoot=pygame.mouse.get_pressed(num_buttons=3)[0] or keys[pygame.K_SPACE],
    )


def run():
    pygame.init()
    try:
        screen = pygame.display.set_mode((C.WIDTH, C.HEIGHT))
        pygame.display.set_caption('Tank Dodge Lab - AI Tank Prototype')
        clock = pygame.time.Clock()
        renderer = Renderer(screen)
        game = Game()
        paused = False
        show_debug = False
        accumulator = 0.0
        running = True
        while running:
            # Clamp long frames so returning from alt-tab doesn't simulate a huge burst.
            frame_dt = min(clock.tick(C.FPS_LIMIT) / 1000.0, 0.1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game.state = 'menu'
                        paused = False
                        accumulator = 0.0
                    elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                        if game.state == 'menu':
                            game.start({pygame.K_1: 1, pygame.K_2: 2,
                                        pygame.K_3: 3}[event.key])
                            accumulator = 0.0
                    elif event.key == pygame.K_r and game.state != 'menu':
                        game.start(game.mode)
                        paused = False
                        accumulator = 0.0
                    elif event.key == pygame.K_p and game.state == 'playing':
                        paused = not paused
                        accumulator = 0.0
                    elif event.key == pygame.K_F3:
                        show_debug = not show_debug
            if game.state == 'playing' and not paused:
                accumulator += frame_dt
                controls = read_controls()
                steps = 0
                while accumulator >= C.FIXED_DT and steps < 14:
                    game.step(C.FIXED_DT, controls)
                    accumulator -= C.FIXED_DT
                    steps += 1
                if steps == 14:
                    accumulator = 0.0  # Spiral-of-death safeguard on slower PCs.
            else:
                accumulator = 0.0
            renderer.render(game, paused=paused, fps=clock.get_fps(),
                            show_debug=show_debug)
    finally:
        pygame.quit()


if __name__ == '__main__':
    run()
