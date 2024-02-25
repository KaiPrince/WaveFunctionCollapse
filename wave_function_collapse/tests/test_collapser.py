from wave_function_collapse.tests.mocks.mock_cell import MockCell
from wave_function_collapse.tests.mocks.mock_collapser import MockCollapser


def test_get_wave_function():
    # Arrange
    wave_function = [MockCell({1, 2, 3}), MockCell({1, 2, 3}), MockCell({1, 2, 3})]
    collapser = MockCollapser(wave_function)

    # Act
    result = collapser.get_wave_function()

    # Assert
    assert result == wave_function


def test_get_influenced_cells():
    # Arrange
    wave_function = [MockCell({1, 2, 3}), MockCell({1, 2, 3}), MockCell({1, 2, 3})]
    collapser = MockCollapser(wave_function)

    # Act
    result = collapser.get_influenced_cells(wave_function[0])

    # Assert
    assert result == [wave_function[1], wave_function[2]]
