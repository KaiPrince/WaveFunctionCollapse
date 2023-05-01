import pytest
import numpy as np

from sudoku.board import Board, BoardData
from sudoku.sudoku import sudoku_board, empty_board
from wave_function_collapse.wave_function_collapse import (
    WaveFunctionCollapse,
    MIN_ENTROPY,
)


@pytest.fixture
def wave_function_collapse():
    board = sudoku_board
    return WaveFunctionCollapse(board)


@pytest.fixture
def build_wave_function_collapse():
    def __inner(board_data: BoardData):
        board = Board(np.copy(np.array(board_data)).tolist())
        return WaveFunctionCollapse(board)

    return __inner


def test_constructor():
    # Arrange
    board = sudoku_board

    # Act
    obj = WaveFunctionCollapse(board)

    # Assert
    assert isinstance(obj, WaveFunctionCollapse)


def test_solve(build_wave_function_collapse):
    # Arrange
    board: BoardData = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [9, 1, 2, 3, 4, 5, 6, 7, 8],
        [8, 9, 1, None, None, 4, 5, 6, 7],
        [7, 8, 9, None, None, 3, 4, 5, 6],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
    ]
    wave_function_collapse = build_wave_function_collapse(board)

    # Act
    solution = wave_function_collapse.solve().data

    # Assert
    assert solution == sudoku_board


@pytest.mark.parametrize(
    "board, expected",
    [
        [sudoku_board, np.full([9, 9], 0).tolist()],
        [empty_board, np.full([9, 9], 9).tolist()],
    ],
)
def test_initialize_wave(build_wave_function_collapse, board, expected):
    # Arrange
    wave_function_collapse = build_wave_function_collapse(board)

    # Act
    wave = wave_function_collapse.initialize_wave()

    # Assert
    assert wave == expected


def test_observe_col(build_wave_function_collapse):
    # Arrange
    cell_row = 3
    cell_col = 4
    board: BoardData = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [9, 1, 2, 3, 4, 5, 6, 7, 8],
        [8, 9, 1, 2, 3, 4, 5, 6, 7],
        [7, 8, 9, None, None, 3, 4, 5, 6],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
    ]
    wave_function_collapse = build_wave_function_collapse(board)

    # Act
    collapsed_board: Board = wave_function_collapse.observe_cell(cell_row, cell_col)

    # Assert
    collapsed_cell = collapsed_board._get_cell(cell_row, cell_col)
    assert collapsed_cell == 2


def test_observe_row(build_wave_function_collapse):
    # Arrange
    cell_row = 3
    cell_col = 4
    board: BoardData = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [9, 1, 2, 3, 4, 5, 6, 7, 8],
        [8, 9, 1, 2, None, 4, 5, 6, 7],
        [7, 8, 9, 1, None, 3, 4, 5, 6],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
    ]
    wave_function_collapse = build_wave_function_collapse(board)

    # Act
    collapsed_board: Board = wave_function_collapse.observe_cell(cell_row, cell_col)

    # Assert
    collapsed_cell = collapsed_board._get_cell(cell_row, cell_col)
    assert collapsed_cell == 2


def test_compute_entropy_full_board(build_wave_function_collapse):
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
    wave_function_collapse = build_wave_function_collapse(board)

    # Act
    entropy = wave_function_collapse.get_entropy(cell_row, cell_col)

    # Assert
    assert entropy == MIN_ENTROPY


def test_compute_entropy_one_option(build_wave_function_collapse):
    # Arrange
    cell_row = 3
    cell_col = 4
    board: Board = [
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
    wave_function_collapse = build_wave_function_collapse(board)

    # Act
    entropy = wave_function_collapse.get_entropy(cell_row, cell_col)

    # Assert
    assert entropy == 1


def test_compute_entropy_two_options(build_wave_function_collapse):
    # Arrange
    cell_row = 3
    cell_col = 4
    board: Board = [
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
    wave_function_collapse = build_wave_function_collapse(board)

    # Act
    entropy = wave_function_collapse.get_entropy(cell_row, cell_col)

    # Assert
    assert entropy == 2
