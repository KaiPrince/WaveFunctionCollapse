import numpy as np
import pytest

from sudoku.board import Board, BoardData
from sudoku.sudoku import empty_board


@pytest.fixture
def build_board():
    def __inner(data: BoardData):
        return Board(data)

    return __inner


def test_constructor():
    # Arrange

    # Act
    obj = Board(empty_board)

    # Assert
    assert isinstance(obj, Board)


def test_get_cell(build_board):
    # Arrange
    board_data = np.copy(np.array(empty_board)).tolist()
    board_data[2][2] = 9
    board = build_board(board_data)

    # Act
    result = board.get_cell(2, 2)

    # Assert
    assert result == 9


def test_cell_is_invalid_row(build_board):
    # Arrange
    cell_row = 3
    cell_col = 4
    board_data: BoardData = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [9, 1, 2, 3, 4, 5, 6, 7, 8],
        [8, 9, 1, 2, 3, 4, 5, 6, 7],
        [7, 8, 9, 1, 3, 3, 4, 5, 6],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
    ]
    board = build_board(board_data)

    # Act
    result = board.cell_is_invalid(cell_row, cell_col)

    # Assert
    assert result is True


def test_cell_is_invalid_col(build_board):
    # Arrange
    cell_row = 3
    cell_col = 4
    board_data: BoardData = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [9, 1, 2, 3, 4, 5, 6, 7, 8],
        [8, 9, 1, 2, 2, 4, 5, 6, 7],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
    ]
    board = build_board(board_data)

    # Act
    result = board.cell_is_invalid(cell_row, cell_col)

    # Assert
    assert result is True
