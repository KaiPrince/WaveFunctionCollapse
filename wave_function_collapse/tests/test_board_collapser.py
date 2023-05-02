import numpy as np
import pytest

from sudoku.board import BoardData, Board
from sudoku.sudoku import sudoku_board, empty_board
from wave_function_collapse.board_collapser import MIN_ENTROPY, BoardCollapser
from wave_function_collapse.cell import Cell


@pytest.fixture
def build_board_collapser():
    def __inner(data: BoardData):
        board = Board(data)
        return BoardCollapser(board)

    return __inner


@pytest.mark.parametrize(
    "board, expected",
    [
        [sudoku_board, np.full([9, 9], 0).tolist()],
        [empty_board, np.full([9, 9], 9).tolist()],
    ],
)
def test_initialize_wave(build_board_collapser, board, expected):
    # Arrange
    board_collapser = build_board_collapser(board)

    # Act
    wave = board_collapser.initialize_wave()

    # Assert
    assert wave == expected


def test_compute_entropy_full_board(build_board_collapser):
    # Arrange
    cell_row = 3
    cell_col = 4
    board: BoardData = [
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
    board_collapser = build_board_collapser(board)

    # Act
    entropy = board_collapser.get_entropy(Cell(cell_row, cell_col))

    # Assert
    assert entropy == MIN_ENTROPY


def test_compute_entropy_one_option(build_board_collapser):
    # Arrange
    cell_row = 3
    cell_col = 4
    board: BoardData = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [9, 1, 2, 3, 4, 5, 6, 7, 8],
        [8, 9, 1, 2, 3, 4, 5, 6, 7],
        [7, 8, 9, 1, None, 3, 4, 5, 6],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
    ]
    board_collapser = build_board_collapser(board)

    # Act
    entropy = board_collapser.get_entropy(Cell(cell_row, cell_col))

    # Assert
    assert entropy == 1


def test_compute_entropy_two_options(build_board_collapser):
    # Arrange
    cell_row = 3
    cell_col = 4
    board: BoardData = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [9, 1, 2, 3, 4, 5, 6, 7, 8],
        [8, 9, 1, 2, None, 4, 5, 6, 7],
        [7, 8, 9, 1, None, None, 4, 5, 6],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
    ]
    board_collapser = build_board_collapser(board)

    # Act
    entropy = board_collapser.get_entropy(Cell(cell_row, cell_col))

    # Assert
    assert entropy == 2
