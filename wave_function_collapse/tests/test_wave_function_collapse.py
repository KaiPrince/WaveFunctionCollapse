from wave_function_collapse.cell import Cell
from wave_function_collapse.tests.mocks.mock_collapser import MockCollapser
from wave_function_collapse.tests.mocks.mock_random_provider import MockRandomProvider
from wave_function_collapse.wave_function_collapse import WaveFunctionCollapse


def test_solve_all_uncollapsed():
    # Arrange
    random_provider = MockRandomProvider(lambda seq: seq[0], lambda seq: seq)
    wave_function = [Cell({1, 2, 3}, random_provider), Cell({1, 2, 3}, random_provider),
                     Cell({1, 2, 3}, random_provider)]
    collapser = MockCollapser(wave_function)
    director = WaveFunctionCollapse(collapser, random_provider)

    # Act
    result = director.solve()

    # Assert
    assert result is not None
    assert [x.super_position for x in result] == [{1}, {2}, {3}]


def test_solve_all_uncollapsed_big():
    # Arrange
    states = {x for x in range(1, 10)}
    random_provider = MockRandomProvider(lambda seq: seq[0], lambda seq: seq)
    wave_function = [Cell(states, random_provider) for _ in range(1, 10)]
    collapser = MockCollapser(wave_function)
    director = WaveFunctionCollapse(collapser, random_provider)

    # Act
    result = director.solve()

    # Assert
    assert [x.super_position for x in result] == [{x} for x in range(1, 10)]


def test_solve_invalid():
    # Arrange
    wave_function = [Cell({1, 2}), Cell({1, 2}), Cell({1, 2})]
    collapser = MockCollapser(wave_function)
    director = WaveFunctionCollapse(collapser)

    # Act
    result = director.solve()

    # Assert
    assert result is None


def test_propagate_one_uncollapsed():
    # Arrange
    wave_function = [Cell({1, 2, 3}), Cell({1, 2, 3}), Cell({2})]
    collapser = MockCollapser(wave_function)
    director = WaveFunctionCollapse(collapser)

    # Act
    result = director.propagate(wave_function[2], wave_function)

    # Assert
    assert [x.super_position for x in result] == [{1, 3}, {1, 3}, {2}]


def test_propagate_one_partially_collapsed():
    # Arrange
    wave_function = [Cell({3}), Cell({1, 2, 3}), Cell({2})]
    collapser = MockCollapser(wave_function)
    director = WaveFunctionCollapse(collapser)

    # Act
    result = director.propagate(wave_function[2], wave_function)

    # Assert
    assert [x.super_position for x in result] == [{3}, {1, 3}, {2}]


def test_propagate_invalid():
    # Arrange
    wave_function = [Cell({1}), Cell({1, 2, 3}), Cell({1})]
    collapser = MockCollapser(wave_function)
    director = WaveFunctionCollapse(collapser)

    # Act
    result = director.propagate(wave_function[0], wave_function)

    # Assert
    assert [x.super_position for x in result] == [{1}, {2, 3}, set()]
