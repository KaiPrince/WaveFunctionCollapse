from simple_terrain.mountain import Mountain
from simple_terrain.terrain_value import TerrainValue
from simple_terrain.water import Water
from wave_function_collapse.cell import Cell, T_SuperPosition


class TerrainCell(Cell[TerrainValue]):
    def eliminate_coefficients(self, other: 'TerrainCell') -> 'TerrainCell':
        if other.is_collapsed():
            other_value: TerrainValue = list(other.super_position)[0]
            if other_value.is_mountain():
                super_position = self.super_position.difference({Water()})
                return self._copy(super_position)
            if other_value.is_water():
                super_position = self.super_position.difference({Mountain()})
                return self._copy(super_position)

        return self

    def _copy(self, super_position: T_SuperPosition):
        return TerrainCell(super_position, self.random_provider, self._identifier)
