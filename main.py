import pygame
from pygame import Vector2
import random

# pygame setup
pygame_modules: tuple[int, int] = pygame.init()
if pygame_modules[0] < 5:
    raise RuntimeError(f'Pygame failed to initialize. only {pygame_modules[0]} out of 5 modules initialized.')

class Snake:
    def __init__(self, cell_size: Vector2 | tuple[int, int], color: pygame.Color | str) -> None:
        self.body: list[Vector2] = [
            Vector2(4, 7),
            Vector2(3, 7),
            Vector2(2, 7)
        ]
        self.cell_size: Vector2 = Vector2(cell_size)
        self.color: pygame.Color = pygame.Color(color)
        self.direction: Vector2 = Vector2(1, 0)
        self.score: int = 0
        self.input_buffer: list = []

        self.can_move: bool = False
        self.can_grow: bool = False

        self.controls: dict[int, ...] = {
            pygame.K_UP: self.move_up,
            pygame.K_DOWN: self.move_down,
            pygame.K_LEFT: self.move_left,
            pygame.K_RIGHT: self.move_right,
        }

    def set_direction(self, new_direction: Vector2 | tuple[int, int]) -> None:
        new_direction: Vector2 = Vector2(new_direction)
        if new_direction and new_direction != -self.direction:
            self.direction = new_direction

    def move_up(self) -> None:
        self.set_direction((0, -1))
        self.can_move = True

    def move_down(self) -> None:
        self.set_direction((0, 1))
        self.can_move = True

    def move_left(self) -> None:
        self.set_direction((-1, 0))
        self.can_move = True

    def move_right(self) -> None:
        self.set_direction((1, 0))
        self.can_move = True

    def push_to_input_buffer(self, key: int, max_len=3) -> None:
        buffer_not_full: bool = len(self.input_buffer) < max_len
        new_key: bool = key != self.input_buffer[-1] if self.input_buffer else True
        valid_control_key: bool = key in self.controls.keys()

        if buffer_not_full and new_key and valid_control_key:
            self.input_buffer.append(key)

    def handle_input(self) -> None:
        if self.input_buffer:
            key: int = self.input_buffer.pop(0)
            self.controls[key]()

    def move(self) -> None:
        if not self.can_move:
            return

        new_head: Vector2 = self.body[0] + self.direction
        self.body.insert(0, new_head)
        if not self.can_grow:
            self.body.pop()
            return
        self.can_grow = False

    def grow(self) -> None:
        self.can_grow = True

    def is_inside_itself(self) -> bool:
        return self.body[0] in self.body[1:]

    def is_outside_bounds(self, grid_size: Vector2) -> bool:
        in_horizontal_bounds: bool = 0 <= self.body[0].x <= (grid_size.x - 1)
        in_vertical_bounds:   bool = 0 <= self.body[0].y <= (grid_size.y - 1)
        return not (in_horizontal_bounds and in_vertical_bounds)

    def grid_to_screen(self, grid_pos) -> Vector2:
        screen_pos: Vector2 = Vector2(grid_pos.x * self.cell_size.x, grid_pos.y * self.cell_size.y)
        return screen_pos

    def draw(self, surface: pygame.Surface) -> None:
        for pos in self.body:
            rect: pygame.Rect = pygame.Rect(self.grid_to_screen(pos), self.cell_size)
            pygame.draw.rect(surface, self.color, rect)


class Fruit:
    def __init__(self, pos: Vector2 | tuple[int, int], size: Vector2 | tuple[int, int], color: pygame.Color | str) -> None:
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


class Game:
    def __init__(self, size: Vector2 | tuple[int, int], caption: str, fps: int, cell_size: Vector2 | tuple[int, int]) -> None:
        self.surface: pygame.Surface = pygame.display.set_mode(size)
        pygame.display.set_caption(caption)
        self.FPS: int = fps
        self.cell_size: Vector2 = Vector2(cell_size)
        self.clock: pygame.Clock = pygame.Clock()
        self.grid_size: Vector2 = Vector2(self.surface.width // self.cell_size.x, self.surface.height // self.cell_size.y)
        self.running: bool = True
        self.font: str = 'fonts/DePixelHalbfett.ttf'

        self.snake: Snake = Snake(self.cell_size, 'green')
        self.apple: Fruit = Fruit((10, 7), self.cell_size, 'red')

    @staticmethod
    def load_font(font: str, size: int) -> pygame.Font:
        try:
            return pygame.font.Font(font, size)
        except FileNotFoundError:
            print(f'[Warning] {font} was not found.')
            return pygame.font.SysFont('CambriaMath', size)

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

    def end_game_screen(self, text: str, text_color: pygame.Color | str):
        font: pygame.Font = self.load_font(self.font, 80)
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

    def render_text(self, text: str, size: int, pos: Vector2 | tuple[int, int], color: pygame.Color | str):
        font: pygame.Font = self.load_font(self.font, size)
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



if __name__ == '__main__':
    game: Game = Game((640, 600), 'Snake', 5, (40, 40))
    game.main()
    pygame.quit()
