import sys
import csv
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
results_list = []
def results():
    global name
    with open('results.csv', encoding='utf8') as csvfile:
        results_list = list(csv.reader(csvfile, delimiter=',', quotechar='"'))

    results_list.append([name, points])
    with open('results.csv', 'w') as csvfile:
        writer = csv.writer(
            csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(results_list)):
            writer.writerow(results_list[i])



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
            results()
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
        global name
        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                screen.fill((0, 0, 0))
                name = get_name()
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
                if pygame.sprite.spritecollideany(self, alone):
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
                pygame.sprite.spritecollide(self, alone, True)
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
                if pygame.sprite.spritecollideany(self, alone):
                    print(pygame.sprite.spritecollide(self, alone, False))
                pygame.sprite.spritecollide(self, alone, True)
                field[i][vert] = 0
                updated = True


class Alone(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__(all_sprites)
        self.add(alone)
        self.image = pygame.Surface((40, 40))
        self.rect = pygame.Rect(x, y, 40, 40)
        pygame.draw.rect(self.image, pygame.Color(color), (0, 0, 80, 80), 0)


SQUARE = [[1, 1], [1, 1]]
TOWER = [[1, 1, 1, 1]]
L = [[1], [1, 1, 1]]
FIGURES = [SQUARE, TOWER, L]


class Figure(pygame.sprite.Sprite):
    global field
    def __init__(self, x, y, n, c):
        super().__init__(all_sprites)
        # self.add(figures)
        #self.x = x
        #self.y = y
        self.f = FIGURES[n]
        self.lastx = 0
        self.lasty = 0
        self.count = c
        clr = choice(colors)
        self.go = True
        self.rect = pygame.Rect(x, y, 40 * len(self.f), 40 * max(list(map(lambda x: len(x), self.f))))

        print(self.f, clr)
        self.figure = pygame.sprite.Group()
        for i in range(len(self.f)):
            for j in range(len(self.f[i])):
                self.figure.add(Alone(x + 40 * i, y + 40 * j, clr))
                # alone.add(Alone(x + 40 * i, y + 40 * j, clr))

    def draw(self):
        self.figure.draw(screen)

    def update(self, flag, *args):
        self.check()
        c = len(self.figure.sprites())
        if self.go:
            if flag == 1:
                delta = min(args[0], self.delta, 410 - self.rect.y)
                for i in range(c):
                    self.figure.sprites()[i].rect.y += delta
                self.rect.y += delta
            elif flag == 0:
                if args[0] == 'R' and self.count == args[1] and self.rect.x <= (410 - self.rect.width):
                    self.rect.x += 40
                    for i in range(c):
                        self.figure.sprites()[i].rect.x += 40
                elif args[0] == 'L' and self.count == args[1] and self.rect.x >= 40:
                    self.rect.x -= 40
                    for i in range(c):
                        self.figure.sprites()[i].rect.x -= 40
                elif args[0] == 'D' and self.count == args[1]:
                    #self.check()
                    #if self.go:
                    for i in range(c):
                        self.figure.sprites()[i].rect.y += self.delta
                    self.rect.y += self.delta



    def check(self):
        self.delta = 0
        if self.go:
            for i in range(self.rect.y, 490 - self.rect.height):
                print(pygame.sprite.spritecollide(self, figures, False)[0].rect.y, self.rect.y + self.rect.height)
                if len(pygame.sprite.spritecollide(self, figures, False)) != 1 and i == pygame.sprite.spritecollide(self, figures, False)[-1].rect.y:
                    self.delta = pygame.sprite.spritecollide(self, figures, False)[0].rect.y - self.rect.y - self.rect.height
                    break
                else:
                    self.delta = i
            if self.delta > 0:
                self.delta = min(40, self.delta, 490 - self.rect.y - self.rect.height)
            elif self.delta == -2:
                self.delta = 0
            if pygame.sprite.spritecollideany(self, border) or self.delta == 0:
                self.go = False


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self,):
        super().__init__(all_sprites)
         # нижняя стенка
        #self.add(border)
        self.image = pygame.Surface([400, 1])
        self.rect = pygame.Rect(10, 489, 400, 1)


class Board:
    global field, points
    # создание поля
    def __init__(self, width, height, size=40):
        self.width = width
        self.height = height
        self.board = field
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = size

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


