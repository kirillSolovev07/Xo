from pygame import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

size = (500, 550)
size_board = 3
size_cell = 150
margin = 25
cell_coord_list = [(x, y) for x in range(1, 4) for y in range(1, 4)]
val_board = [0 for _ in range(10)]
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

    def create_button(self):
        draw.rect(scene, self.fill_color, (self.x, self.y, self.width, self.height))


def draw_grid():
    for i in range(size_board - 1):
        draw.line(scene, BLACK, (margin, margin + 50 + size_cell + size_cell * i - 1),
                  (margin + size_cell * size_board, margin + 50 + size_cell + size_cell * i - 1), 2)
        draw.line(scene, BLACK, (margin + size_cell + size_cell * i - 1, margin + 50),
                  (margin + size_cell + size_cell * i - 1, margin + 50 + size_cell * size_board), 2)


def create_but(start_coord, finish_coord, text):
    return Button(finish_coord[0], finish_coord[1], start_coord[0], start_coord[1], text, BLACK)


def draw_img_player(coord_cell):
    pass


def check_win():
    for i in range(size_board):
        if (val_board[i * 3] == val_board[i * 3 + 1] == val_board[i * 3 + 2]) or (
                val_board[i] == val_board[i + 3] == val_board[i + 6]) or (
                val_board[0] == val_board[4] == val_board[8]) or (
                val_board[2] == val_board[4] == val_board[6]):
            return True
    return False


def step(coord_cell):
    if not check_win():
        num_cell = coord_cell[0] ** 2 * coord_cell[1] - 1
        val_board[num_cell] = None


init()

scene = display.set_mode(size)
display.set_caption("Крестики-Нолики")
scene.fill(WHITE)

while not game_over:
    for e in event.get():
        if e.type == QUIT:
            game_over = True
        elif e.type == MOUSEBUTTONDOWN:
            x, y = e.pos
            click_coord = ((x - margin) // size_cell + 1, (y - margin - 50) // size_cell + 1)
            if margin < x < margin + size_cell * size_board and margin < y < margin + size_cell * size_board and click_coord in cell_coord_list:
                step(click_coord)
                cell_coord_list.remove(((x - margin) // size_cell + 1, (y - margin) // size_cell + 1))

        draw_grid()
        a = create_but((90, 15), (160, 35), "Ffff")
        b = create_but((340, 15), (410, 35), "Ffff")

        display.update()
        time.delay(60)
