from abc import ABC, abstractmethod
from typing import TypeVar

T_Coefficient = TypeVar("T_Coefficient")
T_SuperPosition = set[T_Coefficient]


# A Cell tracks the states of a single element and reacts to changes in other Cells
class Cell[T_Coefficient](ABC):
    super_position: T_SuperPosition
    history: list[T_SuperPosition]

    def __init__(self, super_position: T_SuperPosition):
        self.super_position = super_position
        self.history = []

    def collapse(self, state: T_Coefficient) -> None:
        self._set_super_position({state})

    def compute_possible_states(self) -> T_SuperPosition:
        return self.super_position

    def entropy(self) -> int:
        return len(self.super_position)

    def is_invalid(self) -> bool:
        return not any(self.super_position)

    def is_collapsed(self) -> bool:
        return len(self.super_position) == 1

    def eliminate_coefficients(self, other: 'Cell[T_Coefficient]'):
        if other.is_collapsed():
            super_position = self.super_position.difference(other.super_position)
            self._set_super_position(super_position)

    def revert(self):
        if any(self.history):
            self.super_position = self.history.pop()

    def _set_super_position(self, super_position: T_SuperPosition):
        self.history.append(self.super_position)
        self.super_position = super_position
