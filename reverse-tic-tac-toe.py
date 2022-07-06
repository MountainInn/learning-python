import tkinter
import tkinter.messagebox
import math
import random
from functools import partial
from itertools import chain

ROW_COUNT = 10
COLUMN_COUNT = 10
CELL_SIZE = 64

win = tkinter.Tk()

BLANK_CELL = tkinter.PhotoImage(
    file=r"./blank-cell.png")
CROSS_CELL = tkinter.PhotoImage(
    file=r"./cross.png")
CIRCLE_CELL = tkinter.PhotoImage(
    file=r"./circle.png")


class Player:
    pass

class Cell(tkinter.Button):
    def __init__(self, master, game, coordinates):
        self.x, self.y = coordinates
        self.value = -1

        super().__init__(master, width=CELL_SIZE, height=CELL_SIZE, image=BLANK_CELL)

        self['state'] = 'disabled'
        self.configure(command=partial(game.claim_cell, cell=self))
        self.grid(column=self.x, row=self.y)

    def reset(self):
        self.toggle(True)
        self.value = -1
        self.configure(image=BLANK_CELL, bg='white')

    def is_claimed(self):
        return self.value != -1

    def is_owned_by_player(self, player: Player):
        return self.value == player.player_id

    def toggle(self, toggle):
        self['state'] = 'normal' if toggle else 'disabled'

    def set_matched_color(self):
        self.configure(bg='red')

    def get_coords(self):
        return (self.x, self.y)


class Player:
    def __init__(self, name, player_id):
        self.name = name
        self.player_id = player_id
        self.owned_cells = list()

    def set_mark(self, mark):
        self.mark = mark

    def claim_cell(self, cell: Cell):
        self.owned_cells.append(cell)
        self.owned_cells.sort(key=lambda c: (c.x, c.y))
        cell.toggle(False)
        cell.value = self.player_id
        cell.configure(image=self.mark)

    def reset_owned_cells(self):
        self.owned_cells = list()


