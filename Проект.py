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
points = 0
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
            start_screen()


class Pause(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.add(stop_btn)
        self.image = pygame.Surface((60, 40))
        self.rect = pygame.Rect(580, 400, 60, 50)
        font = pygame.font.Font(None, 28)
        text = font.render('STOP', 1, (255, 255, 155))
        pygame.draw.rect(self.image, pygame.Color(11, 255, 155), (0, 0, 60, 40), 5)
        self.image.blit(text, (7, 10))

    def update(self, *args):
        global stop
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            stop = not stop



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
        global count
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            if self.number == 1:
                count = 0
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
    global key
    intro_text = ["ИГРА ТЕТРИС",
                  "Добро пожаловать в игру тетрис!",
                  "Вас ждут позитив и прекрасное времяпровождение",
                  "Цель игры:",
                  "Заполнить как можно больше горизонтальных линий на игровом ",
                  "поле, размещая опускающиеся фигуры и не оставляя пустых ",
                  "пространств между ними.",
                  "Правила: ",
                  "Вы можете передвигать фигурки вправо-влево-вниз при помощи",
                  "стелочек на клавиатуре, а так же поворачивать фигуру ",
                  "по часовой стрелке при нажатии на фигуру мышкой",
                  "(со второго уровня)",
                  "В игре накапливаются очки за каждый собранный ряд. ",
                  "Чтобы начать игры нажмите на экран или любую клавишу.",
                  "Чтобы выйти из игры нажмите на крестик или на клавишу ESC",
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
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                screen.fill((0, 0, 0))
                show_levels()
        pygame.display.flip()
        clock.tick(FPS)


class Deleter(pygame.sprite.Sprite):
    global field, updated
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface((40, 40))
        self.rect = pygame.Rect(0, 0, 40, 40)
        pygame.draw.rect(self.image, pygame.Color(0, 0, 0), (0, 0, 40, 40), 0)

    def update(self, w=11, h=12):
        for i in range(h):
            for j in range(w):
                self.rect.x = j * 40 + 10
                self.rect.y = i * 40 + 10
                if pygame.sprite.spritecollideany(self, figures):
                    field[i][j] = 1
                else:
                    field[i][j] = 0

    def check_field(self, w=11, h=12):
        global points, updated
        hor = -10
        for i in range(h):
            if field[i] == [1] * w:
                points += 100
                hor = i
                break
        if hor != -10:
            for i in range(w):
                self.rect.x = i * 40 + 10
                self.rect.y = hor * 40 + 10
                pygame.sprite.spritecollide(self, figures, True)
                field[hor][i] = 0
                updated = True

        m = []
        vert = -10
        for i in range(w):
            m = []
            for j in range(h):
                if field[j][i] == 1:
                    m.append(1)
            if m == [1] * h:
                points += 100
                vert = i
                break
        if vert != -10:
            for i in range(h):
                self.rect.x = vert * 40 + 10
                self.rect.y = i * 40 + 10
                pygame.sprite.spritecollide(self, figures, True)
                field[i][vert] = 0
                updated = True



class Figure(pygame.sprite.Sprite):
    global field
    def __init__(self, x, y, n, c):
        super().__init__(all_sprites)
        # self.add(figures)
        self.x = x
        self.y = y
        self.n = n
        self.lastx = 0
        self.lasty = 0
        self.count = c
        self.go = True
        if n == 0:
            self.image = pygame.Surface((80, 80))
            self.rect = pygame.Rect(x, y, 80, 80)
            pygame.draw.polygon(self.image, pygame.Color(choice(colors)), [(0, 0), (80, 0), (80, 80)], 0)
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
        self.check()
        if self.go:
            if flag == 1:
                self.rect.y += args[0]
            else:
                if args[0] == 'R' and self.count == args[1] and self.rect.x <= 330:
                    self.rect.x += 40
                elif args[0] == 'L' and self.count == args[1] and self.rect.x >= 40:
                    self.rect.x -= 40
                elif args[0] == 'D' and self.count == args[1]:
                    self.check()
                    if self.go:
                        if self.n == 0:
                            self.rect.y += min(40, 410 - self.rect.y)
                        elif self.n == 1:
                            self.rect.y += min(40, 330 - self.rect.y)
                        elif self.n == 2:
                            self.rect.y += min(40, 370 - self.rect.y)


    def check(self):
        if (self.n == 0 and self.rect.y == 410) or \
                (self.n == 1 and self.rect.y == 330) or \
                (self.n == 2 and self.rect.y == 370) or len(pygame.sprite.spritecollide(self, figures, False)) > 1:
            self.go = False



class Board:
    global field, points
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = field
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
    # name = get_name()
    screen.fill((0, 0, 0))
    levels.draw(screen)
    font = pygame.font.Font(None, 50)
    text = font.render('Выберете уровень', 1, (255, 255, 100))
    screen.blit(text, (30, 10))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                levels.update(event)
        pygame.display.flip()
        clock.tick(FPS)


def get_name():
    screen.fill((30, 30, 30))
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(100, 200, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    font = pygame.font.Font(None, 50)
    text = font.render('Введите имя', 1, (255, 255, 100))
    screen.blit(text, (100, 100))
    color = color_inactive
    active = False
    text = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode


        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        clock.tick(30)


v = 150
f = 0


# первый уровень
def first_run():
    new_game()
    global key, f, count, figures, board, exit_btn, deleter, del_, updated, stop
    board.render(screen)

    if count == 0:
        count += 1
        figure = Figure(10 + f * 40, 10, f % 3, count)
        figures.add(figure)
        all_sprites.add(figure)
        f = choice(range(11))
        updated = False
    while True:
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                exit_btn.update(event)
                stop_btn.update(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                figures.update(0, 'R', count)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                figures.update(0, 'L', count)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                figures.update(0, 'D', count)
            if figure.go is False or updated:
                count += 1
                figure = Figure(10 + f * 40, 10, f % 3, count)
                figures.add(figure)
                all_sprites.add(figure)
                f = choice(range(11))
                updated = False
        if not stop:
            y = v / FPS
            figures.update(1, y)
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 30)
        text = font.render('Уровень 1', 1, (255, 255, 100))
        screen.blit(text, (570, 10))
        text = font.render('Очки:', 1, (255, 255, 100))
        screen.blit(text, (570, 40))
        text = font.render(f'{points}', 1, (255, 255, 100))
        screen.blit(text, (570, 80))
        exit_btn.draw(screen)
        stop_btn.draw(screen)
        figures.draw(screen)
        deleter.update()
        del_.check_field()
        board.render(screen)
        pygame.display.flip()
        clock.tick(FPS)


# все спрайты
all_sprites = pygame.sprite.Group()
# все уровни
levels = pygame.sprite.Group()

# Создание уровней
level1 = Level(30, 80, 1)
level2 = Level(180, 80, 2)
level3 = Level(330, 80, 3)
def new_game():
    # все фигуры
    figures = pygame.sprite.Group()
    # текущая фигура
    figure = pygame.sprite.Sprite()
    # Кнопка выхода
    exit_btn = pygame.sprite.Group()
    deleter = pygame.sprite.Group()
    exit = Exit()
    exit_btn.add(exit)
    field = [[0] * 11 for _ in range(12)]
    board = Board(11, 12)
    del_ = Deleter()
    deleter.add(del_)
    all_sprites.add(exit)

# Добавление всех спрайтов


all_sprites.add(level1)
levels.add(level1)

all_sprites.add(level2)
levels.add(level2)

all_sprites.add(level3)
levels.add(level3)

#MYEVENT = 30
#pygame.time.set_timer(MYEVENT, 14940)
# все фигуры
figures = pygame.sprite.Group()
# текущая фигура
figure = pygame.sprite.Sprite()
# Кнопка выхода
exit_btn = pygame.sprite.Group()
stop_btn = pygame.sprite.Group()
deleter = pygame.sprite.Group()
exit = Exit()
exit_btn.add(exit)
stop = Pause()
stop_btn.add(stop)
stop = False
field = [[0] * 11 for _ in range(12)]
board = Board(11, 12)
del_ = Deleter()
deleter.add(del_)
all_sprites.add(exit)
# Музыка
pygame.mixer.music.load('fon.mp3')
# pygame.mixer.music.play()
running = True
start_screen()

terminate()