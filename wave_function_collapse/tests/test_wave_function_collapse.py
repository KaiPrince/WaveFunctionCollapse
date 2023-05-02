import pytest
import numpy as np

from sudoku.board import Board, BoardData
from sudoku.sudoku import sudoku_board, empty_board
from wave_function_collapse.board_collapser import BoardCollapser
from wave_function_collapse.cell import Cell
from wave_function_collapse.wave_function_collapse import WaveFunctionCollapse


@pytest.fixture
def build_wave_function_collapse():
    def __inner(board_data: BoardData):
        board = Board(np.copy(np.array(board_data)).tolist())
        board_collapser = BoardCollapser(board)
        return WaveFunctionCollapse(board_collapser)

    return __inner


def test_solve(build_wave_function_collapse):
    # Arrange
    board: BoardData = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [9, 1, 2, 3, 4, 5, 6, 7, 8],
        [8, 9, 1, None, None, 4, 5, 6, 7],
        [7, 8, 9, None, None, 3, 4, 5, 6],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [4, None, 6, 7, 8, 9, 1, 2, 3],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
    ]
    wave_function_collapse = build_wave_function_collapse(board)

    # Act
    found_solution = wave_function_collapse.solve()

    # Assert
    assert found_solution is True
    assert wave_function_collapse.collapser.board.data == sudoku_board


@pytest.mark.skip("todo")
def test_solve_fails(build_wave_function_collapse):
    # Arrange
    board: BoardData = np.full([9, 9], 1).tolist()
    board[3][3] = None
    wave_function_collapse = build_wave_function_collapse(board)

    # Act
    with pytest.raises(NotImplementedError):
        wave_function_collapse.solve()

    # Assert


def test_solve_empty_board(build_wave_function_collapse):
    # Arrange
    wave_function_collapse = build_wave_function_collapse(empty_board)

    # Act
    found_solution = wave_function_collapse.solve()

    # Assert
    assert found_solution is True
    assert wave_function_collapse.collapser.board.is_valid()


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
    was_collapsed = wave_function_collapse.observe_cell(Cell(cell_row, cell_col))

    # Assert
    assert was_collapsed is True
    collapsed_cell = wave_function_collapse.collapser.board.get_cell(cell_row, cell_col)
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
    was_collapsed = wave_function_collapse.observe_cell(Cell(cell_row, cell_col))

    # Assert
    assert was_collapsed is True
    collapsed_cell = wave_function_collapse.collapser.board.get_cell(cell_row, cell_col)
    assert collapsed_cell == 2
