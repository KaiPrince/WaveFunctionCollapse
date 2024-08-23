from wave_function_collapse.cell import Cell
from wave_function_collapse.tests.mocks.mock_collapser import MockWaveFunction
from wave_function_collapse.tests.mocks.mock_random_provider import MockRandomProvider
from wave_function_collapse.wave_function_collapse import WaveFunctionCollapse


def test_solve_all_uncollapsed():
    # Arrange
    cell_random_provider = MockRandomProvider(lambda seq: seq[0], lambda seq: seq)
    int_random_provider = MockRandomProvider(lambda seq: seq[0], lambda seq: seq)
    wave_function = [Cell({1, 2, 3}, int_random_provider), Cell({1, 2, 3}, int_random_provider),
                     Cell({1, 2, 3}, int_random_provider)]
    collapser = MockWaveFunction(wave_function)
    director = WaveFunctionCollapse(cell_random_provider)

    # Act
    result: MockWaveFunction | None = director.solve(collapser)

    # Assert
    assert result is not None
    assert [x.super_position for x in result.wave_function] == [{1}, {2}, {3}]


def test_solve_all_uncollapsed_big():
    # Arrange
    states = {x for x in range(1, 10)}
    cell_random_provider = MockRandomProvider(lambda seq: seq[0], lambda seq: seq)
    int_random_provider = MockRandomProvider(lambda seq: sorted(seq)[0], lambda seq: seq)
    wave_function = [Cell(states, int_random_provider) for _ in range(1, 10)]
    collapser = MockWaveFunction(wave_function)
    director = WaveFunctionCollapse(cell_random_provider)

    # Act
    result: MockWaveFunction | None = director.solve(collapser)

    # Assert
    assert [x.super_position for x in result.wave_function] == [{x} for x in range(1, 10)]


def test_solve_invalid():
    # Arrange
    wave_function = [Cell({1, 2}), Cell({1, 2}), Cell({1, 2})]
    collapser = MockWaveFunction(wave_function)
    director = WaveFunctionCollapse()

    # Act
    result: MockWaveFunction | None = director.solve(collapser)

    # Assert
    assert result is None


def test_propagate_one_uncollapsed():
    # Arrange
    wave_function = [Cell({1, 2, 3}), Cell({1, 2, 3}), Cell({2})]
    collapser = MockWaveFunction(wave_function)
    director = WaveFunctionCollapse()

    # Act
    result: MockWaveFunction = director.propagate(wave_function[2], collapser)

    # Assert
    assert [x.super_position for x in result.wave_function] == [{1, 3}, {1, 3}, {2}]


def test_propagate_one_partially_collapsed():
    # Arrange
    wave_function = [Cell({3}), Cell({1, 2, 3}), Cell({2})]
    collapser = MockWaveFunction(wave_function)
    director = WaveFunctionCollapse()

    # Act
    result: MockWaveFunction = director.propagate(wave_function[2], collapser)

    # Assert
    assert [x.super_position for x in result.wave_function] == [{3}, {1, 3}, {2}]


def test_propagate_invalid():
    # Arrange
    wave_function = [Cell({1}), Cell({1, 2, 3}), Cell({1})]
    collapser = MockWaveFunction(wave_function)
    director = WaveFunctionCollapse()

    # Act
    result: MockWaveFunction = director.propagate(wave_function[0], collapser)

    # Assert
    assert [x.super_position for x in result.wave_function] == [{1}, {2, 3}, set()]
