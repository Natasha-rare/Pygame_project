import sys
import csv
import pygame
from random import choice
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets

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


# Дизайн таблицы результатов
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(650, 433)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 630, 413))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.tableWidget.setFont(font)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Таблица результатов"))


class Results_output(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loadTable('results.csv')

    def loadTable(self, name):
        with open('results.csv', encoding='utf8') as csvfile:
            results_list = list(csv.reader(csvfile, delimiter=',', quotechar='"'))

            self.tableWidget.setColumnCount(2)
            self.tableWidget.setHorizontalHeaderLabels(['имя', 'результат'])
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(results_list):
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(elem))

        self.tableWidget.resizeColumnsToContents()


# добавление текущего результата
def results():
    global name, results_list
    with open('results.csv', encoding='utf8') as csvfile:
        results_list = list(csv.reader(csvfile, delimiter=',', quotechar='"'))

    results_list.append([name, points])
    with open('results.csv', 'w') as csvfile:
        writer = csv.writer(
            csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(results_list)):
            writer.writerow(results_list[i])


# Спрайт выхода из игры (на начальный экран)
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

# Спрайт паузы
class Pause(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.add(stop_btn)
        self.image = pygame.Surface((60, 40))
        self.rect = pygame.Rect(580, 400, 60, 50)
        font = pygame.font.Font(None, 24)
        text = font.render('STOP', 1, (255, 255, 155))
        self.image.blit(text, (6, 10))
        pygame.draw.rect(self.image, pygame.Color(11, 255, 155), (0, 0, 60, 40), 3)

    def update(self, *args):
        global stop
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            stop = not stop
            if stop is True:
                pygame.draw.rect(self.image, pygame.Color(0, 0, 0), (0, 0, 60, 40))
                font = pygame.font.Font(None, 24)
                text = font.render('START', 1, (255, 255, 155))
                self.image.blit(text, (6, 10))
                pygame.draw.rect(self.image, pygame.Color(11, 255, 155), (0, 0, 60, 40), 3)
            else:
                pygame.draw.rect(self.image, pygame.Color(0, 0, 0), (0, 0, 60, 40))
                font = pygame.font.Font(None, 24)
                text = font.render('STOP', 1, (255, 255, 155))
                self.image.blit(text, (6, 10))
                pygame.draw.rect(self.image, pygame.Color(11, 255, 155), (0, 0, 60, 40), 3)


# Спрайт уровня
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
            elif self.number == 2:
                count = 0
                second_run()
            elif self.number == 3:
                count = 0
                third_run()


# загрузка изображения
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


#завершение работы игры
def terminate():
    pygame.quit()
    sys.exit()


#Заставка с правилами игры
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
                  "по часовой стрелке при нажатии на стрелку вверх",
                  "(со второго уровня)",
                  "В игре накапливаются очки за каждый собранный нижний ряд. ",
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
                name = ''
                show_levels()
        pygame.display.flip()
        clock.tick(FPS)


# Одиночный спрайт. Используется при создании фигур
class Alone(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__(all_sprites)
        self.add(alone)
        self.image = pygame.Surface((40, 40))
        self.rect = pygame.Rect(x, y, 40, 40)
        pygame.draw.rect(self.image, pygame.Color(color), (0, 0, 80, 80), 0)


SQUARE = [[1, 1], [1, 1]]
TOWER = [[[1, 1, 1, 1]], [[1], [1], [1], [1]]]
THIRD = [[[1, 1], [0, 1, 1]], [[0, 1], [1, 1], [1]]]
L = [[[1], [1, 1, 1]], [[0, 1], [0, 1], [1, 1]], [[1, 1], [1, 0], [1, 0]], [[1, 1, 1], [0, 0, 1]]]
FIGURES = [SQUARE, TOWER, L, THIRD]


class Figure(pygame.sprite.Sprite):
    global field

    def __init__(self, x, y, n, c):
        super().__init__(all_sprites)
        self.f = FIGURES[n]
        if self.f == L:
            self.f = L[0]
        elif self.f == TOWER:
            self.f = TOWER[0]
        elif self.f == THIRD:
            self.f = THIRD[0]
        self.count = c
        self.clr = choice(colors)
        self.go = True
        self.rect = pygame.Rect(x, y, 40 * len(self.f), 40 * max(list(map(lambda x: len(x), self.f))))
        self.figure = pygame.sprite.Group()
        for i in range(len(self.f)):
            for j in range(len(self.f[i])):
                try:
                    if self.f[i][j] == 1:
                        field[(y - 10) // 40 + j][(x - 10) // 40 + i] = 1
                        self.figure.add(Alone(x + 40 * i, y + 40 * j, self.clr))
                except IndexError:
                    print('adadadaa')
                    break
                # alone.add(Alone(x + 40 * i, y + 40 * j, clr))

    def draw(self):
        self.figure.draw(screen)

    def update(self, flag, *args):
        self.check()
        c = len(self.figure.sprites())
        x = (self.rect.x - 10) // 40
        y = (self.rect.y - 10) // 40
        if flag == 4:
            for i in self.figure.sprites():
                if i.rect.y == 11:
                    self.figure.remove(i)
            c = len(self.figure.sprites())
            if c > 0:
                for i in range(c - 1, -1, -1):
                    x1, y1 = (self.figure.sprites()[i].rect.x - 10) // 40, (self.figure.sprites()[i].rect.y - 10) // 40
                    field[y1][x1] = 0
                    self.figure.sprites()[i].rect.y += 40
                    y2 = (self.figure.sprites()[i].rect.y - 10) // 40
                    if y2 > 11:
                        self.figure.remove(self.figure.sprites()[i])
                    else:
                        field[y2][x1] = 1
                self.rect.y += 40
        if self.go:
            if flag == 1:
                delta = min(args[0], 410 - self.rect.y)
                for i in range(c - 1, -1, -1):
                    x1, y1 = (self.figure.sprites()[i].rect.x - 10) // 40, (self.figure.sprites()[i].rect.y - 10) // 40
                    field[y1][x1] = 0
                    self.figure.sprites()[i].rect.y += delta
                    y2 = (self.figure.sprites()[i].rect.y - 10) // 40
                    field[y2][x1] = 1
                self.rect.y += delta
            elif flag == 0:
                if args[0] == 'R' and self.count == args[1] and self.rect.x <= (410 - self.rect.width):
                    r = True
                    for i in range(y, y + self.rect.height // 40):
                        if field[i][x + self.rect.width // 40] == 1:
                            r = False
                    if r:
                        for i in range(c - 1, -1, -1):
                            x1, y1 = (self.figure.sprites()[i].rect.x - 10) // 40, (
                                        self.figure.sprites()[i].rect.y - 10) // 40
                            field[y1][x1] = 0
                            self.figure.sprites()[i].rect.x += 40
                            x2 = (self.figure.sprites()[i].rect.x - 10) // 40
                            field[y1][x2] = 1
                        self.rect.x += 40
                elif args[0] == 'L' and self.count == args[1] and self.rect.x >= 40:
                    l = True
                    for i in range(y - 1, y + self.rect.height // 40):
                        if field[i][x - 1] == 1:
                            l = False
                    if l:
                        for i in range(c):
                            x1, y1 = (self.figure.sprites()[i].rect.x - 10) // 40, (
                                        self.figure.sprites()[i].rect.y - 10) // 40
                            field[y1][x1] = 0
                            self.figure.sprites()[i].rect.x -= 40
                            x2 = (self.figure.sprites()[i].rect.x - 10) // 40
                            field[y1][x2] = 1
                        self.rect.x -= 40

                elif args[0] == 'U' and self.count == args[1] and self.rect.x >= 40:
                    if self.f not in SQUARE:
                        for i in range(4):
                            alone.remove(alone.sprites()[:-1])
                        for i in range(len(self.f)):
                            for j in range(len(self.f[i])):
                                field[y + j][x + i] = 0

                        if self.f in L:
                            if L.index(self.f) == 3:
                                self.f = L[0]
                            else:
                                self.f = L[L.index(self.f) + 1]
                        elif self.f in TOWER:
                            self.f = TOWER[0] if TOWER.index(self.f) == 1 else TOWER[1]
                        elif self.f in THIRD:
                            self.f = THIRD[0] if THIRD.index(self.f) == 1 else THIRD[1]
                        if max([len(x) for x in self.f]) * 40 + self.rect.x < 410:
                            self.rect = pygame.Rect(self.rect.x, self.rect.y, 40 * len(self.f),
                                                    40 * max(list(map(lambda x: len(x), self.f))))
                            self.figure = pygame.sprite.Group()
                            for i in range(len(self.f)):
                                for j in range(len(self.f[i])):
                                    if self.f[i][j] == 1:
                                        field[y + j][x + i] = 1
                                        self.figure.add(Alone(self.rect.x + 40 * i, self.rect.y + 40 * j, self.clr))
                elif args[0] == 'D' and self.count == args[1]:  # and field[x][y + self.rect.height // 40 + 1] == 0:
                    for i in range(c - 1, -1, -1):
                        x1, y1 = (self.figure.sprites()[i].rect.x - 10) // 40, \
                                 (self.figure.sprites()[i].rect.y - 10) // 40
                        field[y1][x1] = 0
                        self.figure.sprites()[i].rect.y += self.delta
                        y2 = (self.figure.sprites()[i].rect.y - 10) // 40
                        field[y2][x1] = 1
                    self.rect.y += self.delta

    def check(self):
        self.delta = 0
        x = (self.rect.x - 10) // 40
        y = (self.rect.y - 10) // 40
        for i in range(y + self.rect.height // 40, 12):
            if field[i][x] == 0:
                self.delta += 40
            else:
                break
        self.delta = min(40, self.delta, 490 - self.rect.y - self.rect.height)
        if self.delta == 0 or pygame.sprite.spritecollideany(self, border):
            self.go = False


# Нижняя граница
class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, ):
        super().__init__(all_sprites)
        # нижняя стенка
        # self.add(border)
        self.image = pygame.Surface([400, 1])
        self.rect = pygame.Rect(10, 489, 400, 1)


# Поле
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


# Работа с результатами. Их вывод
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
            app = QApplication(sys.argv)
            base = Results_output()
            base.show()


# Запрос имени пользователя с помощью перехода на отдельное окно
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
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 3))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        clock.tick(30)


# Следующий за заставкой экран с уровнями
def show_levels():
    global name
    screen.fill((0, 0, 0))
    levels.draw(screen)
    font = pygame.font.Font(None, 50)
    text = font.render('Выберете уровень', 1, (255, 255, 100))
    screen.blit(text, (30, 10))
    text = font.render('Ввести имя', 1, (255, 255, 100))
    screen.blit(text, (100, 425))
    input_box = pygame.Rect(100, 400, 300, 60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                exit_btn.update(event)
                levels.update(event)
                res.update(event)
                if input_box.collidepoint(event.pos):
                    name = get_name()
        screen.fill((0, 0, 0))
        exit_btn.draw(screen)
        res.draw(screen)
        levels.draw(screen)
        text = font.render('Ввести имя', 1, (255, 255, 100))
        screen.blit(text, (100, 425))
        font = pygame.font.Font(None, 50)
        text = font.render('Выберете уровень', 1, (255, 255, 100))
        screen.blit(text, (30, 10))
        pygame.draw.rect(screen, (255, 255, 100), input_box, 2)

        pygame.display.flip()
        clock.tick(FPS)


v = 150
f = 0


# Проверка заполненности поля
def field_check():
    global updated, points
    if 0 not in field[-1]:
        field[-1] = [0] * 11
        updated = True
        points += 100
    if field[0].count(1) >= 9 or field[1].count(1) >= 9:
        congratulate(-1)


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
                for i in field:
                    print(i)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                for i in figures:
                    i.update(0, 'R', count)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                for i in figures:
                    i.update(0, 'L', count)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                for i in figures:
                    i.update(0, 'D', count)
        # Если не была нажата клавиша стоп
        if not stop:
            if figures[-1].go is False or updated:
                count += 1
                figures.append(Figure(10 + f * 40, 10, f % 3, count))
                all_sprites.add(Figure(10 + f * 40, 10, f % 3, count))
                f = choice(range(11))
                updated = False
            y = v / FPS
            for i in figures:
                i.update(1, y)
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
        for i in figures:
            i.draw()
        field_check()
        if updated:
            for i in figures:
                i.update(4)
        if points == 200:
            count = 0
            congratulate(1)
        board.render(screen)
        pygame.display.flip()
        clock.tick(FPS)


# Второй уровень
def second_run():
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                for i in figures:
                    i.update(0, 'U', count)
        # Если не была нажата клавиша стоп
        if not stop:
            if figures[-1].go is False or updated:
                count += 1
                figures.append(Figure(10 + f * 40, 10, f % 3, count))
                all_sprites.add(Figure(10 + f * 40, 10, f % 3, count))
                f = choice(range(11))
                updated = False
            y = (v * 2) / FPS
            for i in figures:
                i.update(1, y)
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 30)
        text = font.render('Уровень 2', 1, (255, 255, 100))
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
        field_check()
        if updated:
            for i in figures:
                i.update(4)
        if points == 400:
            count = 0
            congratulate(2)
        board.render(screen)
        pygame.display.flip()
        clock.tick(FPS + 50)


# Третий уровень
def third_run():
    new_game()
    global key, f, count, figures, board, exit_btn, deleter, del_, updated, stop
    board.render(screen)
    if count == 0:
        count += 1
        m = choice(range(4))
        figures.append(Figure(10 + f * 40, 10, m, count))
        all_sprites.add(Figure(10 + f * 40, 10, m, count))
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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                for i in figures:
                    i.update(0, 'U', count)
        # Если не была нажата клавиша стоп
        if not stop:
            if figures[-1].go is False or updated:
                count += 1
                m = choice(range(4))
                figures.append(Figure(10 + f * 40, 10, m, count))
                all_sprites.add(Figure(10 + f * 40, 10, m, count))
                f = choice(range(11))
                updated = False
            y = (v * 3) / FPS
            for i in figures:
                i.update(1, y)
            # figures.update(1, y)
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 30)
        text = font.render('Уровень 3', 1, (255, 255, 100))
        screen.blit(text, (570, 10))
        text = font.render('Очки:', 1, (255, 255, 100))
        screen.blit(text, (570, 40))
        text = font.render(f'{points}', 1, (255, 255, 100))
        screen.blit(text, (570, 80))
        border.draw(screen)
        exit_btn.draw(screen)
        stop_btn.draw(screen)
        for i in figures:
            i.draw()
        field_check()
        if updated:
            for i in figures:
                i.update(4)
        if points == 900:
            congratulate(10)
        board.render(screen)
        pygame.display.flip()
        clock.tick(FPS + 70)


# Украшение -- звездочки
class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.add(stars)
        self.image = choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 1

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 20
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, choice(numbers), choice(numbers))


