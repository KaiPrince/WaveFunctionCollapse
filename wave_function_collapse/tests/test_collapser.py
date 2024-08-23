from wave_function_collapse.cell import Cell
from wave_function_collapse.tests.mocks.mock_collapser import MockWaveFunction


def test_get_wave_function():
    # Arrange
    wave_function = [Cell({1, 2, 3}), Cell({1, 2, 3}), Cell({1, 2, 3})]
    collapser = MockWaveFunction(wave_function)

    # Act
    result = collapser.get_wave_function()

    # Assert
    assert result == wave_function


def test_get_influenced_cells():
    # Arrange
    wave_function = [Cell({1, 2, 3}), Cell({1, 2, 3}), Cell({1, 2, 3})]
    collapser = MockWaveFunction(wave_function)

    # Act
    result = collapser.get_influenced_cells(wave_function[0])

    # Assert
    assert result == [wave_function[1], wave_function[2]]


def test_propagate_one_uncollapsed():
    # Arrange
    wave_function = [Cell({1, 2, 3}), Cell({1, 2, 3}), Cell({2})]
    collapser = MockWaveFunction(wave_function)

    # Act
    result: MockWaveFunction = collapser.propagate(wave_function[2])

    # Assert
    assert [x.super_position for x in result.wave_function] == [{1, 3}, {1, 3}, {2}]


def test_propagate_one_partially_collapsed():
    # Arrange
    wave_function = [Cell({3}), Cell({1, 2, 3}), Cell({2})]
    collapser = MockWaveFunction(wave_function)

    # Act
    result: MockWaveFunction = collapser.propagate(wave_function[2])

    # Assert
    assert [x.super_position for x in result.wave_function] == [{3}, {1, 3}, {2}]


def test_propagate_invalid():
    # Arrange
    wave_function = [Cell({1}), Cell({1, 2, 3}), Cell({1})]
    collapser = MockWaveFunction(wave_function)

    # Act
    result: MockWaveFunction = collapser.propagate(wave_function[0])

    # Assert
    assert [x.super_position for x in result.wave_function] == [{1}, {2, 3}, set()]
