from pygame import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

size = (500, 500)
size_board = 3
size_cell = 150
margin = 25
count_step = 0
cell_coord_list = [(x, y) for x in range(1, 4) for y in range(1, 4)]
val_board = [-1 for _ in range(10)]
player = computer = None
queue = (player, computer)
queue_pos = 0
players = ["0", "X"]
img_X = transform.scale(image.load("img/x.png"), (size_cell - 20, size_cell - 20))
img_O = transform.scale(image.load("img/o.png"), (size_cell - 20, size_cell - 20))
game_over = False


class Button:
    def __init__(self, width, height, x, y, text, fill_color):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.text = text
        self.fill_color = fill_color

        self.create_button()
        self.setText()
        self.draw_text()

    def create_button(self):
        #  Рисует кнопку
        draw.rect(scene, self.fill_color, (self.x, self.y, self.width, self.height))

    def setText(self):
        # Устанавливает текст на кнопке
        self.cr_text = font.Font(None, self.height).render(self.text, True, WHITE)

    def draw_text(self):
        width_text = self.cr_text.get_width()
        height_text = self.cr_text.get_height()
        # Отрисовка текста по центру кнопки
        scene.blit(self.cr_text,
                   (self.x + (self.width // 2 - width_text // 2), self.y + (self.height // 2 - height_text // 2)))


def draw_grid(offset=0):
    for i in range(size_board - 1):
        # Рисует горизонтальную линию
        draw.line(scene, BLACK, (margin, margin + offset + size_cell + size_cell * i - 1),
                  (margin + size_cell * size_board, margin + offset + size_cell + size_cell * i - 1), 2)
        # Рисует вертикальную линию
        draw.line(scene, BLACK, (margin + size_cell + size_cell * i - 1, margin + offset),
                  (margin + size_cell + size_cell * i - 1, margin + offset + size_cell * size_board), 2)


def create_but(width, height, start_coord, text):
    return Button(width, height, start_coord[0], start_coord[1], text, BLACK)


def draw_img_player(coord_cell):
    queue_player = queue[queue_pos]
    if queue_player:
        scene.blit(img_X, (
            (margin + 10) + ((coord_cell[0] - 1) * size_cell), (margin + 10) + ((coord_cell[1] - 1) * size_cell)))
    else:
        scene.blit(img_O, (
            (margin + 10) + ((coord_cell[0] - 1) * size_cell), (margin + 10) + ((coord_cell[1] - 1) * size_cell)))


def hide_button():
    global scene
    scene = display.set_mode(size)
    scene.fill(WHITE)
    draw_grid()


def check_win():
    for i in range(size_board):
        # Проверка выигрыша
        if (val_board[i * 3] == val_board[i * 3 + 1] == val_board[i * 3 + 2] and val_board[i * 3] + val_board[
            i * 3 + 1] + val_board[i * 3 + 2] >= 0) or (
                val_board[i] == val_board[i + 3] == val_board[i + 6] and val_board[i] + val_board[i + 3] + val_board[
            i + 6] >= 0) or (
                val_board[0] == val_board[4] == val_board[8] and val_board[0] + val_board[4] + val_board[8] >= 0) or (
                val_board[2] == val_board[4] == val_board[6] and val_board[2] + val_board[4] + val_board[
            6] >= 0) or count_step == 9:
            return True
    return False


def finish_screen(text):
    obj_text = font.Font(None, 100).render(text, True, BLACK)
    scene.fill(WHITE)
    scene.blit(obj_text, (size[0] // 2 - (obj_text.get_width() // 2), size[1] // 2 - (obj_text.get_height() // 2)))


def step(coord_cell):
    global queue_pos, count_step
    num_cell = coord_cell[0] + (coord_cell[1] - 1) * size_board - 1  # Номер нажатой ячейки
    val_board[num_cell] = queue[queue_pos]  # Ход игрока, добавление хода в val_board
    draw_img_player(coord_cell)
    count_step += 1
    if check_win():
        if count_step == 9:
            scene.fill(BLACK)
        else:
            finish_screen(f"Победил {players[queue[queue_pos]]}")
    queue_pos = 1 - queue_pos


init()

scene = display.set_mode((size[0], size[1] + 50))
display.set_caption("Крестики-Нолики")
display.set_icon(image.load("img/icon.ico"))
scene.fill(WHITE)

# Создание объектов Крестика и Нолика
X_player = create_but(120, 40, (65, 15), "X")
O_player = create_but(120, 40, (315, 15), "0")

draw_grid(offset=50)  # Добавление смещения

while not game_over:
    queue = (player, computer)

    for e in event.get():
        if e.type == QUIT:
            game_over = True
        elif e.type == MOUSEBUTTONDOWN:
            x, y = e.pos
            click_coord = ((x - margin) // size_cell + 1, (y - margin) // size_cell + 1)  # Координаты клика
            # Проверка, что клик не выходит за пределы сетки и выбран X либо 0
            if (
                    margin <= x <= margin + size_cell * size_board and margin <= y <= margin + size_cell * size_board
                    and click_coord in cell_coord_list and player != computer != None):
                step(click_coord)  # Совершение хода
                cell_coord_list.remove(click_coord)  # Удаление нажатых координат
            # Проверка,что клик по кнопке X
            if (X_player.x <= x <= X_player.x + X_player.width) and (X_player.y <= y <= X_player.y + X_player.height):
                # 1 - крестик; 0 - нолик
                player, computer = 1, 0
                hide_button()
            # Проверка, что клик по кнопке 0
            elif O_player.x <= x <= O_player.x + X_player.width and O_player.y <= y <= O_player.y + O_player.height:
                # 1 - крестик; 0 - нолик
                player, computer = 0, 1
                hide_button()

        display.update()
        time.delay(60)
quit()
