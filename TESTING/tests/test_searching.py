"""Behavioural tests for all five searching algorithms.

Expected results come from Python's trusted ``list.index``, ``in`` and ``bisect``.
"""

import bisect
import math
import random

import pytest

from algovision_learning import (
    UnsortedInputError,
    binary_search,
    exponential_search,
    interpolation_search,
    jump_search,
    linear_search,
)

SORTED_SEARCHERS = {
    "binary": binary_search,
    "jump": jump_search,
    "interpolation": interpolation_search,
    "exponential": exponential_search,
}
ALL_SEARCHERS = {"linear": linear_search, **SORTED_SEARCHERS}

any_search = pytest.mark.parametrize("name", list(ALL_SEARCHERS))
sorted_search = pytest.mark.parametrize("name", list(SORTED_SEARCHERS))


def search(name, data, target, **kwargs):
    return ALL_SEARCHERS[name](data, target, **kwargs)


def check(name, data, target):
    """Assert the result is correct per Python's own semantics."""
    result = search(name, data, target)
    if target in data:
        assert 0 <= result < len(data), (name, data, target, result)
        assert data[result] == target
        if name == "linear":
            assert result == list(data).index(target)  # first occurrence
        else:
            low = bisect.bisect_left(data, target)
            high = bisect.bisect_right(data, target)
            assert low <= result < high
    else:
        assert result == -1, (name, data, target, result)
    return result


# --------------------------------------------------------------------------- basics


@any_search
def test_empty_list(name):
    assert search(name, [], 5) == -1


@any_search
def test_single_element(name):
    assert search(name, [5], 5) == 0
    assert search(name, [5], 4) == -1
    assert search(name, [5], 6) == -1
    assert search(name, [-5], -5) == 0


@any_search
def test_two_elements(name):
    assert search(name, [1, 3], 1) == 0
    assert search(name, [1, 3], 3) == 1
    assert search(name, [1, 3], 2) == -1


@any_search
@pytest.mark.parametrize(
    "data",
    [
        [1, 2, 3, 4, 5],
        [2, 5, 8, 12, 16, 23, 38, 56, 72, 91],
        [-10, -5, -3, 0, 4, 9],
        [-1, -1, -1, -1],
        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89],
        [1.5, 2.5, 3.5, 10.25],
        [1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 4],
        list(range(0, 200, 3)),
    ],
    ids=lambda d: repr(d)[:40],
)
def test_every_present_and_missing_target(name, data):
    lo, hi = min(data), max(data)
    targets = set(data) | {lo - 1, hi + 1, lo - 0.5, hi + 0.5, 10**9, -(10**9)}
    targets |= {v + 0.5 for v in data}
    for target in targets:
        check(name, data, target)


