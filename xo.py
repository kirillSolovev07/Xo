from pygame import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

size = (500, 550)
size_board = 3
size_cell = 150
margin = 25
cell_coord_list = [(x, y) for x in range(1, 4) for y in range(1, 4)]
val_board = [-1 for _ in range(10)]
player = computer = None
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

    def draw_rect(self):
        return Rect(0, 0, 500, 50)

    def create_button(self):
        self.rect = self.draw_rect()
        draw.rect(scene, self.fill_color, (self.x, self.y, self.width, self.height))

    def setText(self):
        self.cr_text = font.Font(None, self.height).render(self.text, True, WHITE)

    def draw_text(self):
        width_text = self.cr_text.get_width()
        height_text = self.cr_text.get_height()
        scene.blit(self.cr_text,
                   (self.x + (self.width // 2 - width_text // 2), self.y + (self.height // 2 - height_text // 2)))


def draw_grid():
    for i in range(size_board - 1):
        draw.line(scene, BLACK, (margin, margin + 50 + size_cell + size_cell * i - 1),
                  (margin + size_cell * size_board, margin + 50 + size_cell + size_cell * i - 1), 2)
        draw.line(scene, BLACK, (margin + size_cell + size_cell * i - 1, margin + 50),
                  (margin + size_cell + size_cell * i - 1, margin + 50 + size_cell * size_board), 2)


def create_but(width, height, start_coord, text):
    return Button(width, height, start_coord[0], start_coord[1], text, BLACK)


def draw_img_player(coord_cell):
    pass


def check_win():
    for i in range(size_board):
        print(i)
        if (val_board[i * 3] == val_board[i * 3 + 1] == val_board[i * 3 + 2] and val_board[i * 3] + val_board[
            i * 3 + 1] + val_board[i * 3 + 2] > 0) or (
                val_board[i] == val_board[i + 3] == val_board[i + 6] and val_board[i] + val_board[i + 3] + val_board[
            i + 6] > 0) or (
                val_board[0] == val_board[4] == val_board[8] and val_board[0] + val_board[4] + val_board[8] > 0) or (
                val_board[2] == val_board[4] == val_board[6] and val_board[2] + val_board[4] + val_board[6] > 0):
            print(val_board)
            return True
    return False


def step(coord_cell):
    if not check_win():
        num_cell = coord_cell[0] + (coord_cell[1] - 1) * size_board - 1
        val_board[num_cell] = 1
        # print(num_cell)


init()

scene = display.set_mode(size)
display.set_caption("Крестики-Нолики")
scene.fill(WHITE)

X = create_but(120, 40, (65, 15), "X")
O = create_but(120, 40, (315, 15), "0")

while not game_over:
    draw_grid()

    for e in event.get():
        if e.type == QUIT:
            game_over = True
        elif e.type == MOUSEBUTTONDOWN:
            x, y = e.pos
            click_coord = ((x - margin) // size_cell + 1, (y - margin - 50) // size_cell + 1)
            if (
                    margin <= x <= margin + size_cell * size_board and margin + 50 <= y <= margin + 50 + size_cell * size_board
                    and click_coord in cell_coord_list):
                step(click_coord)
                cell_coord_list.remove(((x - margin) // size_cell + 1, (y - (margin + 50)) // size_cell + 1))
            if (X.x <= x <= X.x + X.width) and (X.y <= y <= X.y + X.height):
                player, computer = 1, 0
            elif O.x <= x <= O.x + X.width and O.y <= y <= O.y + O.height:
                player, computer = 0, 1

        display.update()
        time.delay(60)
