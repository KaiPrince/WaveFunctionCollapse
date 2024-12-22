from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class TerrainValue(ABC):
    @abstractmethod
    def is_land(self) -> bool:
        pass

    @abstractmethod
    def is_mountain(self) -> bool:
        pass

    @abstractmethod
    def is_water(self) -> bool:
        pass
