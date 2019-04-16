from random import random
from collections import namedtuple

Pos = namedtuple("Pos", ("row", "col"))


class Game:
    def __init__(self, size=8):
        self.size = size
        self.result = None
        self.flags_remaining = 0
        self.mines = 0
        self.mines_found = 0

        rows = []
        for r in range(0, size):
            row = []
            for c in range(0, size):
                cell = Cell(Pos(r, c))
                if random() > .7:
                    cell.mined = True
                    self.flags_remaining += 1
                    self.mines += 1
                row.append(cell)
            rows.append(row)

        self.board = rows

    def print_board(self):
        print(f"Flags remaining: {self.flags_remaining}")
        print('   ' + ' '.join([str(i) for i in range(self.size)]))
        print('   ' + ' '.join(['-' for i in range(self.size)]))
        for row_index in range(self.size):
            strs = [str(row_index)+"|"]
            for cell in self.board[row_index]:
                strs.append(self.draw_cell(cell))
            print(" ".join(strs))

    def draw_cell(self, cell):
        if cell.flagged == True:
            return "f"

        if cell.clicked == False:
            return '?'

        return str(cell.surrounding)

    def count_surrounding_mines(self, pos):
        mine_count = 0
        rowIndex = pos.row
        colIndex = pos.col

        for row_delta in range(-1, 2, 1):
            for col_delta in range(-1, 2, 1):
                r = rowIndex + row_delta
                c = colIndex + col_delta
                is_not_self = not (r == rowIndex and c == colIndex)
                if self.pos_is_on_board(r, c) and is_not_self and self.board[r][c].mined:
                    mine_count += 1

        return mine_count

    def pos_is_on_board(self, row, col):
        return row >= 0 and row < self.size and col >= 0 and col < self.size

    def handle_move(self, row, col):
        cell = self.board[row][col]
        if cell.mined:
            self.result = "You lost."
        else:
            cell.clicked = True
            cell.surrounding = self.count_surrounding_mines(cell.pos)

    def handle_flag(self, row, col):
        cell = self.board[row][col]
        if cell.flagged:
            self.flags_remaining += 1
            cell.flagged = False
            # if they unflag a flagged mine, update gamestate
            if cell.mined:
                self.mines_found -= 1
        else:
            self.flags_remaining -= 1
            cell.flagged = True
            # if they flag a mine, update gamestate
            if cell.mined:
                self.mines_found += 1

    def update_game_result_if_victory(self):
        if self.mines_found == self.mines:
            self.result = "Congratulations, you won!"


class Cell:
    def __init__(self, pos):
        self.clicked = False
        self.mined = False
        self.flagged = False
        self.surrounding = None
        self.pos = pos


if __name__ == "__main__":
    game = Game(4)
    while game.result is None:
        flag = False
        game.print_board()
        choice = input(
            "Enter a move in format <row>,<col>:\nTo toggle a flag on a space, enter f:\n")
        parsed = choice.split(",")
        # check for flag
        if len(parsed) == 1 and parsed[0] == "f":
            if game.flags_remaining == 0:
                print("You have no flags remaining")
                continue
            flag = True
            choice = input("Enter space to flag in format <row>,<col>:\n")
            parsed = choice.split(",")
        # else handle move
        if len(parsed) != 2:
            print(
                f"Read {parsed} from {choice}, please enter in format row,col")
        else:
            try:
                row = int(parsed[0])
                col = int(parsed[1])
            except ValueError:
                print(f"Could not parse {parsed}")
                continue
            if not game.pos_is_on_board(row, col):
                print(
                    f"Row {row} and col {col} are not on size {game.size} board")
            else:
                if not flag:
                    game.handle_move(row, col)
                else:
                    game.handle_flag(row, col)

        if game.result is None:
            game.update_game_result_if_victory()

    print(game.result)
