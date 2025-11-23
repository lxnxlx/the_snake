from random import choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
#  Множество центров точек ячек площадью 20х20 пикселей
ALL_CELLS = {
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
}


# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Родительский Класс"""

    def __init__(
            self,
            position=(0, 0),
            body_color=(0, 0, 0)
    ):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Это абстрактный метод,
        который предназначен для переопределения в дочерних классах.
        """
        pass


class Snake(GameObject):
    """Класс объекта змейка."""

    def __init__(
            self,
            position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            body_color=SNAKE_COLOR
    ):
        super().__init__(position, body_color)
        self.length = 1
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновление положения змейки в игре."""
        head_x, head_y = self.get_head_position()
        new_head_x = (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_head_x, new_head_y)
        self.positions.insert(0, new_head)

    def cut_tail(self):
        """Удаляет хвост, если длина превышает допустимую."""
        """
        Вынес в отдельный метод для контроля удаления,
        т.к. если это реализоватьть в методе move,
        то после первого поедания яблока змея не будет расти.
        """

        if len(self.positions) > self.length:
            return self.positions.pop()
        return None

    def draw(self):
        """Рисует все сегменты змейки."""
        # Изменен прекод, чтобы не стирать постоянно последний элемент.
        for position in self.positions[:self.length]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Возвращает координаты головы змеи."""
        return self.positions[0]

    @property
    def body_pos(self):
        """
        Возвращает координаты змейки,
        нужен для определения координат яблока.
        """
        return self.positions

    def reset(self):
        """Возвращает змейку в исходное положение"""
        self.positions = [self.position]
        self.length = 1
        self.direction = choice([UP, DOWN, RIGHT, LEFT])
        self.next_direction = None
        self.last = None


class Apple(GameObject):
    """Яблоко для игры"""

    def __init__(self,
                 position=(0, 0),
                 body_color=APPLE_COLOR
                 ):
        super().__init__(position, body_color)
        self.position = position

    def randomize_position(self, snake_positions=None):
        """Метод случайного расположения яблока"""
        if snake_positions is None:
            snake_positions = set()
        self.position = choice(list(ALL_CELLS - set(snake_positions)))

    def draw(self):
        """Метод отрисовки яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
    return True


def main():
    """Инициализация PyGame:"""
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    # Первоначальная позиция яблока
    apple.randomize_position(snake.positions)

    running = True
    while running:
        clock.tick(SPEED)

        # Обработка пользовательского ввода
        running = handle_keys(snake)

        # Обновление направления змейки
        snake.update_direction()

        # Движение змейки
        snake.move()

        # Проверка столкновения с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Проверка столкновения с собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
        else:
            snake.cut_tail()

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
