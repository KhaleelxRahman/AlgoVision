"""Searching algorithms for the AlgoVision learning module.

Common contract for every function here:

* Input: a ``list`` or ``tuple`` of finite ints/floats plus a finite numeric
  ``target``.
* Output: an ``int`` index where ``data[index] == target``, or ``-1`` if the
  target is absent. The input is never mutated.
* With duplicate values, ``linear_search`` returns the FIRST matching index; the
  other searches return SOME matching index (not guaranteed to be the first).
* Binary, jump, interpolation and exponential search require ascending
  (non-decreasing) input. By default they validate this and raise
  ``UnsortedInputError``; that check is one O(n) pass that happens before the
  search itself. Pass ``validate_sorted=False`` to skip it when you already know
  the data is sorted.

Each source line ends with ``# @id <algorithm>.<name>`` (stable code-line IDs;
see ``sorting.py``).
"""

from __future__ import annotations

import math
from typing import Sequence

from .validation import (
    Number,
    prepare_search_input,
    prepare_sorted_search_input,
)


def linear_search(data: Sequence[Number], target: Number) -> int:
    """Return the first index of ``target`` in ``data`` or -1 (works unsorted)."""
    arr = prepare_search_input(data, target)  # @id linear.init
    for i in range(len(arr)):  # @id linear.loop
        if arr[i] == target:  # @id linear.compare
            return i  # @id linear.found
    return -1  # @id linear.not_found


def binary_search(
    data: Sequence[Number], target: Number, validate_sorted: bool = True
) -> int:
    """Return an index of ``target`` in sorted ``data`` or -1."""
    arr = prepare_sorted_search_input(data, target, validate_sorted)  # @id binary.init
    low = 0  # @id binary.set_low
    high = len(arr) - 1  # @id binary.set_high
    while low <= high:  # @id binary.loop
        mid = (low + high) // 2  # @id binary.mid
        if arr[mid] == target:  # @id binary.compare_equal
            return mid  # @id binary.found
        if arr[mid] < target:  # @id binary.compare_less
            low = mid + 1  # @id binary.go_right
        else:  # @id binary.else_branch
            high = mid - 1  # @id binary.go_left
    return -1  # @id binary.not_found


def jump_search(
    data: Sequence[Number], target: Number, validate_sorted: bool = True
) -> int:
    """Return an index of ``target`` in sorted ``data`` or -1 (block size sqrt(n))."""
    arr = prepare_sorted_search_input(data, target, validate_sorted)  # @id jump.init
    n = len(arr)  # @id jump.length
    step = math.isqrt(n)  # @id jump.block_size
    prev = 0  # @id jump.prev
    curr = step  # @id jump.curr
    while prev < n and arr[min(curr, n) - 1] < target:  # @id jump.jump_loop
        prev = curr  # @id jump.advance_prev
        curr += step  # @id jump.advance_curr
    for i in range(prev, min(curr, n)):  # @id jump.scan
        if arr[i] == target:  # @id jump.compare
            return i  # @id jump.found
    return -1  # @id jump.not_found


def interpolation_search(
    data: Sequence[Number], target: Number, validate_sorted: bool = True
) -> int:
    """Return an index of ``target`` in sorted ``data`` or -1 (probe by value).

    Known limitation: float data whose range overflows when subtracted
    (differences beyond about 1e308) is not supported.
    """
    arr = prepare_sorted_search_input(data, target, validate_sorted)  # @id interpolation.init
    low = 0  # @id interpolation.set_low
    high = len(arr) - 1  # @id interpolation.set_high
    while low <= high and arr[low] <= target <= arr[high]:  # @id interpolation.loop
        if arr[high] == arr[low]:  # @id interpolation.flat_check
            return low  # @id interpolation.flat_found
        pos = low + int((high - low) * (target - arr[low]) // (arr[high] - arr[low]))  # @id interpolation.estimate
        if arr[pos] == target:  # @id interpolation.compare_equal
            return pos  # @id interpolation.found
        if arr[pos] < target:  # @id interpolation.compare_less
            low = pos + 1  # @id interpolation.go_right
        else:  # @id interpolation.else_branch
            high = pos - 1  # @id interpolation.go_left
    return -1  # @id interpolation.not_found


def exponential_search(
    data: Sequence[Number], target: Number, validate_sorted: bool = True
) -> int:
    """Return an index of ``target`` in sorted ``data`` or -1 (double, then bisect)."""
    arr = prepare_sorted_search_input(data, target, validate_sorted)  # @id exponential.init
    n = len(arr)  # @id exponential.length
    if n == 0:  # @id exponential.empty_check
        return -1  # @id exponential.empty_return
    if arr[0] == target:  # @id exponential.check_first
        return 0  # @id exponential.first_found
    bound = 1  # @id exponential.bound_init
    while bound < n and arr[bound] <= target:  # @id exponential.grow_loop
        bound *= 2  # @id exponential.double
    low = bound // 2  # @id exponential.range_low
    high = min(bound, n - 1)  # @id exponential.range_high
    while low <= high:  # @id exponential.bsearch_loop
        mid = (low + high) // 2  # @id exponential.mid
        if arr[mid] == target:  # @id exponential.compare_equal
            return mid  # @id exponential.found
        if arr[mid] < target:  # @id exponential.compare_less
            low = mid + 1  # @id exponential.go_right
        else:  # @id exponential.else_branch
            high = mid - 1  # @id exponential.go_left
    return -1  # @id exponential.not_found
