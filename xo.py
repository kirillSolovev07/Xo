from pygame import *
from random import randint, choice


class Button:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

        self.draw_button()

    def draw_button(self):
        #  Рисует кнопку
        draw.rect(scene, BLACK, (self.x, self.y, self.width, self.height))


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


def draw_img_player(coord_cell):
    queue_player = queue[queue_pos]  # Получаем номер игрока
    # Если номер игрока 1 ...
    if queue_player:
        # Добавляем картинку Х
        scene.blit(img_X, (
            (margin + 10) + ((coord_cell[0] - 1) * size_cell), (margin + 110) + ((coord_cell[1] - 1) * size_cell)))
    else:
        #  Добавляем картинку Y
        scene.blit(img_O, (
            (margin + 10) + ((coord_cell[0] - 1) * size_cell), (margin + 110) + ((coord_cell[1] - 1) * size_cell)))


def draw_up_info(human_or_computer, role_game):
    # Заливаем вехний прямоугольник белым цветом
    draw.rect(scene, WHITE, (0, 0, 500, 100))
    # Создаем надписи
    Label(size[0] // 4, 25, 40, BLACK, f"{human_or_computer[0]}: {players[role_game[0]]}")
    Label(size[0] // 4 * 3, 25, 40, BLACK, f"{human_or_computer[1]}: {players[role_game[1]]}")
    Label(size[0] // 2, 75, 35, BLACK, f"Ход {players[queue[queue_pos]]}")


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
    # Заливаем экран белым цветом
    scene.fill(WHITE)
    # Размещаем надпись о победе или ничьей
    Label(size[0] // 2, size[1] // 4, 100, BLACK, text)
    # размещаем кнопку
    repit = Button(280, 80, size[0] // 2 - 140, size[1] // 4 * 3 - 40)
    # размещаем на кнопке надпись
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
    human_human.draw_button()
    human_computer.draw_button()

    # Отрисовка текста на кнопки
    human_text.draw_text()
    computer_text.draw_text()

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
    #  Если игра не остановленна ...
    # Если игра не остановлена ...
    if not stop_play and player != computer != None:
        draw_up_info(("Человек", "Компьютер"), (player, computer))  # Отрисовываем очередность хода
    elif not stop_play and player1 != player2 != None:
        draw_up_info(("Игрок 1", "Игрок 2"), (player1, player2))  # Отрисовываем очередность хода


def index_cell_in_coord(index_cell, num_pos, coord):
    # Если известна координата Х ...
    if num_pos == 0:
        y = (index_cell + 1 - coord) // size_board + 1  # Находим координату Y
        # Возвращаем координаты
        return coord, y
    # Если Координата на главной диагонали ...
    elif num_pos == None:
        #  Возвращаем координаты
        return coord, coord
    # Если известна кордината Y или координата на побочной диагонали ...
    else:
        x = index_cell + 1 - coord * size_board + size_board  # Находим координату Х
        # Возвращаем координаты
        return x, coord


def check_win_step(player):
    index_cell = None
    num_pos = coord = None

    for i in range(size_board):
        # Если в одном ряду 2 одинаковых хода ...
        if (val_board[i * 3] + val_board[i * 3 + 1] + val_board[i * 3 + 2]) + 1 == player and val_board[
                                                                                              i * 3:i * 3 + 2 + 1].count(
            -1) == 1:
            index_cell = val_board[i * 3:i * 3 + 2 + 1].index(-1) + (
                    size_board * i)  # Номер ячейки, в которую надо сделать ход
            num_pos = 1  # Номер координаты
            coord = i + 1  # Координата
        # Если в одном столбце 2 одинаковых хода ...
        elif val_board[i] + val_board[i + 3] + val_board[i + 6] + 1 == player and val_board[i::3].count(
                -1) == 1:
            index_cell = val_board[i::3].index(-1) * size_board + i  # Номер ячейки, в которую надо сделать ход
            num_pos = 0  # Номер координаты
            coord = i + 1  # Координата
        # Если в главной диагонали 2 одинаковых хода ...
        elif val_board[0] + val_board[4] + val_board[8] + 1 == player and val_board[::4].count(
                -1) == 1 and val_board[::4][i] == -1:
            index_cell = val_board[::4].index(-1) * 4  # Номер ячейки, в которую надо сделать ход
            coord = i + 1  # Координата
        # Если в побочной диагонали 2 одинаковых хода ...
        elif val_board[2] + val_board[4] + val_board[6] + 1 == player and val_board[2:7:2].count(
                -1) == 1 and val_board[2:7:2][i] == -1:
            index_cell = val_board[2:7:2].index(-1) * 2 + 2  # Номер ячейки, в которую надо сделать ход
            coord = i + 1  # Координата
            num_pos = 1  # Номер координаты
    # Возвращаем номер клетки, в которую нужно сделать ход, номер координаты (0, 1), одна из координат
    return index_cell, num_pos, coord


def find_best_option():
    # Получение номера клетки, в которую нужно сделать ход, номера координаты (0, 1), одной из координат для компьютера
    index_cell, num_pos, coord = check_win_step(queue[queue_pos] * 2)
    # Если номер клетки и координата не None ...
    if index_cell != coord != None:
        return index_cell_in_coord(index_cell, num_pos, coord)  # Возвращаем полные координаты клетки

    # Получение номера клетки, в которую нужно сделать ход, номера координаты (0, 1), одной из координат для игрока
    index_cell, num_pos, coord = check_win_step(queue[1 - queue_pos] * 2)
    # Если номер клетки и координата не None ...
    if index_cell != coord != None:
        return index_cell_in_coord(index_cell, num_pos, coord)  # Возвращаем полные координаты клетки


def choice_step_computer():
    global count_step_computer
    # Если первый ход компьютера ...
    if not count_step_computer:
        coord_step = choice([(1, 1), (1, 3), (2, 2), (3, 1), (3, 3)])  # Выбор случайных координат
        count_step_computer += 1  # Кол-во ходов компьютера +1
        # Если выбранные координаты в списке свободных координат ...
        if coord_step in cell_coord_list:
            step(coord_step)  # Выполняем ход
            cell_coord_list.remove(coord_step)  # Удаляем координаты из списка свободных координат
        # Иначе ...
        else:
            return choice_step_computer()  # Запускаем рекурсию
    # Если найдено место с наилучшими последствиями хода ...
    elif find_best_option():
        coord_step = find_best_option()  # Получаем координаты места
        step(coord_step)  # Выполняем ход
        cell_coord_list.remove(coord_step)  # Удаляем координаты из списка свободных координат
    # Иначе ...
    else:
        coord_step = choice(cell_coord_list)  # Случайно выбираем координаты из списка доступных
        step(coord_step)  # Выполняем ход
        cell_coord_list.remove(coord_step)  # Удаляем координаты из списка свободных координат


def draw_choice_X_or_O():
    global X_player, O_player
    draw.rect(scene, WHITE, (0, 0, 500, 100))
    # Создание текста о выборе персонажа
    Label(size[0] // 2, 25, 40, BLACK, "Выберите X либо O")

    # Создание объектов Крестика и Нолика
    X_player = Button(120, 40, 65, 55)
    O_player = Button(120, 40, 315, 55)

    # Создание объектов текста X и 0
    Label(X_player.x + X_player.width // 2, X_player.y + X_player.height // 2, X_player.height, WHITE, "X")
    Label(O_player.x + O_player.width // 2, O_player.y + O_player.height // 2, O_player.height, WHITE, "O")


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
play_with_human = play_with_computer = None
player1 = player2 = None
player = computer = None
X_player = O_player = None
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

info_up = Label(size[0] // 2, 25, 40, BLACK, "Выберите с кем будете играть")
human_human = Button(170, 40, 40, 55)
human_computer = Button(170, 40, 290, 55)

human_text = Label(human_human.x + human_human.width // 2, human_human.y + human_human.height // 2, human_human.height,
                   WHITE,
                   "Человек")
computer_text = Label(human_computer.x + human_computer.width // 2, human_computer.y + human_computer.height // 2,
                      human_computer.height, WHITE, "Компьютер")

draw_grid(offset=100)  # Добавление смещения

while not game_over:
    for e in event.get():
        # Если нажата кнопка закрытия ...
        if e.type == QUIT:
            game_over = True
        # Если был клик мыши
        elif e.type == MOUSEBUTTONDOWN:
            x, y = e.pos
            click_coord = ((x - margin) // size_cell + 1, (y - margin - 100) // size_cell + 1)  # Координаты клика
            if (human_human.x <= x <= human_human.x + human_human.width) and (
                    human_human.y <= y <= human_human.y + human_human.height):  # (player == computer == None) and
                play_with_human = True
                play_with_computer = False
                draw_choice_X_or_O()
            elif (
                    human_computer.x <= x <= human_computer.x + human_computer.width) and (
                    human_computer.y <= y <= human_computer.y + human_computer.height):  # (player == computer == None) and
                play_with_computer = True
                play_with_human = False
                draw_choice_X_or_O()

            # Проверка,что клик по кнопке X
            if X_player and player1 == player2 == None and X_player.x <= x <= X_player.x + X_player.width and X_player.y <= y <= X_player.y + X_player.height:
                # 1 - крестик; 0 - нолик
                player1, player2 = 1, 0
            # Проверка, что клик по кнопке 0
            elif O_player and player1 == player2 == None and O_player.x <= x <= O_player.x + O_player.width and O_player.y <= y <= O_player.y + O_player.height:
                # 1 - крестик; 0 - нолик
                player1, player2 = 0, 1

            # Проверка,что клик по кнопке X
            if X_player and player == computer == None and X_player and X_player.x <= x <= X_player.x + X_player.width and X_player.y <= y <= X_player.y + X_player.height:
                # 1 - крестик; 0 - нолик
                player, computer = 1, 0
            # Проверка, что клик по кнопке 0
            elif O_player and player == computer == None and O_player and O_player.x <= x <= O_player.x + O_player.width and O_player.y <= y <= O_player.y + O_player.height:
                # 1 - крестик; 0 - нолик
                player, computer = 0, 1

            # Проверка, что очередь хода игрока, клик не выходит за пределы сетки и выбран X либо 0
            if margin <= x <= margin + size_cell * size_board and (margin + 100) <= y <= (
                    margin + 100) + size_cell * size_board and click_coord in cell_coord_list and player != computer != None:
                step(click_coord)  # Совершение хода
                cell_coord_list.remove(click_coord)  # Удаление нажатых координат

            # Проверка что клик по кнопке Переиграть
            if stop_play and (size[0] // 2 - 140 <= x <= size[0] // 2 + 140 and size[1] // 4 * 3 - 40 <= y <= size[
                1] // 4 * 3 + 40):
                repit_game()

    if play_with_human:
        # Создание очередности игроков
        queue = (player1, player2)
    else:
        # Создание очередности игроков
        queue = (player, computer)

    # Если игра не остановлена ...
    if not stop_play and player != computer != None:
        draw_up_info(("Человек", "Компьютер"), (player, computer))  # Отрисовываем очередность хода
    elif not stop_play and player1 != player2 != None:
        draw_up_info(("Игрок 1", "Игрок 2"), (player1, player2))  # Отрисовываем очередность хода

    # Если очередь хода компьютера и заданы значения ходов и игра не остановлена ...
    if play_with_computer and queue_pos and (player != computer != None) and not stop_play:
        choice_step_computer()  # Выбираем ход для компьютера

    display.update()
    time.delay(60)
quit()
