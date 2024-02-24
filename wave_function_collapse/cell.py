from abc import ABC, abstractmethod
from typing import TypeVar

T_Coefficient = TypeVar("T_Coefficient")
T_SuperPosition = set[T_Coefficient]


# A Cell tracks the states of a single element and reacts to changes in other Cells
class Cell[T_Coefficient](ABC):
    @abstractmethod
    def compute_possible_states(self) -> T_SuperPosition:
        pass

    @abstractmethod
    def collapse(self, state: T_Coefficient) -> None:
        pass

    @abstractmethod
    def is_invalid(self) -> bool:
        pass

    @abstractmethod
    def eliminate_coefficients(self, other: 'Cell[T_Coefficient]'):
        pass

    @abstractmethod
    def revert(self):
        pass
