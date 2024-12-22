from simple_terrain.land import Land
from simple_terrain.mountain import Mountain
from simple_terrain.terrain_cell import TerrainCell
from simple_terrain.terrain_value import TerrainValue
from simple_terrain.water import Water
from simple_terrain.wave_function import SimpleTerrainWaveFunction
from wave_function_collapse.wave_function_collapse import WaveFunctionCollapse

empty_map = [[TerrainCell({Water(), Land(), Mountain()}) for j in range(5)] for i in range(5)]

wave_function = SimpleTerrainWaveFunction(empty_map, 5, 5)

wave_function_collapse = WaveFunctionCollapse()

solution: SimpleTerrainWaveFunction | None = wave_function_collapse.solve(wave_function)

for row in solution.map:
    for cell in row:
        cell_value: TerrainValue = list(cell.super_position)[0]
        # char = cell_value.__repr__()
        print(cell_value, end='')
    print()
