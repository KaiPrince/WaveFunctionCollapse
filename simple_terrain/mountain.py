from simple_terrain.terrain_value import TerrainValue


class Mountain(TerrainValue):
    def is_land(self) -> bool:
        return False

    def is_mountain(self) -> bool:
        return True

    def is_water(self) -> bool:
        return False

    def __repr__(self):
        return '^'
