from wave_function_collapse.tests.mocks.mock_cell import MockCell
from wave_function_collapse.tests.mocks.mock_collapser import MockCollapser
from wave_function_collapse.tests.mocks.mock_random_provider import MockRandomProvider
from wave_function_collapse.wave_function_collapse import WaveFunctionCollapse


def test_solve_one_uncollapsed():
    # Arrange
    wave_function = [MockCell({1}), MockCell({2}), MockCell({1, 2, 3})]
    collapser = MockCollapser(wave_function)
    director = WaveFunctionCollapse(collapser)

    # Act
    result = director.try_solve()

    # Assert
    assert result is True
    assert wave_function[0].super_position == {1}
    assert wave_function[1].super_position == {2}
    assert wave_function[2].super_position == {3}


def test_solve_all_uncollapsed():
    # Arrange
    wave_function = [MockCell({1, 2, 3}), MockCell({1, 2, 3}), MockCell({1, 2, 3})]
    collapser = MockCollapser(wave_function)
    random_provider = MockRandomProvider(lambda seq: seq[0], lambda seq: seq)
    director = WaveFunctionCollapse(collapser, random_provider)

    # Act
    result = director.try_solve()

    # Assert
    assert result is True
    assert wave_function[0].super_position == {1}
    assert wave_function[1].super_position == {2}
    assert wave_function[2].super_position == {3}


def test_solve_all_uncollapsed_big():
    # Arrange
    states = {x for x in range(1, 10)}
    wave_function = [MockCell(states), MockCell(states), MockCell(states), MockCell(states),
                     MockCell(states), MockCell(states), MockCell(states), MockCell(states),
                     MockCell(states)]
    collapser = MockCollapser(wave_function)
    random_provider = MockRandomProvider(lambda seq: seq[0], lambda seq: seq)
    director = WaveFunctionCollapse(collapser, random_provider)

    # Act
    result = director.try_solve()

    # Assert
    assert result is True
    for i in states:
        assert wave_function[i - 1].super_position == {i}


def test_solve_invalid():
    # Arrange
    wave_function = [MockCell({1, 2}), MockCell({1, 2}), MockCell({1, 2})]
    collapser = MockCollapser(wave_function)
    director = WaveFunctionCollapse(collapser)

    # Act
    result = director.try_solve()

    # Assert
    assert result is False
    assert wave_function[0].super_position == {1, 2}
    assert wave_function[1].super_position == {1, 2}
    assert wave_function[2].super_position == {1, 2}


def test_observe_one_uncollapsed():
    # Arrange
    wave_function = [MockCell({1, 2, 3}), MockCell({1, 2, 3}), MockCell({1, 2, 3})]
    collapser = MockCollapser(wave_function)
    random_provider = MockRandomProvider(lambda seq: seq[0], lambda seq: seq)
    director = WaveFunctionCollapse(collapser, random_provider)

    # Act
    result = director.try_observe_cell(wave_function[1])

    # Assert
    assert result is True
    assert wave_function[0].super_position == {2, 3}
    assert wave_function[1].super_position == {1}
    assert wave_function[2].super_position == {2, 3}


def test_observe_one_partially_collapsed():
    # Arrange
    wave_function = [MockCell({1}), MockCell({2, 3}), MockCell({2, 3})]
    collapser = MockCollapser(wave_function)
    random_provider = MockRandomProvider(lambda seq: seq[0], lambda seq: seq)
    director = WaveFunctionCollapse(collapser, random_provider)

    # Act
    result = director.try_observe_cell(wave_function[2])

    # Assert
    assert result is True
    assert wave_function[0].super_position == {1}
    assert wave_function[1].super_position == {3}
    assert wave_function[2].super_position == {2}


def test_observe_invalid():
    # Arrange
    wave_function = [MockCell({1}), MockCell({2}), MockCell({1, 2})]
    collapser = MockCollapser(wave_function)
    random_provider = MockRandomProvider(lambda seq: seq[0], lambda seq: seq)
    director = WaveFunctionCollapse(collapser, random_provider)

    # Act
    result = director.try_observe_cell(wave_function[2])

    # Assert
    assert result is False
    assert wave_function[0].super_position == {1}
    assert wave_function[1].super_position == {2}
    assert wave_function[2].super_position == {1, 2}


def test_propogate_one_uncollapsed():
    # Arrange
    wave_function = [MockCell({1, 2, 3}), MockCell({1, 2, 3}), MockCell({2})]
    collapser = MockCollapser(wave_function)
    director = WaveFunctionCollapse(collapser)

    # Act
    result = director.try_propagate(wave_function[2])

    # Assert
    assert result is True
    assert wave_function[0].super_position == {1, 3}
    assert wave_function[1].super_position == {1, 3}
    assert wave_function[2].super_position == {2}


def test_propogate_one_partially_collapsed():
    # Arrange
    wave_function = [MockCell({3}), MockCell({1, 2, 3}), MockCell({2})]
    collapser = MockCollapser(wave_function)
    director = WaveFunctionCollapse(collapser)

    # Act
    result = director.try_propagate(wave_function[2])

    # Assert
    assert result is True
    assert wave_function[0].super_position == {3}
    assert wave_function[1].super_position == {1}
    assert wave_function[2].super_position == {2}


def test_propogate_invalid():
    # Arrange
    wave_function = [MockCell({1}), MockCell({1, 2, 3}), MockCell({1})]
    collapser = MockCollapser(wave_function)
    director = WaveFunctionCollapse(collapser)

    # Act
    result = director.try_propagate(wave_function[0])

    # Assert
    assert result is False
    assert wave_function[0].super_position == {1}
    assert wave_function[1].super_position == {1, 2, 3}
    assert wave_function[2].super_position == {1}
