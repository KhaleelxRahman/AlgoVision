"""Invalid-input behaviour, applied uniformly to all ten algorithms."""

import pytest

from algovision_learning import (
    UnsortedInputError,
    binary_search,
    bubble_sort,
    exponential_search,
    insertion_sort,
    interpolation_search,
    jump_search,
    linear_search,
    merge_sort,
    quick_sort,
    selection_sort,
)

SORTERS = [bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort]
SEARCHERS = [linear_search, binary_search, jump_search, interpolation_search, exponential_search]

sorters = pytest.mark.parametrize("func", SORTERS, ids=lambda f: f.__name__)
searchers = pytest.mark.parametrize("func", SEARCHERS, ids=lambda f: f.__name__)

NOT_A_SEQUENCE = [None, 5, 3.5, "123", b"123", {1: 2}, {1, 2, 3}, iter([1, 2]), (x for x in [1, 2]), range(3)]
BAD_ELEMENT_TYPES = [
    [1, "2", 3],
    [1, None, 3],
    [1, [2], 3],
    [1, True, 3],  # bool is rejected on purpose
    [False],
    [1, 2 + 3j],
    ["a", "b"],
]
NON_FINITE = [float("nan"), float("inf"), float("-inf")]


# -------------------------------------------------------------------------- sorting


@sorters
@pytest.mark.parametrize("bad", NOT_A_SEQUENCE, ids=lambda v: type(v).__name__)
def test_sort_rejects_non_list_or_tuple(func, bad):
    with pytest.raises(TypeError, match="list or tuple"):
        func(bad)


@sorters
@pytest.mark.parametrize("bad", BAD_ELEMENT_TYPES, ids=repr)
def test_sort_rejects_bad_element_types(func, bad):
    with pytest.raises(TypeError, match=r"data\[\d+\]"):
        func(bad)


@sorters
@pytest.mark.parametrize("value", NON_FINITE, ids=repr)
def test_sort_rejects_nan_and_infinity(func, value):
    with pytest.raises(ValueError, match="finite"):
        func([1, value, 2])


@sorters
def test_sort_rejects_missing_argument(func):
    with pytest.raises(TypeError):
        func()


@sorters
def test_invalid_input_does_not_modify_caller_data(func):
    data = [3, 2, "x"]
    with pytest.raises(TypeError):
        func(data)
    assert data == [3, 2, "x"]


# ------------------------------------------------------------------------ searching


@searchers
@pytest.mark.parametrize("bad", NOT_A_SEQUENCE, ids=lambda v: type(v).__name__)
def test_search_rejects_non_list_or_tuple(func, bad):
    with pytest.raises(TypeError, match="list or tuple"):
        func(bad, 1)


@searchers
@pytest.mark.parametrize("bad", BAD_ELEMENT_TYPES, ids=repr)
def test_search_rejects_bad_element_types(func, bad):
    with pytest.raises(TypeError, match=r"data\[\d+\]"):
        func(bad, 1)


@searchers
@pytest.mark.parametrize("value", NON_FINITE, ids=repr)
def test_search_rejects_nan_and_infinity_in_data(func, value):
    with pytest.raises(ValueError, match="finite"):
        func([1, value, 2], 1)


@searchers
@pytest.mark.parametrize("bad", [None, "3", [3], True, 2 + 1j], ids=lambda v: type(v).__name__ + repr(v))
def test_search_rejects_bad_target_type(func, bad):
    with pytest.raises(TypeError, match="target"):
        func([1, 2, 3], bad)


@searchers
@pytest.mark.parametrize("value", NON_FINITE, ids=repr)
def test_search_rejects_nan_and_infinity_target(func, value):
    with pytest.raises(ValueError, match="target"):
        func([1, 2, 3], value)


@searchers
def test_search_rejects_missing_target(func):
    with pytest.raises(TypeError):
        func([1, 2, 3])


@searchers
def test_bad_target_rejected_even_for_empty_data(func):
    with pytest.raises(TypeError):
        func([], "x")


@pytest.mark.parametrize("func", SEARCHERS[1:], ids=lambda f: f.__name__)
def test_unsorted_error_hierarchy(func):
    assert issubclass(UnsortedInputError, ValueError)
    with pytest.raises(UnsortedInputError):
        func([2, 1], 1)


@pytest.mark.parametrize("func", SEARCHERS[1:], ids=lambda f: f.__name__)
def test_type_errors_take_priority_over_sorted_check(func):
    with pytest.raises(TypeError):
        func([3, "a", 1], 1)