# Поздравление с победой/ переходом на следующий уровень
def congratulate(n):
    screen.fill((0, 0, 0))
    running = True

    create_particles((100, 100))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # создаём частицы по щелчку мыши
                create_particles(pygame.mouse.get_pos())
            if event.type == pygame.KEYDOWN:
                if n == 2:
                    third_run()
                elif n == 1:
                    second_run()
                else:
                    start_screen()
        stars.update()
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        if n == -1:
            t = font.render('К сожалению вы проиграли', 1, (255, 255, 100))
            screen.blit(t, (100, 100))
            t = font.render(f'Вы набрали {points} очков', 1, (255, 255, 100))
            screen.blit(t, (100, 200))
            for i in range(len(results_list)):
                k = results_list[i]
                if name in k:
                    results_list[i] = name, points
        elif n == 10:
            t = font.render('Поздравляем с победой!', 1, (255, 255, 100))
            screen.blit(t, (100, 100))
        else:
            t = font.render(f'Вы прошли уровень {n}', 1, (255, 255, 100))
            screen.blit(t, (100, 100))

        font = pygame.font.Font(None, 20)
        t = font.render('Нажмите на клавиатуру для продолжения', 1, (255, 255, 100))
        screen.blit(t, (100, 400))
        stars.draw(screen)
        pygame.display.flip()
        clock.tick(50)


# все спрайты
all_sprites = pygame.sprite.Group()
# все уровни
levels = pygame.sprite.Group()
# Звездочки
stars = pygame.sprite.Group()
# Создание уровней
level1 = Level(30, 80, 1)
level2 = Level(180, 80, 2)
level3 = Level(330, 80, 3)


# Начало нового уровня
def new_game():
    global points, field, figures, stop
    stop = False
    # все фигуры
    figures = []
    # Кнопка выхода
    exit_btn = pygame.sprite.Group()
    exit = Exit()
    exit_btn.add(exit)
    field = [[0] * 11 for _ in range(12)]
    all_sprites.add(exit)


screen_rect = (0, 0, WIDTH, HEIGHT)
# Добавление всех спрайтов
all_sprites.add(level1)
levels.add(level1)

all_sprites.add(level2)
levels.add(level2)

all_sprites.add(level3)
levels.add(level3)
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
field = [[0] * 12 for _ in range(11)]
board = Board(11, 12)
all_sprites.add(exit)
# Музыка
pygame.mixer.music.load('fon.mp3')
pygame.mixer.music.play()
running = True
start_screen()

terminate()