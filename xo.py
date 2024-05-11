from pygame import *
from random import randint, choice


class Button:
    def __init__(self, width, height, x, y, fill_color):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.fill_color = fill_color

        self.create_button()

    def create_button(self):
        #  Рисует кнопку
        draw.rect(scene, self.fill_color, (self.x, self.y, self.width, self.height))


class Label:
    def __init__(self, x, y, font_size, text_color, text):
        self.x = x
        self.y = y
        self.font_size = font_size
        self.text = text
        self.text_color = text_color
        self.draw_text()

    def setText(self):
        # Возвращает объект текста
        return font.Font(None, self.font_size).render(self.text, True, self.text_color)

    def draw_text(self):
        text = self.setText()
        width_text = text.get_width()  # Ширина текста
        height_text = text.get_height()  # Высота текста
        # Отрисовка текста
        scene.blit(text, (self.x - width_text // 2, self.y - height_text // 2))


def draw_grid(offset=0):
    for i in range(size_board - 1):
        # Рисует горизонтальную линию
        draw.line(scene, BLACK, (margin, margin + offset + size_cell + size_cell * i - 1),
                  (margin + size_cell * size_board, margin + offset + size_cell + size_cell * i - 1), 2)
        # Рисует вертикальную линию
        draw.line(scene, BLACK, (margin + size_cell + size_cell * i - 1, margin + offset),
                  (margin + size_cell + size_cell * i - 1, margin + offset + size_cell * size_board), 2)


def create_but(width, height, start_coord):
    return Button(width, height, start_coord[0], start_coord[1], BLACK)


def draw_img_player(coord_cell):
    queue_player = queue[queue_pos]
    if queue_player:
        scene.blit(img_X, (
            (margin + 10) + ((coord_cell[0] - 1) * size_cell), (margin + 110) + ((coord_cell[1] - 1) * size_cell)))
    else:
        scene.blit(img_O, (
            (margin + 10) + ((coord_cell[0] - 1) * size_cell), (margin + 110) + ((coord_cell[1] - 1) * size_cell)))


def draw_up_info():
    draw.rect(scene, WHITE, (0, 0, 500, 100))
    Label(size[0] // 4, 25, 40, BLACK, f"Человек: {players[player]}")
    Label(size[0] // 4 * 3, 25, 40, BLACK, f"Компьютер: {players[computer]}")
    Label(size[0] // 2, 75, 35, BLACK, f"Ход {players[queue[queue_pos]]}")


def hide_button():
    global scene
    scene = display.set_mode(size)
    scene.fill(WHITE)

    draw_grid(offset=100)
    draw_up_info()


def check_win():
    for i in range(size_board):
        # Проверка выигрыша
        if (val_board[i * 3] == val_board[i * 3 + 1] == val_board[i * 3 + 2] and val_board[i * 3] + val_board[
            i * 3 + 1] + val_board[i * 3 + 2] >= 0) or (
                val_board[i] == val_board[i + 3] == val_board[i + 6] and val_board[i] + val_board[i + 3] + val_board[
            i + 6] >= 0) or (
                val_board[0] == val_board[4] == val_board[8] and val_board[0] + val_board[4] + val_board[8] >= 0) or (
                val_board[2] == val_board[4] == val_board[6] and val_board[2] + val_board[4] + val_board[
            6] >= 0):
            return True
        if count_step == 9:
            return 1
    return False


def finish_screen(text):
    scene.fill(WHITE)
    Label(size[0] // 2, size[1] // 4, 100, BLACK, text)
    # scene.blit(obj_text, (size[0] // 2 - (obj_text.get_width() // 2), size[1] // 2 - (obj_text.get_height() // 2)))
    repit = create_but(280, 80, (size[0] // 2 - 140, size[1] // 4 * 3 - 40))
    Label(size[0] // 2, size[1] // 4 * 3, repit.height - 10, WHITE, "Переиграть")


def repit_game():
    # Переменные приводятся к прежнему состоянию
    global computer, player, val_board, cell_coord_list, count_step, queue_pos, stop_play
    count_step = 0
    cell_coord_list = [(x, y) for x in range(1, 4) for y in range(1, 4)]
    val_board = [-1 for _ in range(9)]
    player = computer = None
    queue_pos = 0
    stop_play = False

    # Изменение размеров окна
    scene = display.set_mode(size)
    scene.fill(WHITE)

    # Создание текста о выборе персонажа
    info_up.draw_text()

    # отрисовка объектов Крестика и Нолика
    X_player.create_button()
    O_player.create_button()

    # Отрисовка текста на кнопки
    X_text.draw_text()
    O_text.draw_text()

    draw_grid(offset=100)  # Отрисовка сетки со смещением


def step(coord_cell):
    global queue_pos, count_step, computer, player, stop_play
    num_cell = coord_cell[0] + (coord_cell[1] - 1) * size_board - 1  # Номер нажатой ячейки
    val_board[num_cell] = queue[queue_pos]  # Ход игрока, добавление хода в val_board
    draw_img_player(coord_cell)  # Отрисовка изображения X либо 0
    count_step += 1  # Добавление счетчика
    check = check_win()
    if check:
        if type(check) == bool:
            finish_screen(f"Победил {players[queue[queue_pos]]}")  # Информация о выигрыше
        else:
            finish_screen("Ничья")  # Информация о ничьей
        # Совершен выигрыш либо ничья
        stop_play = True
    queue_pos = 1 - queue_pos  # Изменение очередности хода
    if not stop_play:
        draw_up_info()


def find_best_option():
    # if (val_board[i * 3] == val_board[i * 3 + 1] == val_board[i * 3 + 2] and val_board[i * 3] + val_board[
    #             i * 3 + 1] + val_board[i * 3 + 2] >= 0) or (
    #                 val_board[i] == val_board[i + 3] == val_board[i + 6] and val_board[i] + val_board[i + 3] + val_board[
    #             i + 6] >= 0) or (
    #                 val_board[0] == val_board[4] == val_board[8] and val_board[0] + val_board[4] + val_board[8] >= 0) or (
    #                 val_board[2] == val_board[4] == val_board[6] and val_board[2] + val_board[4] + val_board[
    #             6] >= 0):
    for i in range(size_board):
        if val_board[i * 3] + val_board[i * 3 + 1] + val_board[i * 3 + 2] + 1 == 0 and val_board[i:i * 3 + 2 + 1].count(
                -1) == 1:
            index_cell = val_board[i:i * 3 + 2 + 1].index(-1) * (i + 1)
            print("1", val_board, val_board[i:i * 3 + 2 + 1], index_cell, sep="\t")
        elif val_board[i] + val_board[i + 3] + val_board[i + 6] + 1 == 0 and val_board[::3].count(
                -1) == 1:
            index_cell = val_board[::3].index(-1) * size_board + i
            print("2", val_board, val_board[::3], index_cell, sep="\t")
        elif val_board[0] + val_board[4] + val_board[8] + 1 == 0 and val_board[::4].count(
                -1) == 1:
            index_cell = val_board[::4].index(-1) * 4
            print("3", val_board, val_board[::4], index_cell, sep="\t")
        elif val_board[2] + val_board[4] + val_board[6] + 1 == 0:
            pass


def choice_step_computer():
    global count_step_computer
    best_coord = find_best_option()
    if not count_step_computer:
        coord_step = choice([(1, 1), (1, 3), (3, 1), (3, 3), (2, 2)])
        if coord_step in cell_coord_list:
            step(coord_step)
            cell_coord_list.remove(coord_step)
        else:
            return choice_step_computer()
        count_step_computer += 1
    elif best_coord:
        pass
    else:
        coord_step = choice(cell_coord_list)
        step(coord_step)
        cell_coord_list.remove(coord_step)


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

size = (500, 600)
size_board = 3
size_cell = 150
margin = 25
count_step = 0
count_step_computer = 0
cell_coord_list = [(x, y) for x in range(1, 4) for y in range(1, 4)]
val_board = [-1 for _ in range(9)]
player = computer = None
queue = (player, computer)
queue_pos = randint(0, 1)
players = ["O", "X"]
img_X = transform.scale(image.load("img/x.png"), (size_cell - 20, size_cell - 20))
img_O = transform.scale(image.load("img/o.png"), (size_cell - 20, size_cell - 20))
game_over = False
stop_play = False

init()

scene = display.set_mode(size)
display.set_caption("Крестики-Нолики")
display.set_icon(image.load("img/icon.ico"))
scene.fill(WHITE)

# Создание текста о выборе персонажа
info_up = Label(size[0] // 2, 25, 40, BLACK, "Выберите X либо O")

# Создание объектов Крестика и Нолика
X_player = create_but(120, 40, (65, 55))
O_player = create_but(120, 40, (315, 55))

# Создание объектов текста X и 0
X_text = Label(X_player.x + X_player.width // 2, X_player.y + X_player.height // 2, X_player.height, WHITE, "X")
O_text = Label(O_player.x + O_player.width // 2, O_player.y + O_player.height // 2, O_player.height, WHITE, "O")

draw_grid(offset=100)  # Добавление смещения

while not game_over:
    for e in event.get():
        if e.type == QUIT:
            game_over = True
        elif e.type == MOUSEBUTTONDOWN:
            x, y = e.pos
            click_coord = ((x - margin) // size_cell + 1, (y - margin - 100) // size_cell + 1)  # Координаты клика
            # Проверка, что очередь хода игрока, клик не выходит за пределы сетки и выбран X либо 0
            if (not queue_pos and
                    margin <= x <= margin + size_cell * size_board and (margin + 100) <= y <= (
                            margin + 100) + size_cell * size_board
                    and click_coord in cell_coord_list and player != computer != None):
                step(click_coord)  # Совершение хода
                cell_coord_list.remove(click_coord)  # Удаление нажатых координат

            # Проверка,что клик по кнопке X
            if (player == computer == None) and (X_player.x <= x <= X_player.x + X_player.width) and (
                    X_player.y <= y <= X_player.y + X_player.height):
                # 1 - крестик; 0 - нолик
                player, computer = 1, 0
                # Создание очередности игроков
                queue = (player, computer)
                hide_button()
            # Проверка, что клик по кнопке 0
            elif (player == computer == None) and (O_player.x <= x <= O_player.x + X_player.width) and (
                    O_player.y <= y <= O_player.y + O_player.height):
                # 1 - крестик; 0 - нолик
                player, computer = 0, 1
                # Создание очередности игроков
                queue = (player, computer)
                hide_button()

            # Проверка что клик по кнопке Переиграть
            if stop_play and (size[0] // 2 - 140 <= x <= size[0] // 2 + 140 and size[1] // 4 * 3 - 40 <= y <= size[
                1] // 4 * 3 + 40):
                repit_game()
    if queue_pos and (player != computer != None) and not stop_play:
        choice_step_computer()

    display.update()
    time.delay(60)
quit()
