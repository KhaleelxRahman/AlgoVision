"""Structured, JSON-ready learning metadata for all 10 algorithms.

``build_catalog()`` returns plain dicts, lists, strings, numbers and booleans, so
``json.dumps`` works on it directly and any frontend (React/TypeScript or plain
JavaScript) can consume the exported file without a Python runtime.

The code shown to learners is extracted from the real function source with
``inspect``: ``# @id <algorithm>.<name>`` tags become stable line IDs and are
stripped from the displayed text. Nothing is duplicated by hand, so the shown
code cannot drift from the implementation.
"""

from __future__ import annotations

import ast
import inspect
import json
import re
import textwrap
from typing import Any, Callable, Dict, List, Optional

from . import searching, sorting
from .content_searching import CONTENT as SEARCHING_CONTENT
from .content_sorting import CONTENT as SORTING_CONTENT

SCHEMA_VERSION = "1.0"
LANGUAGES = ["en", "hinglish"]

_TAG = re.compile(r"\s+# @id (?P<id>[a-z]+\.[a-z_]+)\s*$")

_COMMON_PRECONDITION = {
    "en": "data must be a list or tuple of finite ints/floats (bool, NaN, infinity and other types are rejected with TypeError/ValueError).",
    "hinglish": "data finite ints/floats ki list ya tuple honi chahiye (bool, NaN, infinity aur doosre types TypeError/ValueError ke saath reject hote hain).",
}
_SORT_PRECONDITIONS = [
    _COMMON_PRECONDITION,
    {
        "en": "The input is never modified; a new ascending list is returned.",
        "hinglish": "Input kabhi modify nahi hota; ek nayi ascending list return hoti hai.",
    },
]
_UNSORTED_OK_PRECONDITIONS = [
    _COMMON_PRECONDITION,
    {
        "en": "target must be a finite int or float. data may be in any order.",
        "hinglish": "target finite int ya float hona chahiye. data kisi bhi order mein ho sakta hai.",
    },
]
_SORTED_PRECONDITIONS = [
    _COMMON_PRECONDITION,
    {
        "en": "target must be a finite int or float.",
        "hinglish": "target finite int ya float hona chahiye.",
    },
    {
        "en": "data must be sorted in ascending (non-decreasing) order. Otherwise UnsortedInputError (a ValueError) is raised, unless validate_sorted=False is passed, in which case the result on unsorted data is unspecified.",
        "hinglish": "data ascending (non-decreasing) order mein sorted hona chahiye. Warna UnsortedInputError (ek ValueError) aata hai, jab tak validate_sorted=False na diya ho; us case mein unsorted data par result unspecified hai.",
    },
]

_SORT_OUTPUT = {
    "en": "A new list with the same values in ascending order.",
    "hinglish": "Wahi values ascending order mein, ek nayi list ke roop mein.",
}
_SEARCH_OUTPUT = {
    "en": "The index of a matching element, or -1 if the target is not present.",
    "hinglish": "Matching element ka index, ya -1 agar target maujood nahi hai.",
}

