import pygame
from pygame import Vector2
from pygame.typing import SequenceLike, ColorLike
from src.snake import Snake
from src.fruit import Fruit
from src.helpers import load_font


class Game:
    def __init__(self, size: SequenceLike[float], caption: str, fps: int, cell_size: SequenceLike[float]) -> None:
        self.surface: pygame.Surface = pygame.display.set_mode(size)
        pygame.display.set_caption(caption)
        self.FPS: int = fps
        self.cell_size: Vector2 = Vector2(cell_size)
        self.clock: pygame.Clock = pygame.Clock()
        self.grid_size: Vector2 = Vector2(self.surface.width // self.cell_size.x,
                                          self.surface.height // self.cell_size.y)
        self.running: bool = True
        self.font: str = 'assets/fonts/DePixelHalbfett.ttf'

        self.snake: Snake = Snake(self.cell_size, 'green')
        self.apple: Fruit = Fruit((10, 7), self.cell_size, 'red')

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                self.snake.push_to_input_buffer(event.key)

    def win(self) -> None:
        self.end_game_screen('You Won', 'green')
        self.running = False

    def lose(self) -> None:
        self.end_game_screen('You Lose', 'red')
        self.running = False

    def end_game_screen(self, text: str, text_color: ColorLike):
        font: pygame.Font = load_font(self.font, 80)
        text: pygame.Surface = font.render(text, True, text_color)
        text_rect: pygame.Rect = text.get_rect(center=self.surface.get_rect().center)
        dark_overlay: pygame.Surface = pygame.surface.Surface(self.surface.size).convert_alpha()
        dark_overlay.fill((0, 0, 0, 200))
        dark_overlay.blit(text, text_rect)
        self.surface.blit(dark_overlay, (0, 0))
        pygame.display.flip()
        pygame.time.delay(2000)

    def update(self) -> None:
        self.snake.handle_input()
        self.snake.move()

        if self.snake.is_outside_bounds(self.grid_size) or self.snake.is_inside_itself():
            self.lose()

        if self.snake.body[0] == self.apple.pos:
            self.snake.grow()
            self.snake.score += 1
            if not self.apple.respawn(self.grid_size, self.snake.body):
                self.win()

    def render_text(self, text: str, size: int, pos: SequenceLike[float], color: ColorLike):
        font: pygame.Font = load_font(self.font, size)
        text: pygame.Surface = font.render(text, True, color)
        self.surface.blit(text, pos)

    def render(self) -> None:
        self.surface.fill('black')
        self.apple.draw(self.surface)
        self.snake.draw(self.surface)
        self.render_text(f'Score: {self.snake.score}', 20, (10, 10), '#ffffff')
        pygame.display.flip()

    def main(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.FPS)
