from simple_terrain.terrain_value import TerrainValue


class Water(TerrainValue):
    def is_land(self) -> bool:
        return False

    def is_mountain(self) -> bool:
        return False

    def is_water(self) -> bool:
        return True

    def __repr__(self):
        return '~'
