import random
from typing import Sequence


class RandomProvider[T]:
    def choice(self, seq: Sequence[T]) -> T:
        return random.choice(seq)

    def shuffle(self, seq: Sequence[T]):
        return random.sample(seq, k=len(seq))
