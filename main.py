import pygame
from src.game import Game

# pygame setup
pygame_modules: tuple[int, int] = pygame.init()
if pygame_modules[0] < 5:
    raise RuntimeError(f'Pygame failed to initialize. only {pygame_modules[0]} out of 5 modules initialized.')

if __name__ == '__main__':
    game: Game = Game((640, 600), 'Snake', 5, (40, 40))
    game.main()
    pygame.quit()
