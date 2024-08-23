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
