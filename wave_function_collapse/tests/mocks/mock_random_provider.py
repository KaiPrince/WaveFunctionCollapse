from typing import Callable, Sequence

from wave_function_collapse.cell import Cell
from wave_function_collapse.random_provider import RandomProvider


class MockRandomProvider(RandomProvider[Cell]):
    def __init__(self, choice_func: Callable[[Sequence[Cell]], Cell],
                 shuffle_func: Callable[[Sequence[Cell]], Sequence[Cell]]):
        self.choice_func = choice_func
        self.shuffle_func = shuffle_func

    def choice(self, seq: Sequence[Cell]) -> Cell:
        result = self.choice_func(seq)
        return result

    def shuffle(self, seq: Sequence[Cell]) -> Sequence[Cell]:
        return self.shuffle_func(seq)
