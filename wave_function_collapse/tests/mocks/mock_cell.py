from wave_function_collapse.cell import Cell, T_SuperPosition


class MockCell(Cell[int]):

    def eliminate_coefficients(self, other: 'MockCell'):
        if other.is_collapsed():
            super_position = self.super_position.difference(other.super_position)
            self._set_super_position(super_position)
        # Add adjacency-specific rules here

    def __repr__(self):
        return f'MockCell({self.super_position})'
