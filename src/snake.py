import pygame
from pygame import Vector2


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
                pygame.K_UP   : self.move_up,
                pygame.K_DOWN : self.move_down,
                pygame.K_LEFT : self.move_left,
                pygame.K_RIGHT: self.move_right,
                pygame.K_w    : self.move_up,
                pygame.K_s    : self.move_down,
                pygame.K_a    : self.move_left,
                pygame.K_d    : self.move_right,
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
        in_vertical_bounds: bool = 0 <= self.body[0].y <= (grid_size.y - 1)
        return not (in_horizontal_bounds and in_vertical_bounds)

    def grid_to_screen(self, grid_pos) -> Vector2:
        screen_pos: Vector2 = Vector2(grid_pos.x * self.cell_size.x, grid_pos.y * self.cell_size.y)
        return screen_pos

    def draw(self, surface: pygame.Surface) -> None:
        for pos in self.body:
            rect: pygame.Rect = pygame.Rect(self.grid_to_screen(pos), self.cell_size)
            pygame.draw.rect(surface, self.color, rect)
