from wave_function_collapse.tests.mocks.mock_cell import MockCell


def test_compute_possible_states():
    # Arrange
    cell = MockCell({1, 2, 3})

    # Act
    result = cell.compute_possible_states()

    # Assert
    assert result == {1, 2, 3}


def test_collapse():
    # Arrange
    states = {1, 2, 3}
    cell = MockCell(states)

    # Act
    cell.collapse(1)

    # Assert
    assert cell.super_position == {1}


def test_revert():
    # Arrange
    cell = MockCell({1, 2, 3})
    cell.collapse(1)

    # Act
    cell.revert()

    # Assert
    assert cell.super_position == {1, 2, 3}


def test_revert_without_history():
    # Arrange
    cell = MockCell({1, 2, 3})

    # Act
    cell.revert()

    # Assert
    assert cell.super_position == {1, 2, 3}


def test_eliminate_coefficient():
    # Arrange
    cell = MockCell({1, 2, 3})
    collapsed_cell = MockCell({1})

    # Act
    cell.eliminate_coefficients(collapsed_cell)

    # Assert
    assert cell.super_position == {2, 3}


def test_is_invalid():
    # Arrange
    cell = MockCell(set())

    # Act
    result = cell.is_invalid()

    # Assert
    assert result is True


def test_is_invalid_has_states():
    # Arrange
    cell = MockCell({1})

    # Act
    result = cell.is_invalid()

    # Assert
    assert result is False