class Game:
    def __init__(self, grid_window, selection_window):
        self.human_player = Player(name="Игрок", player_id=0)
        self.computer_player = Player(name="Компьютер", player_id=1)
        self.current_player = self.human_player

        self.init_grid(grid_window)

        self.select_crosses_button = self.make_selection_button("Выбрать X", CROSS_CELL, selection_window)
        self.select_circles_button = self.make_selection_button("Выбрать O", CIRCLE_CELL, selection_window)

    def make_selection_button(self, text, mark, selection_window):
        self.select_crosses_button = tkinter.Button(master=selection_window,
                                                    width=25, height=7, text=text, command=partial(self.select_side, mark=mark))
        self.select_crosses_button.pack(side=tkinter.LEFT)

    def init_grid(self, grid_window):
        self.grid = list()

        for x in range(COLUMN_COUNT):
            self.grid.append(list())
            for y in range(ROW_COUNT):
                cell = Cell(grid_window, self, (x, y))
                self.grid[x].append(cell)

    def toggle_grid_buttons(self, toggle: bool):
        for row in self.grid:
            for cell in row:
                cell.toggle(toggle)
                if toggle:
                    cell.reset()

    def toggle_selection_buttons(self, toggle: bool):
        state = 'normal' if toggle else 'disabled'
        self.select_circles_button['state'] = state
        self.select_crosses_button['state'] = state

    def other_mark(self, mark):
        if mark == CROSS_CELL:
            return CIRCLE_CELL
        elif mark == CIRCLE_CELL:
            return CROSS_CELL

    def select_side(self, mark):
        self.human_player.set_mark(mark)
        self.computer_player.set_mark(self.other_mark(mark))
        self.toggle_game(True)

    def toggle_game(self, start_game):
        if start_game:
            self.human_player.reset_owned_cells()
            self.computer_player.reset_owned_cells()
            self.reset_grid()

        self.toggle_selection_buttons(not start_game)
        self.toggle_grid_buttons(start_game)


    def generate_non_diagonal_coords(self, cell:Cell):
        return [
            list( map(lambda i: (cell.x, i), list(range(ROW_COUNT))) ),
            list( map(lambda i: (i, cell.y), list(range(COLUMN_COUNT))) )
        ]

    def generate_diagonal_coords(self, cell:Cell):
        coord = cell.get_coords()

        def generate_diagonal_half(coord, step):
            result = []
            while True:
                coord = (coord[0] + step[0], coord[1] + step[1])
                if not (coord[0] > 0 and coord[0] < COLUMN_COUNT and\
                        coord[1] > 0 and coord[1] < ROW_COUNT ):
                    break

                result.append(coord)

            return result


        left_half = generate_diagonal_half(coord, (-1,-1))[::-1]
        right_half = generate_diagonal_half(coord, (1,1))

        first_diagonal = left_half + [coord] + right_half


        left_half = generate_diagonal_half(coord, (-1, 1))[::-1]
        right_half = generate_diagonal_half(coord, (1, -1))

        second_diagonal = left_half + [coord] + right_half

        return [first_diagonal, second_diagonal]


    def get_cell(self, coords):
        return self.grid[coords[0]][coords[1]]

    def count_matches(self, cell: Cell):
        non_diagonal_coords = self.generate_non_diagonal_coords(cell)
        diagonal_coords = self.generate_diagonal_coords(cell)
        coords_lists = list( chain(non_diagonal_coords, diagonal_coords) )

        for coord_list in coords_lists:
            match_cells = list()
            for coord in coord_list:
                check_cell = self.get_cell(coord)

                if check_cell.is_owned_by_player(self.current_player):
                    match_cells.append(check_cell)
                    if len(match_cells) >= 5:
                        for c in match_cells:
                            c.set_matched_color()
                        return True
                else:
                    match_cells.clear()

        return False

    def check_same_diagonal(self, cell_a: Cell, cell_b: Cell):
        return cell_a.x - cell_a.y == cell_b.x - cell_b.y \
            or cell_a.x + cell_a.y == cell_b.x + cell_b.y

    def get_cells_on_two_diagonals(self, cell: Cell):

        def is_on_the_first_diagonal(cell: Cell, check_cell: Cell):
            return (check_cell.x < cell.x and check_cell.y < cell.y) or (check_cell.x > cell.x and check_cell.y > cell.y)
        def is_on_the_second_diagonal(cell: Cell, check_cell: Cell):
            return (check_cell.x < cell.x and check_cell.y > cell.y) or (check_cell.x > cell.x and check_cell.y < cell.y)

        diagonals = [[cell.get_coords()], [cell.get_coords()]]

        for check_cell in self.current_player.owned_cells:
            if self.check_same_diagonal(cell, check_cell):
                if is_on_the_first_diagonal(cell, check_cell):
                    diagonals[0].append(check_cell.get_coords())
                elif is_on_the_second_diagonal(cell, check_cell):
                    diagonals[1].append(check_cell.get_coords())

        for diagonal in diagonals:
            diagonal.sort()

        return diagonals

    def count_diagonal_matches(self, cell: Cell):
        match_counter = 0

        two_diagonals = get_cells_on_two_diagonals(cell)

        for diagonal in diagonals:
            for c in diagonal:
                if c.is_owned_by_player(self.current_player):
                    match_counter += 1
                    if match_counter >= 5:
                        return True
                else:
                    match_counter = 0

        return False

    def check_match_5(self, cell: Cell) -> bool:
        return self.count_matches(cell)

    def switch_current_player(self):
        if self.current_player == self.human_player:
            self.current_player = self.computer_player
        elif self.current_player == self.computer_player:
            self.current_player = self.human_player

    def reset_grid(self):
        for row in self.grid:
            for cell in row:
                cell.reset()

    def claim_cell(self, cell: Cell):
        if cell.value != -1:
            return

        self.current_player.claim_cell(cell)

        if self.check_match_5(cell):
            self.toggle_game(False)
            tkinter.messagebox.showinfo(
                message=f'{self.current_player.name} проиграл!')
            return

        self.switch_current_player()

        if self.current_player == self.computer_player:
            self.computer_claim_cell()

    def computer_claim_cell(self):
        flat_grid = list(chain.from_iterable(self.grid))
        only_blank_cells = [
            cell for cell in flat_grid if not cell.is_claimed()]
        random_cell = random.choice(only_blank_cells)
        self.claim_cell(random_cell)


paned_window = tkinter.PanedWindow()
paned_window.pack(expand=1)

selection_window = tkinter.PanedWindow()
selection_window.pack()

game = Game(paned_window, selection_window)

win.mainloop()