# Facts per algorithm. Complexity values follow the table in the repository README.
_SPECS: List[Dict[str, Any]] = [
    {
        "id": "bubble-sort", "name": "Bubble Sort", "category": "sorting",
        "func": sorting.bubble_sort, "prefix": "bubble",
        "time": ("O(n)", "O(n²)", "O(n²)"), "space": "O(1)", "stable": True,
        "examples": [{"data": [5, 2, 9, 1, 5, 6]}, {"data": []}],
    },
    {
        "id": "selection-sort", "name": "Selection Sort", "category": "sorting",
        "func": sorting.selection_sort, "prefix": "selection",
        "time": ("O(n²)", "O(n²)", "O(n²)"), "space": "O(1)", "stable": False,
        "examples": [{"data": [29, -3, 10, 10, 0]}, {"data": [1]}],
    },
    {
        "id": "insertion-sort", "name": "Insertion Sort", "category": "sorting",
        "func": sorting.insertion_sort, "prefix": "insertion",
        "time": ("O(n)", "O(n²)", "O(n²)"), "space": "O(1)", "stable": True,
        "examples": [{"data": [12, 11, 13, 5, 6]}, {"data": [1, 2, 3]}],
    },
    {
        "id": "merge-sort", "name": "Merge Sort", "category": "sorting",
        "func": sorting.merge_sort, "prefix": "merge",
        "time": ("O(n log n)", "O(n log n)", "O(n log n)"), "space": "O(n)", "stable": True,
        "examples": [{"data": [38, 27, 43, 3, 9, 82, 10]}, {"data": [2, 2, 1]}],
    },
    {
        "id": "quick-sort", "name": "Quick Sort", "category": "sorting",
        "func": sorting.quick_sort, "prefix": "quick",
        "time": ("O(n log n)", "O(n log n)", "O(n²)"), "space": "O(log n)", "stable": False,
        "examples": [{"data": [10, 7, 8, 9, 1, 5]}, {"data": [3, 3, 3]}],
    },
    {
        "id": "linear-search", "name": "Linear Search", "category": "searching",
        "func": searching.linear_search, "prefix": "linear",
        "time": ("O(1)", "O(n)", "O(n)"), "space": "O(1)", "requires_sorted": False,
        "examples": [
            {"data": [7, 3, 9, 3, 1], "target": 3},
            {"data": [7, 3, 9, 3, 1], "target": 4},
        ],
    },
    {
        "id": "binary-search", "name": "Binary Search", "category": "searching",
        "func": searching.binary_search, "prefix": "binary",
        "time": ("O(1)", "O(log n)", "O(log n)"), "space": "O(1)", "requires_sorted": True,
        "examples": [
            {"data": [2, 5, 8, 12, 16, 23, 38, 56, 72, 91], "target": 23},
            {"data": [2, 5, 8, 12, 16, 23, 38, 56, 72, 91], "target": 7},
        ],
    },
    {
        "id": "jump-search", "name": "Jump Search", "category": "searching",
        "func": searching.jump_search, "prefix": "jump",
        "time": ("O(1)", "O(√n)", "O(√n)"), "space": "O(1)", "requires_sorted": True,
        "examples": [
            {"data": [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89], "target": 55},
            {"data": [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89], "target": 4},
        ],
    },
    {
        "id": "interpolation-search", "name": "Interpolation Search", "category": "searching",
        "func": searching.interpolation_search, "prefix": "interpolation",
        "time": ("O(1)", "O(log log n)", "O(n)"), "space": "O(1)", "requires_sorted": True,
        "time_footnote": {
            "average": {
                "en": "Assumes sorted data with roughly uniformly distributed values.",
                "hinglish": "Maanta hai ki data sorted hai aur values lagbhag uniform failay hain.",
            }
        },
        "examples": [
            {"data": [10, 20, 30, 40, 50, 60, 70, 80, 90], "target": 70},
            {"data": [10, 20, 30, 40, 50, 60, 70, 80, 90], "target": 65},
        ],
    },
    {
        "id": "exponential-search", "name": "Exponential Search", "category": "searching",
        "func": searching.exponential_search, "prefix": "exponential",
        "time": ("O(1)", "O(log n)", "O(log n)"), "space": "O(1)", "requires_sorted": True,
        "examples": [
            {"data": [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21], "target": 15},
            {"data": [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21], "target": 2},
        ],
    },
]


def extract_code_lines(func: Callable[..., Any]) -> List[Dict[str, Any]]:
    """Return learner-facing code lines for ``func`` with stable line IDs.

    The signature (exposed separately as ``signature``), the docstring and blank
    lines are dropped, and the body is de-indented by one level. Every remaining
    line must end with ``# @id <algorithm>.<name>``; the tag is removed from the
    displayed text.
    """
    source = textwrap.dedent(inspect.getsource(func))
    function_node = ast.parse(source).body[0]
    first = function_node.body[0]
    has_docstring = ast.get_docstring(function_node, clean=False) is not None
    header_end = first.end_lineno if has_docstring else first.lineno - 1
    skip = set(range(function_node.lineno, header_end + 1))

    lines: List[Dict[str, Any]] = []
    seen = set()
    for number, raw in enumerate(source.splitlines(), start=1):
        if number in skip or not raw.strip():
            continue
        raw = raw[4:]  # drop the function-body indentation
        match = _TAG.search(raw)
        if match is None:
            raise ValueError(
                f"{func.__name__}: source line {number} has no '# @id' tag: {raw!r}"
            )
        line_id = match.group("id")
        if line_id in seen:
            raise ValueError(f"{func.__name__}: duplicate line id {line_id!r}")
        seen.add(line_id)
        code = raw[: match.start()].rstrip()
        lines.append(
            {
                "id": line_id,
                "line": len(lines) + 1,
                "indent": (len(code) - len(code.lstrip())) // 4,
                "code": code,
            }
        )
    return lines


