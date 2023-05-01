from sudoku.board import Board, Line, BoardData
import numpy as np

sudoku_board: BoardData = [
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

empty_board: BoardData = np.full([9, 9], None).tolist()


def main():
    board = Board(sudoku_board)
    board.print_board()
    print(board.is_valid())


if __name__ == "__main__":
    main()
