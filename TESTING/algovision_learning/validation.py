"""Input validation shared by every AlgoVision learning algorithm.

Rules (documented once, enforced everywhere):

* ``data`` must be a ``list`` or ``tuple``. Anything else raises ``TypeError``.
* Every element must be an ``int`` or ``float``. ``bool`` is rejected on purpose
  (``True`` is technically an ``int`` in Python but is almost always a mistake).
  Wrong element types raise ``TypeError``.
* ``NaN`` and ``+/-infinity`` are rejected with ``ValueError`` because they break
  ordering and interpolation arithmetic.
* Search algorithms that require sorted input raise ``UnsortedInputError``
  (a ``ValueError``) when the data is not in ascending (non-decreasing) order.
"""

from __future__ import annotations

import math
from typing import Any, List, Sequence, Union

Number = Union[int, float]


class UnsortedInputError(ValueError):
    """Raised when a search that requires sorted input receives unsorted data."""


def _is_valid_number(value: Any) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return not (isinstance(value, float) and not math.isfinite(value))


def _raise_invalid(value: Any, label: str) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(
            f"{label} must be an int or float, got {type(value).__name__}"
        )
    raise ValueError(f"{label} must be finite (NaN and infinity are not supported)")


def check_container(data: Any) -> None:
    """Require ``data`` to be a list or tuple (O(1))."""
    if not isinstance(data, (list, tuple)):
        raise TypeError(
            f"data must be a list or tuple of numbers, got {type(data).__name__}"
        )


def check_numbers(data: Sequence[Any]) -> None:
    """Require every element to be a finite int/float (O(n))."""
    for index, value in enumerate(data):
        if not _is_valid_number(value):
            _raise_invalid(value, f"data[{index}]")


def check_target(target: Any) -> None:
    """Require the search target to be a finite int/float (O(1))."""
    if not _is_valid_number(target):
        _raise_invalid(target, "target")


def check_sorted(data: Sequence[Number]) -> None:
    """Require ascending (non-decreasing) order (O(n))."""
    for index in range(1, len(data)):
        if data[index - 1] > data[index]:
            raise UnsortedInputError(
                "data must be sorted in ascending order, but "
                f"data[{index - 1}]={data[index - 1]!r} > data[{index}]={data[index]!r}"
            )


def prepare_sort_input(data: Any) -> List[Number]:
    """Validate sort input and return a fresh list copy.

    Sorting functions work on the copy, so the caller's data is never mutated.
    """
    check_container(data)
    check_numbers(data)
    return list(data)


def prepare_search_input(data: Any, target: Any) -> Sequence[Number]:
    """Validate input for an unsorted-friendly search (linear search)."""
    check_container(data)
    check_numbers(data)
    check_target(target)
    return data


def prepare_sorted_search_input(
    data: Any, target: Any, validate_sorted: bool = True
) -> Sequence[Number]:
    """Validate input for searches that need sorted data.

    The container type and the target are always checked (O(1)). When
    ``validate_sorted`` is true (the default) the elements and the ascending
    order are checked too, which costs one O(n) pass *before* the search starts.
    Pass ``validate_sorted=False`` only if you already know the data is a sorted
    list of finite numbers; behaviour on unsorted data is then unspecified
    (the search still terminates, but may miss the target).
    """
    check_container(data)
    check_target(target)
    if validate_sorted:
        check_numbers(data)
        check_sorted(data)
    return data
