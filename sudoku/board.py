import numpy as np

CellState = int | None
Line = list[CellState]
BoardData = list[Line]


class Board:
    data: BoardData
    width: int = 9
    height: int = 9

    def __init__(self, data: BoardData):
        self.prev_data = list()
        self.tries = 0
        self.data = data

    def get_cell(self, row_index: int, col_index: int):
        return self.data[row_index][col_index]

    def set_cell(self, row_index: int, col_index: int, value: int):
        self.tries += 1
        self.prev_data.append(np.copy(np.array(self.data)).tolist())

        self.data[row_index][col_index] = value

    def revert(self):
        self.data = self.prev_data.pop()

    def print(self):
        for row in self.data:
            print(row)

    def _is_row_valid(self, row: Line):
        if {1, 2, 3, 4, 5, 6, 7, 8, 9} == set(row):
            return True

        return False

    def _is_col_valid(self, index: int):
        col: Line = [row[index] for row in self.data]
        if {1, 2, 3, 4, 5, 6, 7, 8, 9} == set(col):
            return True
        return False

    def is_valid(self):
        for row in self.data:
            if not self._is_row_valid(row):
                return False

        for col_index in range(len(self.data[0])):
            if not self._is_col_valid(col_index):
                return False

        return True

    def cell_is_invalid(self, row_index: int, col_index: int) -> bool:
        cell = self.data[row_index][col_index]
        for i, other in enumerate(self.data[row_index]):
            if i == col_index:
                continue

            if other == cell:
                return True

        for i, row in enumerate(self.data):
            if i == row_index:
                continue

            other = row[col_index]
            if other == cell:
                return True

        return False
