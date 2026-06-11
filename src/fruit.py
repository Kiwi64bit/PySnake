import pygame
from pygame import Vector2
import random


class Fruit:
    def __init__(self, pos: Vector2 | tuple[int, int], size: Vector2 | tuple[int, int],
                 color: pygame.Color | str) -> None:
        self.pos: Vector2 = Vector2(pos)
        self.size: Vector2 = Vector2(size)
        self.color: pygame.Color = pygame.Color(color)

    def respawn(self, grid_size: Vector2, snake_body: list[Vector2]) -> bool:
        grid_width: int = int(grid_size.x)
        grid_height: int = int(grid_size.y)
        all_positions: list[Vector2] = [Vector2(x, y) for x in range(grid_width) for y in range(grid_height)]
        available_positions: list[Vector2] = [pos for pos in all_positions if pos not in snake_body]
        if not available_positions:
            print("[Info] No available positions to spawn new fruit. Snake has filled the board.")
            return False
        self.pos = random.choice(available_positions)
        return True

    def grid_to_screen(self, grid_pos) -> Vector2:
        screen_pos: Vector2 = Vector2(grid_pos.x * self.size.x, grid_pos.y * self.size.y)
        return screen_pos

    def get_rect(self) -> pygame.Rect:
        pos: Vector2 = self.grid_to_screen(self.pos)
        rect: pygame.Rect = pygame.Rect(pos, self.size)
        return rect

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.get_rect())