def _signature(func: Callable[..., Any]) -> str:
    parts = []
    for name, parameter in inspect.signature(func).parameters.items():
        if parameter.default is inspect.Parameter.empty:
            parts.append(name)
        else:
            parts.append(f"{name}={parameter.default!r}")
    return f"{func.__name__}({', '.join(parts)})"


def _build_entry(spec: Dict[str, Any], content: Dict[str, Any]) -> Dict[str, Any]:
    func = spec["func"]
    is_sort = spec["category"] == "sorting"
    code_lines = extract_code_lines(func)
    line_texts = content["lines"]

    expected_ids = {line["id"] for line in code_lines}
    if set(line_texts) != expected_ids:
        missing = sorted(expected_ids - set(line_texts))
        extra = sorted(set(line_texts) - expected_ids)
        raise ValueError(
            f"{spec['id']}: line explanations out of sync (missing={missing}, extra={extra})"
        )
    for line in code_lines:
        if not line["id"].startswith(spec["prefix"] + "."):
            raise ValueError(f"{spec['id']}: line id {line['id']!r} has wrong prefix")
        line["explanation"] = line_texts[line["id"]]

    best, average, worst = spec["time"]
    time_entry: Dict[str, Any] = {"best": best, "average": average, "worst": worst}
    if "time_footnote" in spec:
        time_entry["footnotes"] = spec["time_footnote"]

    examples = []
    for example in spec["examples"]:
        arguments = dict(example)
        examples.append({"input": arguments, "output": func(**arguments)})

    entry: Dict[str, Any] = {
        "id": spec["id"],
        "name": spec["name"],
        "category": spec["category"],
        "function": func.__name__,
        "signature": _signature(func),
        "preconditions": (
            _SORT_PRECONDITIONS
            if is_sort
            else _SORTED_PRECONDITIONS
            if spec["requires_sorted"]
            else _UNSORTED_OK_PRECONDITIONS
        ),
        "output": _SORT_OUTPUT if is_sort else _SEARCH_OUTPUT,
        "mutates_input": False,
        "complexity": {
            "time": time_entry,
            "space": {"auxiliary": spec["space"]},
            "notes": content["complexity_notes"],
        },
        "explanation": {
            "summary": content["summary"],
            "when_to_use": content["when_to_use"],
            "how_it_works": content["how_it_works"],
        },
        "code": {
            "language": "python",
            "source": "\n".join(line["code"] for line in code_lines),
            "line_ids": [line["id"] for line in code_lines],
            "lines": code_lines,
        },
        "examples": examples,
    }
    if is_sort:
        entry["stable"] = spec["stable"]
    else:
        entry["requires_sorted_input"] = spec["requires_sorted"]
    return entry


def build_catalog() -> Dict[str, Any]:
    """Build the complete, JSON-serialisable learning catalog."""
    content = {**SORTING_CONTENT, **SEARCHING_CONTENT}
    algorithms = [_build_entry(spec, content[spec["id"]]) for spec in _SPECS]
    return {
        "schema_version": SCHEMA_VERSION,
        "languages": list(LANGUAGES),
        "algorithms": algorithms,
    }


def get_algorithm_metadata(algorithm_id: str) -> Dict[str, Any]:
    """Return one algorithm's metadata by id (for example ``"bubble-sort"``)."""
    for entry in build_catalog()["algorithms"]:
        if entry["id"] == algorithm_id:
            return entry
    raise KeyError(f"unknown algorithm id: {algorithm_id!r}")


def list_algorithms(category: Optional[str] = None) -> List[str]:
    """Return algorithm ids, optionally filtered by ``"sorting"``/``"searching"``."""
    return [s["id"] for s in _SPECS if category is None or s["category"] == category]


def get_function(algorithm_id: str) -> Callable[..., Any]:
    """Return the Python implementation for an algorithm id."""
    for spec in _SPECS:
        if spec["id"] == algorithm_id:
            return spec["func"]
    raise KeyError(f"unknown algorithm id: {algorithm_id!r}")


def catalog_to_json(catalog: Optional[Dict[str, Any]] = None) -> str:
    """Serialise the catalog to a stable, human-diffable JSON string."""
    data = build_catalog() if catalog is None else catalog
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"
