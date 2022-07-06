import tkinter
import tkinter.messagebox
import math
import random
from functools import partial
from itertools import chain

ROW_COUNT = 10
COLUMN_COUNT = 10
CELL_SIZE = 64

MAIN_WINDOW = tkinter.Tk()

BLANK_CELL = tkinter.PhotoImage(
    file=r"./blank-cell.png")
CROSS_MARK = tkinter.PhotoImage(
    file=r"./cross.png")
CIRCLE_MARK = tkinter.PhotoImage(
    file=r"./circle.png")


def toggle_button(button: tkinter.Button, toggle: bool):
    state = 'normal' if toggle else 'disabled'
    button['state'] = state


class Player:
    pass


class Game:
    pass


class Cell(tkinter.Button):
    def __init__(self, grid_window: tkinter.PanedWindow, game: Game, coordinates: tuple[int, int]):
        self.x, self.y = coordinates
        self.player_id = -1

        super().__init__(grid_window, width=CELL_SIZE, height=CELL_SIZE, image=BLANK_CELL)

        self['state'] = 'disabled'
        self.configure(command=partial(game.claim_cell, cell=self))
        self.grid(column=self.x, row=self.y)

    def reset(self):
        self.player_id = -1
        self.configure(image=BLANK_CELL, bg='white')

    def is_claimed(self) -> bool:
        return self.player_id != -1

    def is_owned_by_player(self, player: Player) -> bool:
        return self.player_id == player.id

    def set_matched_color(self):
        self.configure(bg='red')

    def get_coords(self) -> tuple[int, int]:
        return (self.x, self.y)


class Player:
    def __init__(self, name: str, player_id: int):
        self.name = name
        self.id = player_id
        self.owned_cells = list()

    def claim_cell(self, cell: Cell):
        self.owned_cells.append(cell)
        self.owned_cells.sort(key=lambda c: (c.x, c.y))
        toggle_button(cell, False)
        cell.player_id = self.id
        cell.configure(image=self.mark)

    def clear_owned_cells(self):
        self.owned_cells = list()


class Game:
    def __init__(self, grid_window: tkinter.PanedWindow, selection_window: tkinter.PanedWindow):
        self.human_player = Player(name="Игрок", player_id=0)
        self.computer_player = Player(name="Компьютер", player_id=1)
        self.current_player = self.human_player

        self.init_grid(grid_window)

        self.select_crosses_button = self.make_selection_button(
            "Выбрать X", CROSS_MARK, selection_window)
        self.select_circles_button = self.make_selection_button(
            "Выбрать O", CIRCLE_MARK, selection_window)

    def init_grid(self, grid_window: tkinter.PanedWindow):
        self.grid = list()

        for x in range(COLUMN_COUNT):
            self.grid.append(list())
            for y in range(ROW_COUNT):
                cell = Cell(grid_window, self, (x, y))
                self.grid[x].append(cell)

    def make_selection_button(self, text: str, mark: tkinter.PhotoImage, selection_window: tkinter.PanedWindow) -> tkinter.Button:
        select_button = tkinter.Button(master=selection_window,
                                       width=25, height=7, text=text, command=partial(self.select_mark, mark=mark))
        select_button.pack(side=tkinter.LEFT)

        return select_button

    def toggle_game(self, start_game: bool):
        if start_game:
            self.human_player.clear_owned_cells()
            self.computer_player.clear_owned_cells()

        self.toggle_grid_buttons(start_game)
        self.toggle_selection_buttons(not start_game)

    def toggle_grid_buttons(self, toggle: bool):
        for row in self.grid:
            for cell in row:
                toggle_button(cell, toggle)
                if toggle:
                    cell.reset()
                    toggle_button(cell, True)

    def toggle_selection_buttons(self, toggle: bool):
        toggle_button(self.select_circles_button, toggle)
        toggle_button(self.select_crosses_button, toggle)

    def select_mark(self, mark: tkinter.PhotoImage):
        self.human_player.mark = mark
        self.computer_player.mark = self.opposite_mark(mark)
        self.toggle_game(True)

    def opposite_mark(self, mark: tkinter.PhotoImage) -> tkinter.PhotoImage:
        return CROSS_MARK if mark == CIRCLE_MARK else CIRCLE_MARK

    def check_match_5(self, cell: Cell) -> bool:
        non_diagonal_coords = self.generate_non_diagonal_coords(cell)
        diagonal_coords = self.generate_diagonal_coords(cell)
        coords_lists = list(chain(non_diagonal_coords, diagonal_coords))

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

    def generate_non_diagonal_coords(self, cell: Cell) -> list[list[tuple[int, int]]]:
        return [
            list(map(lambda i: (cell.x, i), list(range(ROW_COUNT)))),
            list(map(lambda i: (i, cell.y), list(range(COLUMN_COUNT))))
        ]

    def generate_diagonal_coords(self, cell: Cell) -> list[list[tuple[int, int]]]:
        coord = cell.get_coords()

        def diagonal_half_coords(coord: tuple[int, int], step: tuple[int, int]) -> list[tuple[int, int]]:
            result = []
            while True:
                coord = (coord[0] + step[0], coord[1] + step[1])
                if not (coord[0] > 0 and coord[0] < COLUMN_COUNT and
                        coord[1] > 0 and coord[1] < ROW_COUNT):
                    break

                result.append(coord)

            return result

        left_half = diagonal_half_coords(coord, (-1, -1))[::-1]
        right_half = diagonal_half_coords(coord, (1, 1))

        first_diagonal = left_half + [coord] + right_half

        left_half = diagonal_half_coords(coord, (-1, 1))[::-1]
        right_half = diagonal_half_coords(coord, (1, -1))

        second_diagonal = left_half + [coord] + right_half

        return [first_diagonal, second_diagonal]

    def get_cell(self, coords: tuple[int, int]) -> Cell:
        return self.grid[coords[0]][coords[1]]

    def computer_claim_cell(self):
        flat_grid = list(chain.from_iterable(self.grid))
        unclaimed_cells = [
            cell for cell in flat_grid if not cell.is_claimed()]
        random_cell = random.choice(unclaimed_cells)
        self.claim_cell(random_cell)

    def claim_cell(self, cell: Cell):
        if cell.is_claimed():
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

    def switch_current_player(self):
        if self.current_player == self.human_player:
            self.current_player = self.computer_player
        elif self.current_player == self.computer_player:
            self.current_player = self.human_player


def main():

    grid_window = tkinter.PanedWindow()
    grid_window.pack()

    selection_window = tkinter.PanedWindow()
    selection_window.pack()

    game = Game(grid_window, selection_window)

    MAIN_WINDOW.mainloop()


if __name__ == "__main__":
    main()
