from wave_function_collapse.tests.mocks.mock_cell import MockCell


def test_compute_possible_states():
    # Arrange
    states = {1, 2, 3}
    cell = MockCell(states)

    # Act
    result = cell.compute_possible_states()

    # Assert
    assert result == states


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
    states = {1, 2, 3}
    cell = MockCell(states)
    cell.collapse(1)

    # Act
    cell.revert()

    # Assert
    assert cell.super_position == states


def test_revert_without_history():
    # Arrange
    states = {1, 2, 3}
    cell = MockCell(states)

    # Act
    cell.revert()

    # Assert
    assert cell.super_position == states


def test_eliminate_coefficient():
    # Arrange
    states = {1, 2, 3}
    cell = MockCell(states)
    collapsed_cell = MockCell({1})

    # Act
    cell.eliminate_coefficients(collapsed_cell)

    # Assert
    assert cell.super_position == {2, 3}


def test_eliminate_coefficients():
    # Arrange
    states = {1, 2, 3}
    cell = MockCell(states)
    pruned_cell = MockCell({1, 2})

    # Act
    cell.eliminate_coefficients(pruned_cell)

    # Assert
    assert cell.super_position == {3}


def test_eliminate_coefficients_all():
    # Arrange
    states = {1, 2, 3}
    cell = MockCell(states)
    collapsed_cell = MockCell({1, 2, 3})

    # Act
    cell.eliminate_coefficients(collapsed_cell)

    # Assert
    assert cell.super_position == set()


def test_is_invalid():
    # Arrange
    states = set()
    cell = MockCell(states)

    # Act
    result = cell.is_invalid()

    # Assert
    assert result is True


def test_is_invalid_has_states():
    # Arrange
    states = {1}
    cell = MockCell(states)

    # Act
    result = cell.is_invalid()

    # Assert
    assert result is False
