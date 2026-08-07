
from texas_hold_em import unique_list
import pylint
import pytest


def test_already_unique_ints():
    test_list = [1, 2, 3]

    assert unique_list(test_list) == test_list


def test_not_unique_ints():
    test_list = [1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 777, 7, 5, 5]

    assert unique_list(test_list) == [1, 2, 3, 4, 777, 7, 5]


def test_unique_mixed_data():
    test_list = [1, "1", "a", "A", 1.0]

    assert unique_list(test_list) == test_list
