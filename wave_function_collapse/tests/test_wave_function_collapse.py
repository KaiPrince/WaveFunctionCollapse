import pytest
import numpy as np

from sudoku.board import Board
from sudoku.sudoku import sudoku_board, empty_board
from wave_function_collapse.wave_function_collapse import WaveFunctionCollapse


@pytest.fixture
def wave_function_collapse():
    board = sudoku_board
    return WaveFunctionCollapse(board)


def test_constructor():
    # Arrange
    board = sudoku_board

    # Act
    obj = WaveFunctionCollapse(board)

    # Assert
    assert isinstance(obj, WaveFunctionCollapse)


@pytest.mark.skip("TODO")
def test_solve(wave_function_collapse):
    # Arrange

    # Act
    solution = wave_function_collapse.solve()

    # Assert
    expected_sudoku_board: Board = [
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
    assert solution == expected_sudoku_board


@pytest.mark.parametrize("cell, expected", [[1, 0], [None, 9]])
def test_get_entropy(wave_function_collapse, cell, expected):
    # Arrange

    # Act
    entropy = wave_function_collapse.get_entropy(cell)

    # Assert
    assert entropy == expected


@pytest.mark.parametrize(
    "board, expected",
    [
        [sudoku_board, np.full([9, 9], 0).tolist()],
        [empty_board, np.full([9, 9], 9).tolist()],
    ],
)
def test_initialize_wave(wave_function_collapse, board, expected):
    # Arrange

    # Act
    wave = wave_function_collapse.initialize_wave(board)

    # Assert
    assert wave == expected
