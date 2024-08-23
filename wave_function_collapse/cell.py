from typing import TypeVar, Any

from wave_function_collapse.random_provider import RandomProvider

T_Coefficient = TypeVar("T_Coefficient")
T_SuperPosition = set[T_Coefficient]


# A Cell tracks the states of a single element and reacts to changes in other Cells
class Cell[T_Coefficient]:
    super_position: T_SuperPosition

    def __init__(self, super_position: T_SuperPosition, random_provider: RandomProvider[T_Coefficient] = None,
                 identifier: Any = None):
        if random_provider is None:
            random_provider = RandomProvider()
        self.random_provider = random_provider

        if identifier is None:
            identifier = id(self)
        self._identifier = identifier

        self.super_position = super_position

    def is_same(self, other: 'Cell[T_Coefficient]'):
        return self._identifier == other._identifier

    def collapse(self) -> 'Cell[T_Coefficient]':
        state = self.random_provider.choice(list(self.super_position))
        return Cell({state}, self.random_provider, self._identifier)

    def entropy(self) -> int:
        return len(self.super_position)

    def is_invalid(self) -> bool:
        return not any(self.super_position)

    def is_collapsed(self) -> bool:
        return self.entropy() == 1

    def eliminate_coefficients(self, other: 'Cell[T_Coefficient]') -> 'Cell[T_Coefficient]':
        if other.is_collapsed():
            super_position = self.super_position.difference(other.super_position)
            if self.super_position != super_position:
                return Cell(super_position, self.random_provider, self._identifier)

        # We use identity comparison to check if the cell changed
        return self  # Cell(self.super_position, self.random_provider, self._identifier)

    def __repr__(self):
        return f'Cell({self.super_position})'