@any_search
def test_first_middle_last_element(name):
    data = list(range(0, 100, 2))
    for target in (data[0], data[len(data) // 2], data[-1]):
        assert search(name, data, target) == data.index(target)


@any_search
def test_missing_targets_below_between_and_above(name):
    data = [10, 20, 30, 40, 50]
    assert search(name, data, 5) == -1
    assert search(name, data, 25) == -1
    assert search(name, data, 55) == -1


@any_search
def test_negative_values(name):
    data = [-50, -20, -20, -7, -1, 0, 3]
    for target in data + [-100, -8, 100]:
        check(name, data, target)


@any_search
def test_int_and_float_targets_compare_by_value(name):
    assert search(name, [1, 2, 3], 2.0) == 1
    assert search(name, [1.0, 2.0, 3.0], 2) == 1
    assert search(name, [1, 2, 3], 2.5) == -1


@any_search
def test_tuple_input_accepted(name):
    assert search(name, (1, 3, 5, 7), 5) == 2


@any_search
def test_all_equal_values(name):
    data = [4] * 20
    assert data[search(name, data, 4)] == 4
    assert search(name, data, 3) == -1
    assert search(name, data, 5) == -1


def test_linear_search_returns_first_duplicate():
    assert linear_search([7, 3, 9, 3, 1], 3) == 1
    assert linear_search([2, 2, 2], 2) == 0


@sorted_search
def test_duplicates_return_some_matching_index(name):
    data = [1, 2, 2, 2, 2, 2, 3]
    result = search(name, data, 2)
    assert data[result] == 2


def test_linear_search_works_on_unsorted_data():
    data = [9, -1, 4, 4, 0, 7]
    for target in data + [100, -100]:
        check("linear", data, target)


@any_search
def test_randomised_against_python(name):
    rng = random.Random(20260421)
    for _ in range(300):
        size = rng.randint(0, 50)
        data = sorted(rng.randint(-40, 40) for _ in range(size))
        target = rng.randint(-45, 45)
        check(name, data, target)


@sorted_search
def test_randomised_float_data(name):
    rng = random.Random(3)
    for _ in range(100):
        data = sorted(rng.uniform(-100, 100) for _ in range(rng.randint(0, 60)))
        targets = data[:5] + [rng.uniform(-110, 110) for _ in range(5)]
        for target in targets:
            check(name, data, target)


@sorted_search
def test_interpolation_hostile_distribution(name):
    """Heavily skewed values: result must stay correct (only speed suffers)."""
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10**12]
    for target in data + [0, 11, 10**11, 10**12 + 1]:
        check(name, data, target)


@sorted_search
def test_huge_integers_are_exact(name):
    data = [10**30, 10**30 + 1, 10**30 + 2, 10**30 + 10]
    assert search(name, data, 10**30 + 2) == 2
    assert search(name, data, 10**30 + 3) == -1


# ------------------------------------------------------------- mutation behaviour


@any_search
def test_input_is_not_mutated(name):
    data = [1, 3, 3, 5, 8]
    snapshot = list(data)
    search(name, data, 5)
    search(name, data, 4)
    assert data == snapshot


@any_search
def test_returns_plain_int(name):
    assert type(search(name, [1, 2, 3], 2)) is int
    assert type(search(name, [1, 2, 3], 9)) is int


# ------------------------------------------------------------------------ larger inputs


@any_search
def test_larger_sorted_input(name):
    rng = random.Random(11)
    data = sorted(rng.randint(-100_000, 100_000) for _ in range(5000))
    present = rng.sample(data, 100)
    absent = [t for t in (rng.randint(-100_050, 100_050) for _ in range(150)) if t not in set(data)]
    for target in present + absent:
        check(name, data, target)


@sorted_search
def test_large_uniform_data(name):
    data = list(range(0, 2_000_000, 2))
    for target in (0, 2, 1_999_998, 1_000_000, 1_234_568, 1, 1_999_999, -4, 3_000_000):
        assert search(name, data, target, validate_sorted=False) == (
            data.index(target) if target in (0, 2, 1_999_998, 1_000_000, 1_234_568) else -1
        )


# ------------------------------------------------ complexity guard via access counting


class CountingList(list):
    """List that counts element reads made through indexing."""

    reads = 0

    def __getitem__(self, index):
        type(self).reads += 1
        return super().__getitem__(index)


def count_reads(func, data, target):
    CountingList.reads = 0
    result = func(CountingList(data), target, validate_sorted=False)
    return result, CountingList.reads


def test_binary_search_reads_are_logarithmic():
    n = 1_000_000
    data = list(range(n))
    for target in (0, n - 1, n // 3, -1, n):
        _, reads = count_reads(binary_search, data, target)
        assert reads <= 3 * math.ceil(math.log2(n)) + 3  # about 60 for n = 1e6


def test_exponential_search_reads_are_logarithmic_in_target_position():
    n = 1_000_000
    data = list(range(n))
    _, near_reads = count_reads(exponential_search, data, 3)
    _, far_reads = count_reads(exponential_search, data, n - 1)
    assert near_reads <= 12  # target near the front is found in a handful of reads
    assert far_reads <= 6 * math.ceil(math.log2(n))


def test_jump_search_reads_are_about_square_root():
    n = 1_000_000
    data = list(range(n))
    for target in (0, n - 1, n // 2, n // 3, n):
        _, reads = count_reads(jump_search, data, target)
        assert reads <= 3 * math.isqrt(n)  # about 3000, far below n


def test_interpolation_search_is_very_fast_on_uniform_data():
    n = 1_000_000
    data = list(range(0, 3 * n, 3))
    for target in (0, 3 * (n - 1), 3 * 123_456, 3 * 123_456 + 1, 2):
        _, reads = count_reads(interpolation_search, data, target)
        assert reads <= 20  # a handful of probes; binary search needs ~20 + overhead


def test_interpolation_search_degrades_on_skewed_data():
    """Documents the O(n) worst case.

    A huge outlier at the end squashes every estimate onto ``low``, so each probe
    only advances by one element (a linear scan) while binary search needs ~8.
    """
    n = 200
    data = list(range(1, n + 1)) + [10**12]
    result, reads = count_reads(interpolation_search, data, n)
    assert result == n - 1
    assert reads > n // 2  # linear behaviour, far above log2(n) probes


def test_linear_search_reads_are_linear():
    n = 5000
    data = list(range(n))
    CountingList.reads = 0
    assert linear_search(CountingList(data), n - 1) == n - 1
    assert CountingList.reads == n
    CountingList.reads = 0
    assert linear_search(CountingList(data), 0) == 0
    assert CountingList.reads == 1  # best case O(1)


# -------------------------------------------------------- sorted precondition handling


@sorted_search
def test_unsorted_input_raises_by_default(name):
    with pytest.raises(UnsortedInputError):
        search(name, [3, 1, 2], 2)


@sorted_search
def test_unsorted_error_is_a_value_error(name):
    with pytest.raises(ValueError):
        search(name, [2, 1], 1)


@sorted_search
def test_unsorted_error_names_the_offending_position(name):
    with pytest.raises(UnsortedInputError, match=r"data\[1\]=5 > data\[2\]=4"):
        search(name, [1, 5, 4, 9], 4)


@sorted_search
def test_validation_catches_unsorted_even_when_target_is_missing_or_data_empty_ok(name):
    with pytest.raises(UnsortedInputError):
        search(name, [5, 4], 100)
    assert search(name, [], 1) == -1  # empty list is trivially sorted


@sorted_search
def test_duplicates_in_sorted_input_are_allowed(name):
    assert search(name, [1, 1, 2, 2, 3], 3) == 4


@sorted_search
def test_validate_sorted_false_skips_the_check_and_still_terminates(name):
    unsorted = [5, 1, 4, 2, 3, 9, 0]
    for target in range(-1, 11):
        result = search(name, unsorted, target, validate_sorted=False)
        assert result == -1 or unsorted[result] == target  # never a wrong index


@sorted_search
def test_validate_sorted_false_is_correct_on_sorted_data(name):
    data = [1, 3, 5, 7, 9, 11]
    for target in data + [0, 4, 12]:
        expected = data.index(target) if target in data else -1
        assert search(name, data, target, validate_sorted=False) == expected


def test_linear_search_does_not_require_sorted_input():
    assert linear_search([3, 1, 2], 2) == 2  # no UnsortedInputError


def test_linear_search_has_no_validate_sorted_parameter():
    with pytest.raises(TypeError):
        linear_search([1, 2, 3], 2, validate_sorted=False)
