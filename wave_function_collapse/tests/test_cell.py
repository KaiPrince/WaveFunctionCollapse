from wave_function_collapse.cell import Cell
from wave_function_collapse.tests.mocks.mock_random_provider import MockRandomProvider


def test_collapse():
    # Arrange
    states = {1, 2, 3}
    random_provider = MockRandomProvider(lambda seq: seq[0], lambda seq: seq)
    cell = Cell(states, random_provider)

    # Act
    new_cell = cell.collapse()

    # Assert
    assert new_cell.super_position == {1}


def test_eliminate_coefficient():
    # Arrange
    cell = Cell({1, 2, 3})
    collapsed_cell = Cell({1})

    # Act
    new_cell = cell.eliminate_coefficients(collapsed_cell)

    # Assert
    assert new_cell.super_position == {2, 3}


def test_is_invalid():
    # Arrange
    cell = Cell(set())

    # Act
    result = cell.is_invalid()

    # Assert
    assert result is True


def test_is_invalid_has_states():
    # Arrange
    cell = Cell({1})

    # Act
    result = cell.is_invalid()

    # Assert
    assert result is False
