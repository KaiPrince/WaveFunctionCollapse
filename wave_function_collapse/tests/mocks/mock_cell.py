from wave_function_collapse.cell import Cell, T_SuperPosition


class MockCell(Cell[int]):
    super_position: T_SuperPosition
    history: list[T_SuperPosition]

    def __init__(self, super_position: T_SuperPosition):
        self.super_position = super_position
        self.history = []

    def collapse(self, state: int) -> None:
        self._set_super_position({state})

    def compute_possible_states(self) -> T_SuperPosition:
        return self.super_position

    def is_invalid(self) -> bool:
        return not any(self.super_position)

    def is_collapsed(self) -> bool:
        return len(self.super_position) == 1

    def eliminate_coefficients(self, other: 'MockCell'):
        if other.is_collapsed():
            super_position = self.super_position.difference(other.super_position)
            self._set_super_position(super_position)
        # Add adjacency-specific rules here

    def revert(self):
        if any(self.history):
            self.super_position = self.history.pop()

    def _set_super_position(self, super_position: T_SuperPosition):
        self.history.append(self.super_position)
        self.super_position = super_position

    def __repr__(self):
        return f'MockCell({self.super_position})'
