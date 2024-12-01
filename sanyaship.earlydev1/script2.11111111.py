import pygame
import sys
import random

# Настройки
CELL_SIZE = 96  # Размер квадрата (текстура)
GRID_WIDTH = 20  # Ширина сетки (в клетках)
GRID_HEIGHT = 20  # Высота сетки (в клетках)
FPS = 30  # Фреймы в секунду

# Настройки окна (должны быть нечетными)
DISPLAY_WIDTH = 7  # Ширина отображения (в клетках)
DISPLAY_HEIGHT = 7  # Высота отображения (в клетках)

# Проверка на нечётность
if DISPLAY_WIDTH % 2 == 0:
    DISPLAY_WIDTH += 1
if DISPLAY_HEIGHT % 2 == 0:
    DISPLAY_HEIGHT += 1

cucle=1
message_time=20

# Инициализация Pygame
pygame.init()

# Настройка окна
screen_width = CELL_SIZE * DISPLAY_WIDTH  # Ширина окна для отображения
screen_height = CELL_SIZE * DISPLAY_HEIGHT  # Высота окна для отображения
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Саня на лодке")

# Загрузка текстур
try:
    water_texture = pygame.image.load('water_block1.png')  # Путь к текстуре воды
    water_texture = pygame.transform.scale(water_texture, (CELL_SIZE, CELL_SIZE))

    player_texture = pygame.image.load('sanya.gif')  # Путь к текстуре игрока
    player_texture = pygame.transform.scale(player_texture, (CELL_SIZE, CELL_SIZE))

    object_texture = pygame.image.load('bottle.png')  # Путь к текстуре объекта
    object_texture = pygame.transform.scale(object_texture, (CELL_SIZE, CELL_SIZE))

    highlight_texture = pygame.image.load('light.png')  # Путь к текстуре подсветки
    highlight_texture = pygame.transform.scale(highlight_texture, (CELL_SIZE, CELL_SIZE))
except pygame.error as e:
    print(f"Ошибка при загрузке изображения: {e}")
    pygame.quit()
    sys.exit()

# Начальная позиция игрока (центр экрана)
player_x = GRID_WIDTH // 2
player_y = GRID_HEIGHT // 2

# Генерация бутылок на случайных клетках
def generate_bottles(num):
    bottles = []
    for _ in range(num):  # Создать указанное количество бутылок
        while True:
            obj_x = random.randint(0, GRID_WIDTH - 1)
            obj_y = random.randint(0, GRID_HEIGHT - 1)
            if (obj_x, obj_y) not in bottles and (obj_x, obj_y) != (player_x, player_y):
                bottles.append((obj_x, obj_y))
                break
    return bottles

# Начальное количество бутылок
bottle_count = 10
objects = generate_bottles(bottle_count)

# Счётчик собранных бутылок
score = 0
message = ""
message_timer = 0

# Главный игровой цикл
clock = pygame.time.Clock()
while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Обработка нажатий клавиш для движения игрока
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and player_y > 0:
                player_y -= 1
            if event.key == pygame.K_DOWN and player_y < GRID_HEIGHT - 1:
                player_y += 1
            if event.key == pygame.K_LEFT and player_x > 0:
                player_x -= 1
            if event.key == pygame.K_RIGHT and player_x < GRID_WIDTH - 1:
                player_x += 1

    # Проверка на столкновения с бутылками
    collision = False
    for obj_x, obj_y in objects[:]:  # Проходим по копии списка, чтобы безопасно изменять его
        if player_x == obj_x and player_y == obj_y:
            collision = True
            objects.remove((obj_x, obj_y))  # Удаляем бутылку
            score += 1  # Увеличиваем счётчик собранных бутылок
            message = "Кафе у Ирины закрыто!"  # Устанавливаем сообщение
            message_timer = message_time  # Устанавливаем таймер на 1 секунду (60 кадров)

    # Проверяем, если все бутылки собраны
    if not objects:
        objects = generate_bottles(bottle_count)  # Генерируем новые бутылки
        message = "Кафе у Ирины открыто!"  # Устанавливаем другое сообщение
        message_timer = message_time  # Устанавливаем таймер на 1 секунду (60 кадров)
        cucle+=1
        
    # Уменьшаем таймер сообщения
    if message_timer > 0:
        message_timer -= 1

    # Рассчитываем офсет для камеры
    camera_x = player_x - DISPLAY_WIDTH // 2
    camera_y = player_y - DISPLAY_HEIGHT // 2

    # Ограничение камеры, чтобы не выходить за границы сетки
    camera_x = max(0, min(camera_x, GRID_WIDTH - DISPLAY_WIDTH))
    camera_y = max(0, min(camera_y, GRID_HEIGHT - DISPLAY_HEIGHT))

    # Отрисовка сетки с учетом офсета
    screen.fill((0, 0, 0))  # Очистить экран черным цветом

    # Отрисовка воды
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            screen.blit(water_texture, (col * CELL_SIZE - camera_x * CELL_SIZE, row * CELL_SIZE - camera_y * CELL_SIZE))

    # Отрисовка объектов (бутылок)
    for obj_x, obj_y in objects:
        if camera_x <= obj_x < camera_x + DISPLAY_WIDTH and camera_y <= obj_y < camera_y + DISPLAY_HEIGHT:
            screen.blit(object_texture, ((obj_x - camera_x) * CELL_SIZE, (obj_y - camera_y) * CELL_SIZE))

    # Отрисовка игрока
    screen.blit(player_texture, ((player_x - camera_x) * CELL_SIZE, (player_y - camera_y) * CELL_SIZE))

    if objects:
        closest_bottle = min(objects, key=lambda obj: (obj[0] - player_x) ** 2 + (obj[1] - player_y) ** 2)
        triangle_points = [
            (screen_width // 2, screen_height // 2),  # Вершина треугольника в центре
            (screen_width // 2 + (closest_bottle[0] - player_x) * CELL_SIZE // 2, screen_height // 2 + (closest_bottle[1] - player_y) * CELL_SIZE // 2),  # Правый нижний угол
            (screen_width // 2 + (closest_bottle[0] - player_x) * CELL_SIZE // 2, screen_height // 2 + (closest_bottle[1] - player_y) * CELL_SIZE // 2)  # Левый нижний угол
        ]
        pygame.draw.polygon(screen, (255, 0, 0), triangle_points)  # Рисуем треугольник

    # Подсветка области вокруг игрока (3x3)
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            highlight_x = (player_x + dx - camera_x) * CELL_SIZE
            highlight_y = (player_y + dy - camera_y) * CELL_SIZE
            screen.blit(highlight_texture, (highlight_x, highlight_y))  # Отрисовка текстуры подсветки

    # Отображение счётчика
    font = pygame.font.Font(None, 36)
    score_surface = font.render(f"Собрано бутылок: {score}/{10*cucle}", True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))


    # Отображение сообщения, если оно активно
    if message_timer > 0:
        message_surface = font.render(message, True, (255, 255, 0))  # Желтый цвет для сообщения
        screen.blit(message_surface, (screen_width // 2 - message_surface.get_width() // 2, screen_height // 2))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)
