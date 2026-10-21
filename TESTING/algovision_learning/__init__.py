"""AlgoVision Python learning module (Member 3).

Ten educational sorting/searching implementations, English + Hinglish
explanations, stable code-line IDs and JSON-ready metadata. Pure Python, no
server, no third-party runtime dependencies.
"""

from .metadata import (
    SCHEMA_VERSION,
    build_catalog,
    catalog_to_json,
    extract_code_lines,
    get_algorithm_metadata,
    get_function,
    list_algorithms,
)
from .searching import (
    binary_search,
    exponential_search,
    interpolation_search,
    jump_search,
    linear_search,
)
from .sorting import (
    bubble_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
)
from .validation import UnsortedInputError

__all__ = [
    "SCHEMA_VERSION",
    "UnsortedInputError",
    "binary_search",
    "bubble_sort",
    "build_catalog",
    "catalog_to_json",
    "exponential_search",
    "extract_code_lines",
    "get_algorithm_metadata",
    "get_function",
    "insertion_sort",
    "interpolation_search",
    "jump_search",
    "linear_search",
    "list_algorithms",
    "merge_sort",
    "quick_sort",
    "selection_sort",
]
