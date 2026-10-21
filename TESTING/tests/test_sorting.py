"""Behavioural tests for all five sorting algorithms.

Every algorithm is checked against Python's trusted ``sorted()``.
"""

import itertools
import random

import pytest

from algovision_learning import (
    bubble_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
)

SORTERS = {
    "bubble": bubble_sort,
    "selection": selection_sort,
    "insertion": insertion_sort,
    "merge": merge_sort,
    "quick": quick_sort,
}
STABLE = ["bubble", "insertion", "merge"]
UNSTABLE = ["selection", "quick"]

sorter = pytest.mark.parametrize("name", list(SORTERS))


def run(name, data):
    return SORTERS[name](data)


# --------------------------------------------------------------------------- basics


@sorter
@pytest.mark.parametrize(
    "data",
    [
        [],
        [7],
        [-7],
        [0],
        [2, 1],
        [1, 2],
        [3, 1, 2],
        [5, 2, 9, 1, 5, 6],
        [1, 1, 1, 1],
        [2, 1, 2, 1, 2, 1],
        [-5, -1, -10, -3],
        [-2, 0, 3, -1, 0, 2],
        [3.5, -1.25, 2.0, 0.0, 2.0],
        [1, 2.5, -3, 0.5, 4],
        [10**18, -(10**18), 0, 10**18],
    ],
    ids=lambda d: repr(d)[:40],
)
def test_matches_python_sorted(name, data):
    assert run(name, data) == sorted(data)


@sorter
def test_empty_and_single_element(name):
    assert run(name, []) == []
    assert run(name, [42]) == [42]


@sorter
def test_duplicates_and_negatives(name):
    data = [4, -2, 4, 0, -2, 7, 0, -9, 4]
    assert run(name, data) == [-9, -2, -2, 0, 0, 4, 4, 4, 7]


@sorter
def test_already_sorted_and_reverse_sorted(name):
    ascending = list(range(-20, 21))
    assert run(name, ascending) == ascending
    assert run(name, ascending[::-1]) == ascending


@sorter
def test_all_equal(name):
    assert run(name, [5] * 50) == [5] * 50


@sorter
def test_every_permutation_of_small_inputs(name):
    for size in range(0, 7):
        for perm in itertools.permutations(range(size)):
            assert run(name, list(perm)) == list(range(size))


@sorter
def test_every_small_input_with_duplicates(name):
    for size in range(0, 6):
        for combo in itertools.product([-1, 0, 2], repeat=size):
            assert run(name, list(combo)) == sorted(combo)


@sorter
def test_randomised_against_sorted(name):
    rng = random.Random(20260421)
    for _ in range(200):
        size = rng.randint(0, 60)
        data = [rng.randint(-30, 30) for _ in range(size)]
        assert run(name, data) == sorted(data)


@sorter
def test_float_values(name):
    rng = random.Random(7)
    data = [rng.uniform(-1000, 1000) for _ in range(120)]
    assert run(name, data) == sorted(data)


@sorter
def test_tuple_input_accepted(name):
    assert run(name, (3, 1, 2, 1)) == [1, 1, 2, 3]


# ------------------------------------------------------------------ mutation behaviour


@sorter
def test_input_list_is_not_mutated(name):
    data = [9, 3, 7, 3, -1, 0]
    snapshot = list(data)
    run(name, data)
    assert data == snapshot


@sorter
def test_returns_new_list_even_when_already_sorted(name):
    data = [1, 2, 3]
    result = run(name, data)
    assert result == data
    assert result is not data


@sorter
def test_returns_new_list_for_trivial_inputs(name):
    for data in ([], [1]):
        result = run(name, data)
        assert result == data
        assert result is not data


@sorter
def test_result_is_independent_of_input(name):
    data = [3, 2, 1]
    result = run(name, data)
    result.append(99)
    data.append(-1)
    assert run(name, [3, 2, 1]) == [1, 2, 3]
    assert data == [3, 2, 1, -1]


@sorter
def test_repeated_calls_give_same_result(name):
    data = [5, 1, 4, 1, 5]
    assert run(name, data) == run(name, data)


# ------------------------------------------------------------------------ larger inputs


@sorter
def test_larger_random_input(name):
    rng = random.Random(99)
    data = [rng.randint(-10_000, 10_000) for _ in range(1500)]
    assert run(name, data) == sorted(data)


@sorter
def test_larger_sorted_and_reverse_sorted(name):
    ascending = list(range(1500))
    assert run(name, ascending) == ascending
    assert run(name, ascending[::-1]) == ascending


@sorter
def test_larger_input_with_many_duplicates(name):
    rng = random.Random(5)
    data = [rng.randint(0, 5) for _ in range(1500)]
    assert run(name, data) == sorted(data)


@sorter
def test_larger_all_equal(name):
    assert run(name, [3] * 1000) == [3] * 1000


@pytest.mark.parametrize("name", ["merge", "quick"])
def test_fast_sorts_handle_large_input(name):
    rng = random.Random(1)
    data = [rng.randint(-10**6, 10**6) for _ in range(50_000)]
    assert run(name, data) == sorted(data)


@pytest.mark.parametrize("name", ["merge", "quick"])
def test_fast_sorts_handle_large_sorted_and_reverse(name):
    ascending = list(range(20_000))
    assert run(name, ascending) == ascending
    assert run(name, ascending[::-1]) == ascending


def test_quick_sort_does_not_overflow_recursion_stack():
    """Organ-pipe data is a bad case for naive pivots; depth must stay O(log n)."""
    data = list(range(5000)) + list(range(5000, 0, -1))
    assert quick_sort(data) == sorted(data)


# ------------------------------------------------------------------------- stability


def _signature(values):
    """Equal values with different types (1 vs 1.0) reveal element order."""
    return [(type(v).__name__, v) for v in values]


@pytest.mark.parametrize("name", STABLE)
def test_stable_sorts_keep_equal_elements_in_original_order(name):
    for size in range(2, 7):
        for combo in itertools.product([1, 1.0, 2, 2.0], repeat=size):
            data = list(combo)
            assert _signature(run(name, data)) == _signature(sorted(data)), data


@pytest.mark.parametrize(
    "name, data",
    [("selection", [2, 2.0, 1]), ("quick", [1, 1, 1.0])],
)
def test_documented_unstable_sorts_really_reorder_equal_elements(name, data):
    result = run(name, data)
    assert result == sorted(data)  # still correctly sorted
    assert _signature(result) != _signature(sorted(data))  # but order of equals changed