class Results(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface((100, 50))
        self.rect = pygame.Rect(580, 400, 100, 50)
        font = pygame.font.Font(None, 28)
        text = font.render('Results', 1, (255, 255, 155))
        pygame.draw.rect(self.image, pygame.Color(11, 255, 155), (0, 0, 100, 50), 5)
        self.image.blit(text, (10, 15))

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            screen.fill((0, 0, 0))
            pygame.draw.rect(screen, (255, 255, 255), [50, 30, 100, 40], 2)
            pygame.draw.rect(screen, (255, 255, 255), [150, 30, 100, 40], 2)
            pygame.draw.rect(screen, (255, 255, 255), [250, 30, 100, 40], 2)
            font = pygame.font.Font(None, 20)
            text = font.render('имя', 1, (255, 255, 100))
            screen.blit(text, (155, 35))
            text = font.render('баллы', 1, (255, 255, 100))
            screen.blit(text, (255, 35))
            with open('results.csv', encoding='utf8') as csvfile:
                results_list = list(csv.reader(csvfile, delimiter=',', quotechar='"'))
            for i, elem in enumerate(results_list):
                pygame.draw.rect(screen, (255, 255, 255), [50, (i + 1) * 40 + 30, 100, 40], 2)
                pygame.draw.rect(screen, (255, 255, 255), [150, (i + 1) * 40 + 30, 100, 40], 2)
                pygame.draw.rect(screen, (255, 255, 255), [250, (i + 1) * 40 + 30, 100, 40], 2)

                text = font.render(f'{i}', 1, (255, 255, 100))
                screen.blit(text, (55, (1 + i) * 40 + 15))
                text = font.render(f'{elem[0]}', 1, (255, 255, 100))
                screen.blit(text, (155, (1 + i) * 40 + 15))
                text = font.render(f'{elem[1]}', 1, (255, 255, 100))
                screen.blit(text, (255, (1 + i) * 40 + 15))



def show_levels():
    print(name)
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
                exit_btn.update(event)
                levels.update(event)
                res.update(event)
        exit_btn.draw(screen)
        res.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def get_name():
    screen.fill((30, 30, 30))
    text = ''
    font = pygame.font.Font(None, 32)
    input_box = pygame.Rect(100, 200, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    active = False
    color = color_inactive
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
        screen.fill((30, 30, 30))

        font = pygame.font.Font(None, 50)
        t = font.render('Введите имя', 1, (255, 255, 100))
        screen.blit(t, (100, 100))


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
        figures.append(Figure(10 + f * 40, 10, f % 3, count))
        all_sprites.add(Figure(10 + f * 40, 10, f % 3, count))
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
                for i in figures:
                    i.update(0, 'R', count)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                for i in figures:
                    i.update(0, 'L', count)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                for i in figures:
                    i.update(0, 'D', count)

        if not stop:
            if figures[-1].go is False or updated:
                count += 1
                figures.append(Figure(10 + f * 40, 10, f % 3, count))
                all_sprites.add(Figure(10 + f * 40, 10, f % 3, count))
                f = choice(range(11))
                updated = False
            y = v / FPS
            for i in field:
                print(i)
            for i in figures:
                i.update(1, y)
            #figures.update(1, y)
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 30)
        text = font.render('Уровень 1', 1, (255, 255, 100))
        screen.blit(text, (570, 10))
        text = font.render('Очки:', 1, (255, 255, 100))
        screen.blit(text, (570, 40))
        text = font.render(f'{points}', 1, (255, 255, 100))
        screen.blit(text, (570, 80))
        border.draw(screen)
        exit_btn.draw(screen)
        stop_btn.draw(screen)
        # figures.draw(screen)
        for i in figures:
            i.draw()
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
    global points, field, figures
    # все фигуры
    figures = []
    # Кнопка выхода
    exit_btn = pygame.sprite.Group()
    deleter = pygame.sprite.Group()
    exit = Exit()
    exit_btn.add(exit)
    field = [[0] * 11 for _ in range(12)]
    points = 0
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
name = ''
#MYEVENT = 30
#pygame.time.set_timer(MYEVENT, 14940)
# все фигуры
figures = []
alone = pygame.sprite.Group()
# Кнопка выхода
exit_btn = pygame.sprite.Group()
stop_btn = pygame.sprite.Group()
deleter = pygame.sprite.Group()
border = pygame.sprite.Group()
res = pygame.sprite.Group()
res.add(Results())
border.add(Border())
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