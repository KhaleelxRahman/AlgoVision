"""Sorting algorithms for the AlgoVision learning module.

Common contract for every function here:

* Input: a ``list`` or ``tuple`` of finite ints/floats (see ``validation``).
* Output: a NEW ascending list. The input is never mutated or aliased.
* Duplicates and negative numbers are supported.

Each source line ends with ``# @id <algorithm>.<name>``. These tags are the
stable code-line IDs used for explanation highlighting; ``metadata.py`` strips
them when it builds the code shown to learners. Do not rename an ID once it has
been published; add new IDs instead.
"""

from __future__ import annotations

from typing import List, Sequence

from .validation import Number, prepare_sort_input


def bubble_sort(data: Sequence[Number]) -> List[Number]:
    """Return a new ascending list using bubble sort (stable, early exit)."""
    arr = prepare_sort_input(data)  # @id bubble.init
    n = len(arr)  # @id bubble.length
    for end in range(n - 1, 0, -1):  # @id bubble.outer_loop
        swapped = False  # @id bubble.reset_flag
        for j in range(end):  # @id bubble.inner_loop
            if arr[j] > arr[j + 1]:  # @id bubble.compare
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # @id bubble.swap
                swapped = True  # @id bubble.mark_swapped
        if not swapped:  # @id bubble.check_swapped
            break  # @id bubble.early_exit
    return arr  # @id bubble.return


def selection_sort(data: Sequence[Number]) -> List[Number]:
    """Return a new ascending list using selection sort (not stable)."""
    arr = prepare_sort_input(data)  # @id selection.init
    n = len(arr)  # @id selection.length
    for i in range(n - 1):  # @id selection.outer_loop
        min_index = i  # @id selection.assume_min
        for j in range(i + 1, n):  # @id selection.inner_loop
            if arr[j] < arr[min_index]:  # @id selection.compare
                min_index = j  # @id selection.update_min
        if min_index != i:  # @id selection.check_swap
            arr[i], arr[min_index] = arr[min_index], arr[i]  # @id selection.swap
    return arr  # @id selection.return


def insertion_sort(data: Sequence[Number]) -> List[Number]:
    """Return a new ascending list using insertion sort (stable)."""
    arr = prepare_sort_input(data)  # @id insertion.init
    for i in range(1, len(arr)):  # @id insertion.outer_loop
        key = arr[i]  # @id insertion.pick_key
        j = i - 1  # @id insertion.start_scan
        while j >= 0 and arr[j] > key:  # @id insertion.shift_condition
            arr[j + 1] = arr[j]  # @id insertion.shift
            j -= 1  # @id insertion.step_back
        arr[j + 1] = key  # @id insertion.insert
    return arr  # @id insertion.return


def merge_sort(data: Sequence[Number]) -> List[Number]:
    """Return a new ascending list using top-down merge sort (stable)."""
    arr = prepare_sort_input(data)  # @id merge.init

    def sort(items):  # @id merge.def_helper
        if len(items) <= 1:  # @id merge.base_check
            return items  # @id merge.base_return
        mid = len(items) // 2  # @id merge.split
        left = sort(items[:mid])  # @id merge.sort_left
        right = sort(items[mid:])  # @id merge.sort_right
        merged = []  # @id merge.merged_init
        i = j = 0  # @id merge.pointers
        while i < len(left) and j < len(right):  # @id merge.merge_loop
            if left[i] <= right[j]:  # @id merge.compare
                merged.append(left[i])  # @id merge.take_left
                i += 1  # @id merge.advance_left
            else:  # @id merge.else_branch
                merged.append(right[j])  # @id merge.take_right
                j += 1  # @id merge.advance_right
        merged.extend(left[i:])  # @id merge.leftover_left
        merged.extend(right[j:])  # @id merge.leftover_right
        return merged  # @id merge.merge_return

    return sort(arr)  # @id merge.start


def quick_sort(data: Sequence[Number]) -> List[Number]:
    """Return a new ascending list using quick sort (not stable).

    Middle-element pivot with Lomuto partitioning. The smaller partition is
    handled by recursion and the larger one by the loop, so the call stack never
    grows beyond O(log n) even on adversarial input.
    """
    arr = prepare_sort_input(data)  # @id quick.init

    def sort_range(low, high):  # @id quick.def_helper
        while low < high:  # @id quick.loop
            mid = (low + high) // 2  # @id quick.choose_pivot
            arr[mid], arr[high] = arr[high], arr[mid]  # @id quick.move_pivot
            pivot = arr[high]  # @id quick.pivot_value
            boundary = low  # @id quick.boundary
            for j in range(low, high):  # @id quick.scan
                if arr[j] < pivot:  # @id quick.compare
                    arr[boundary], arr[j] = arr[j], arr[boundary]  # @id quick.swap_small
                    boundary += 1  # @id quick.advance_boundary
            arr[boundary], arr[high] = arr[high], arr[boundary]  # @id quick.place_pivot
            if boundary - low < high - boundary:  # @id quick.pick_smaller
                sort_range(low, boundary - 1)  # @id quick.recurse_left
                low = boundary + 1  # @id quick.continue_right
            else:  # @id quick.else_branch
                sort_range(boundary + 1, high)  # @id quick.recurse_right
                high = boundary - 1  # @id quick.continue_left

    sort_range(0, len(arr) - 1)  # @id quick.start
    return arr  # @id quick.return
