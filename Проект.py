import os
import sys
import pygame
from random import choice

pygame.init()
pygame.key.set_repeat(200, 70)
FPS = 60
WIDTH = 700
HEIGHT = 600
STEP = 10

colors = ['blue', 'red', 'green', 'yellow', 'orange']

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Exit(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.add(exit_btn)
        self.image = pygame.Surface((60, 40))
        self.rect = pygame.Rect(580, 500, 60, 50)
        font = pygame.font.Font(None, 30)
        text = font.render('EXIT', 1, (11, 255, 155))
        pygame.draw.rect(self.image, pygame.Color(11, 255, 155), (0, 0, 60, 40), 5)
        self.image.blit(text, (7, 10))

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            screen.fill((0, 0, 0))
            show_levels()


class Level(pygame.sprite.Sprite):
    def __init__(self, x, y, n):
        super().__init__(all_sprites)
        self.add(levels)
        self.x = x
        self.y = y
        self.image = pygame.Surface((80, 80))
        self.rect = pygame.Rect(x, y, 80, 80)
        font = pygame.font.Font(None, 50)
        text = font.render(str(n), 1, (255, 0, 100))
        self.number = n
        pygame.draw.rect(self.image, pygame.Color("blue"), (0, 0, 80, 80), 10)
        self.image.blit(text, (30, 30))

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            if self.number == 1:
                first_run()


def load_image(name, color_key=None):
    try:
        image = pygame.image.load(name)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ИГРА ТЕТРИС",
                  "Добро пожаловать в игру тетрис!",
                  "Вас ждут позитив и прекрасное времяпровождение",
                  "Цель игры:",
                  "заполнить как можно больше горизонтальных линий на игровом ",
                  "поле, размещая опускающиеся фигуры и не оставляя пустых ",
                  "пространств между ними.",
                  "Правила: ",
                  "Вы можете передвигать фигурки вправо-влево при помощи",
                  "стелочек на клавиатуре, а так же поворачивать фигуру ",
                  "по часовой стрелке при нажатии на фигуру мышкой",
                  "(со второго уровня)",
                  "В игре накапливаются ",
                  "очки за каждый ",
                  "собранный ряд.",
                  "Желаю удачи ^.^"]

    fon = pygame.transform.scale(load_image('tetris.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 28)
    text_coord = 20
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                screen.fill((0, 0, 0))
                show_levels()
        pygame.display.flip()
        clock.tick(FPS)

class Figure(pygame.sprite.Sprite):
    def __init__(self, x, y, n):
        super().__init__(all_sprites)
        # self.add(figures)
        self.x = x
        self.y = y
        self.n = n
        self.go = True
        if n == 0:
            self.image = pygame.Surface((80, 80))
            self.rect = pygame.Rect(x, y, 80, 80)
            pygame.draw.rect(self.image, pygame.Color(choice(colors)), (0, 0, 80, 80), 0)
        elif n == 1:
            self.image = pygame.Surface((40, 160))
            self.rect = pygame.Rect(x, y, 40, 160)
            pygame.draw.rect(self.image, pygame.Color(choice(colors)), (0, 0, 40, 160), 0)
        elif n == 2:
            self.image = pygame.Surface((80, 120))
            self.rect = pygame.Rect(x, y, 80, 120)
            pygame.draw.polygon(self.image, pygame.Color(choice(colors)), [(0, 0),
                                                                           (40, 0), (40, 80), (80, 80),
                                                                           (80, 120), (0, 120)], 0)

    def update(self, flag, *args):
        if (self.n == 0 and self.rect.y == 410) or \
                (self.n == 1 and self.rect.y == 330) or \
                (self.n == 2 and self.rect.y == 370):
            self.go = False
        if self.go:
            if flag == 1:
                self.rect.y += args[0]
            else:
                if args and args[0].type == key[pygame.K_RIGHT]:
                    self.rect.x += 40



class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 40

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, (255, 255, 255),
                                 [self.left + self.cell_size * j, self.top + self.cell_size * i,
                                                           self.cell_size, self.cell_size], 2)

def show_levels():
    levels.draw(screen)
    font = pygame.font.Font(None, 50)
    text = font.render('Выберете уровень', 1, (255, 255, 100))
    screen.blit(text, (30, 10))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                levels.update(event)
        pygame.display.flip()
        clock.tick(FPS)


#def run_level(level):
    #screen.fill((0, 0, 0))
    #board.render(screen)
    #font = pygame.font.Font(None, 30)
    #text = font.render(f'Уровень {level}', 1, (255, 255, 100))
    #screen.blit(text, (570, 10))
    #exit_btn.draw(screen)
    #while True:
    #    for event in pygame.event.get():
    #        if event.type == pygame.QUIT:
    #            terminate()
    #        if event.type == pygame.MOUSEBUTTONDOWN:
    #            exit_btn.update(event)
    #    if level == 1:
    #       first_run()
    #    pygame.display.flip()
    #    clock.tick(FPS)


v = 100
f = 0
# первый уровень
def first_run():
    board.render(screen)
    global key, f
    while True:
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                exit_btn.update(event)
            if event.type == pygame.KEYDOWN:
                figures.update(0, event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                figures.add(Figure(10 + f * 40, 10, f % 3))
                all_sprites.add(Figure(10 + f * 40, 10, f % 3))
                f = choice(range(11))
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 30)
        text = font.render(f'Уровень 1', 1, (255, 255, 100))
        screen.blit(text, (570, 10))
        exit_btn.draw(screen)
        figures.draw(screen)
        y = v / FPS
        figures.update(1, y)
        board.render(screen)
        pygame.display.flip()
        clock.tick(FPS)


all_sprites = pygame.sprite.Group()
levels = pygame.sprite.Group()
figures = pygame.sprite.Group()
exit_btn = pygame.sprite.Group()
level1 = Level(30, 80, 1)
level2 = Level(180, 80, 2)
level3 = Level(330, 80, 3)
exit = Exit()
exit_btn.add(exit)
all_sprites.add(exit)
all_sprites.add(level1)
levels.add(level1)
all_sprites.add(level2)
levels.add(level2)
all_sprites.add(level3)
levels.add(level3)
board = Board(11, 12)
pygame.mixer.music.load('fon.mp3')
pygame.mixer.music.play()
running = True
start_screen()

terminate()