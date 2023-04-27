from sudoku.board import Board, Line
import numpy as np

sudoku_board: Board = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [9, 1, 2, 3, 4, 5, 6, 7, 8],
    [8, 9, 1, 2, 3, 4, 5, 6, 7],
    [7, 8, 9, 1, 2, 3, 4, 5, 6],
    [6, 7, 8, 9, 1, 2, 3, 4, 5],
    [5, 6, 7, 8, 9, 1, 2, 3, 4],
    [4, 5, 6, 7, 8, 9, 1, 2, 3],
    [3, 4, 5, 6, 7, 8, 9, 1, 2],
    [2, 3, 4, 5, 6, 7, 8, 9, 1],
]

empty_board: Board = np.full([9, 9], None).tolist()


def print_board():
    for row in sudoku_board:
        print(row)


def is_row_valid(row: Line):
    if {1, 2, 3, 4, 5, 6, 7, 8, 9} == set(row):
        return True

    return False


def is_col_valid(index: int):
    col: Line = [row[index] for row in sudoku_board]
    if {1, 2, 3, 4, 5, 6, 7, 8, 9} == set(col):
        return True
    return False


def is_board_valid():
    for row in sudoku_board:
        if not is_row_valid(row):
            return False

    for col_index in range(len(sudoku_board[0])):
        if not is_col_valid(col_index):
            return False

    return True


def main():
    print_board()
    print(is_board_valid())


if __name__ == "__main__":
    main()
