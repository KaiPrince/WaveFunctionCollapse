from wave_function_collapse.tests.mocks.mock_cell import MockCell
from wave_function_collapse.tests.mocks.mock_collapser import MockCollapser
from wave_function_collapse.wave_function_collapse import WaveFunctionCollapse


def test_one_uncollapsed():
    # Arrange
    wave_function = [MockCell({1}), MockCell({2}), MockCell({1, 2, 3})]
    collapser = MockCollapser(wave_function)
    director = WaveFunctionCollapse(collapser)

    # Act
    result = director.try_solve()

    # Assert
    assert result is True


def test_all_uncollapsed():
    # Arrange
    wave_function = [MockCell({1, 2, 3}), MockCell({1, 2, 3}), MockCell({1, 2, 3})]
    collapser = MockCollapser(wave_function)
    director = WaveFunctionCollapse(collapser)

    # Act
    result = director.try_solve()

    # Assert
    assert result is True
