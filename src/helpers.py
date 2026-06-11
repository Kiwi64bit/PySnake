import pygame


def load_font(font: str, size: int) -> pygame.Font:
    try:
        return pygame.Font(font, size)
    except FileNotFoundError:
        print(f'[Warning] {font} was not found.')
        return pygame.Font(None, size)
