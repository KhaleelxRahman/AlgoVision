"""Tests for the educational metadata, line IDs, content and JSON export."""

import ast
import json
import re
import textwrap
from pathlib import Path

import pytest

import algovision_learning as pkg
from algovision_learning import __main__ as cli
from algovision_learning import searching, sorting
from algovision_learning.metadata import (
    build_catalog,
    catalog_to_json,
    extract_code_lines,
    get_algorithm_metadata,
    get_function,
    list_algorithms,
)
from algovision_learning.validation import (
    prepare_search_input,
    prepare_sort_input,
    prepare_sorted_search_input,
)

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
EXPORTED_JSON = PACKAGE_ROOT / "data" / "algovision_learning.json"

SORTING_IDS = ["bubble-sort", "selection-sort", "insertion-sort", "merge-sort", "quick-sort"]
SEARCHING_IDS = [
    "linear-search",
    "binary-search",
    "jump-search",
    "interpolation-search",
    "exponential-search",
]
ALL_IDS = SORTING_IDS + SEARCHING_IDS

# Complexity as published in the repository README (time) plus documented space.
EXPECTED_TIME = {
    "bubble-sort": ("O(n)", "O(n²)", "O(n²)"),
    "selection-sort": ("O(n²)", "O(n²)", "O(n²)"),
    "insertion-sort": ("O(n)", "O(n²)", "O(n²)"),
    "merge-sort": ("O(n log n)", "O(n log n)", "O(n log n)"),
    "quick-sort": ("O(n log n)", "O(n log n)", "O(n²)"),
    "linear-search": ("O(1)", "O(n)", "O(n)"),
    "binary-search": ("O(1)", "O(log n)", "O(log n)"),
    "jump-search": ("O(1)", "O(√n)", "O(√n)"),
    "interpolation-search": ("O(1)", "O(log log n)", "O(n)"),
    "exponential-search": ("O(1)", "O(log n)", "O(log n)"),
}
EXPECTED_SPACE = {
    "bubble-sort": "O(1)",
    "selection-sort": "O(1)",
    "insertion-sort": "O(1)",
    "merge-sort": "O(n)",
    "quick-sort": "O(log n)",
    "linear-search": "O(1)",
    "binary-search": "O(1)",
    "jump-search": "O(1)",
    "interpolation-search": "O(1)",
    "exponential-search": "O(1)",
}
EXPECTED_STABLE = {
    "bubble-sort": True,
    "selection-sort": False,
    "insertion-sort": True,
    "merge-sort": True,
    "quick-sort": False,
}

# Regression guard: published line IDs must not be renamed or reordered silently.
# If you intentionally add a line, add its ID here; never change an existing one.
EXPECTED_LINE_IDS = {
    "bubble-sort": [
        "bubble.init", "bubble.length", "bubble.outer_loop", "bubble.reset_flag",
        "bubble.inner_loop", "bubble.compare", "bubble.swap", "bubble.mark_swapped",
        "bubble.check_swapped", "bubble.early_exit", "bubble.return",
    ],
    "selection-sort": [
        "selection.init", "selection.length", "selection.outer_loop", "selection.assume_min",
        "selection.inner_loop", "selection.compare", "selection.update_min",
        "selection.check_swap", "selection.swap", "selection.return",
    ],
    "insertion-sort": [
        "insertion.init", "insertion.outer_loop", "insertion.pick_key", "insertion.start_scan",
        "insertion.shift_condition", "insertion.shift", "insertion.step_back",
        "insertion.insert", "insertion.return",
    ],
    "merge-sort": [
        "merge.init", "merge.def_helper", "merge.base_check", "merge.base_return",
        "merge.split", "merge.sort_left", "merge.sort_right", "merge.merged_init",
        "merge.pointers", "merge.merge_loop", "merge.compare", "merge.take_left",
        "merge.advance_left", "merge.else_branch", "merge.take_right", "merge.advance_right",
        "merge.leftover_left", "merge.leftover_right", "merge.merge_return", "merge.start",
    ],
    "quick-sort": [
        "quick.init", "quick.def_helper", "quick.loop", "quick.choose_pivot",
        "quick.move_pivot", "quick.pivot_value", "quick.boundary", "quick.scan",
        "quick.compare", "quick.swap_small", "quick.advance_boundary", "quick.place_pivot",
        "quick.pick_smaller", "quick.recurse_left", "quick.continue_right",
        "quick.else_branch", "quick.recurse_right", "quick.continue_left", "quick.start",
        "quick.return",
    ],
    "linear-search": [
        "linear.init", "linear.loop", "linear.compare", "linear.found", "linear.not_found",
    ],
    "binary-search": [
        "binary.init", "binary.set_low", "binary.set_high", "binary.loop", "binary.mid",
        "binary.compare_equal", "binary.found", "binary.compare_less", "binary.go_right",
        "binary.else_branch", "binary.go_left", "binary.not_found",
    ],
    "jump-search": [
        "jump.init", "jump.length", "jump.block_size", "jump.prev", "jump.curr",
        "jump.jump_loop", "jump.advance_prev", "jump.advance_curr", "jump.scan",
        "jump.compare", "jump.found", "jump.not_found",
    ],
    "interpolation-search": [
        "interpolation.init", "interpolation.set_low", "interpolation.set_high",
        "interpolation.loop", "interpolation.flat_check", "interpolation.flat_found",
        "interpolation.estimate", "interpolation.compare_equal", "interpolation.found",
        "interpolation.compare_less", "interpolation.go_right", "interpolation.else_branch",
        "interpolation.go_left", "interpolation.not_found",
    ],
    "exponential-search": [
        "exponential.init", "exponential.length", "exponential.empty_check",
        "exponential.empty_return", "exponential.check_first", "exponential.first_found",
        "exponential.bound_init", "exponential.grow_loop", "exponential.double",
        "exponential.range_low", "exponential.range_high", "exponential.bsearch_loop",
        "exponential.mid", "exponential.compare_equal", "exponential.found",
        "exponential.compare_less", "exponential.go_right", "exponential.else_branch",
        "exponential.go_left", "exponential.not_found",
    ],
}


@pytest.fixture(scope="module")
def catalog():
    return build_catalog()


@pytest.fixture(scope="module")
def by_id(catalog):
    return {entry["id"]: entry for entry in catalog["algorithms"]}


per_algorithm = pytest.mark.parametrize("algorithm_id", ALL_IDS)


# ------------------------------------------------------------------------ catalog shape


def test_catalog_contains_exactly_the_ten_algorithms(catalog):
    assert [a["id"] for a in catalog["algorithms"]] == ALL_IDS
    assert catalog["schema_version"] == pkg.SCHEMA_VERSION
    assert catalog["languages"] == ["en", "hinglish"]


def test_list_algorithms_filters_by_category():
    assert list_algorithms() == ALL_IDS
    assert list_algorithms("sorting") == SORTING_IDS
    assert list_algorithms("searching") == SEARCHING_IDS


def test_lookup_helpers():
    assert get_algorithm_metadata("binary-search")["name"] == "Binary Search"
    assert get_function("merge-sort") is sorting.merge_sort
    with pytest.raises(KeyError):
        get_algorithm_metadata("bogo-sort")
    with pytest.raises(KeyError):
        get_function("bogo-sort")


def test_public_functions_are_exported_from_package():
    for name in (
        "bubble_sort", "selection_sort", "insertion_sort", "merge_sort", "quick_sort",
        "linear_search", "binary_search", "jump_search", "interpolation_search",
        "exponential_search",
    ):
        assert callable(getattr(pkg, name))
        assert name in pkg.__all__


@per_algorithm
def test_entry_has_the_documented_schema(by_id, algorithm_id):
    entry = by_id[algorithm_id]
    for key in (
        "id", "name", "category", "function", "signature", "preconditions", "output",
        "mutates_input", "complexity", "explanation", "code", "examples",
    ):
        assert key in entry, key
    assert entry["category"] in ("sorting", "searching")
    assert entry["mutates_input"] is False
    assert set(entry["complexity"]["time"]) >= {"best", "average", "worst"}
    assert set(entry["complexity"]["space"]) == {"auxiliary"}
    assert set(entry["complexity"]["notes"]) == {"en", "hinglish"}
    assert set(entry["complexity"]["notes"]["en"]) == {"time", "space"}
    assert set(entry["complexity"]["notes"]["hinglish"]) == {"time", "space"}
    assert set(entry["explanation"]) == {"summary", "when_to_use", "how_it_works"}
    for field in entry["explanation"].values():
        assert set(field) == {"en", "hinglish"}
    assert entry["code"]["language"] == "python"
    assert entry["examples"]
    if entry["category"] == "sorting":
        assert isinstance(entry["stable"], bool)
        assert "requires_sorted_input" not in entry
    else:
        assert isinstance(entry["requires_sorted_input"], bool)
        assert "stable" not in entry


@per_algorithm
def test_function_name_and_signature_match_the_implementation(by_id, algorithm_id):
    entry = by_id[algorithm_id]
    func = get_function(algorithm_id)
    assert entry["function"] == func.__name__
    assert entry["signature"].startswith(func.__name__ + "(")
    if entry["category"] == "sorting":
        assert entry["signature"] == f"{func.__name__}(data)"
    elif entry["requires_sorted_input"]:
        assert entry["signature"] == f"{func.__name__}(data, target, validate_sorted=True)"
    else:
        assert entry["signature"] == f"{func.__name__}(data, target)"


# ----------------------------------------------------------------------------- complexity


@per_algorithm
def test_time_complexity_matches_readme_table(by_id, algorithm_id):
    time = by_id[algorithm_id]["complexity"]["time"]
    assert (time["best"], time["average"], time["worst"]) == EXPECTED_TIME[algorithm_id]


@per_algorithm
def test_auxiliary_space_is_documented(by_id, algorithm_id):
    assert by_id[algorithm_id]["complexity"]["space"]["auxiliary"] == EXPECTED_SPACE[algorithm_id]


def test_interpolation_average_case_carries_its_assumption(by_id):
    footnotes = by_id["interpolation-search"]["complexity"]["time"]["footnotes"]
    assert "uniform" in footnotes["average"]["en"].lower()
    assert footnotes["average"]["hinglish"]


@pytest.mark.parametrize("algorithm_id", SORTING_IDS)
def test_stability_flags(by_id, algorithm_id):
    assert by_id[algorithm_id]["stable"] is EXPECTED_STABLE[algorithm_id]


@pytest.mark.parametrize("algorithm_id", SEARCHING_IDS)
def test_sorted_requirement_flags(by_id, algorithm_id):
    assert by_id[algorithm_id]["requires_sorted_input"] is (algorithm_id != "linear-search")


# ---------------------------------------------------------------------------- line IDs


@per_algorithm
def test_line_ids_are_stable(by_id, algorithm_id):
    assert by_id[algorithm_id]["code"]["line_ids"] == EXPECTED_LINE_IDS[algorithm_id]


@per_algorithm
def test_line_ids_are_unique_well_formed_and_prefixed(by_id, algorithm_id):
    ids = by_id[algorithm_id]["code"]["line_ids"]
    prefix = algorithm_id.split("-")[0]
    assert len(ids) == len(set(ids))
    for line_id in ids:
        assert re.fullmatch(r"[a-z]+\.[a-z_]+", line_id), line_id
        assert line_id.startswith(prefix + "."), line_id


def test_line_ids_are_globally_unique(catalog):
    every_id = [i for a in catalog["algorithms"] for i in a["code"]["line_ids"]]
    assert len(every_id) == len(set(every_id))


@per_algorithm
def test_line_records_are_consistent(by_id, algorithm_id):
    code = by_id[algorithm_id]["code"]
    lines = code["lines"]
    assert [line["id"] for line in lines] == code["line_ids"]
    assert [line["line"] for line in lines] == list(range(1, len(lines) + 1))
    assert code["source"] == "\n".join(line["code"] for line in lines)
    for line in lines:
        assert set(line) == {"id", "line", "indent", "code", "explanation"}
        assert "@id" not in line["code"]
        assert "#" not in line["code"]
        assert line["indent"] == (len(line["code"]) - len(line["code"].lstrip())) // 4


@per_algorithm
def test_displayed_code_hides_docstring_and_signature(by_id, algorithm_id):
    source = by_id[algorithm_id]["code"]["source"]
    assert '"""' not in source
    assert not source.lstrip().startswith("def " + get_function(algorithm_id).__name__)


def test_source_tags_and_extraction_agree_for_every_function():
    for module in (sorting, searching):
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                lines = extract_code_lines(getattr(module, node.name))
                assert lines, node.name


def test_untagged_code_line_is_rejected():
    def sample(data):
        """doc"""
        x = 1  # @id sample.ok
        y = 2
        return x + y  # @id sample.done

    with pytest.raises(ValueError, match="no '# @id' tag"):
        extract_code_lines(sample)


def test_duplicate_line_id_is_rejected():
    def sample(data):
        """doc"""
        x = 1  # @id sample.same
        return x  # @id sample.same

    with pytest.raises(ValueError, match="duplicate line id"):
        extract_code_lines(sample)


# ------------------------------------------------------- displayed code is the real code


def _rebuild(algorithm_id, entry):
    """Re-create a callable from the displayed lines only."""
    func = get_function(algorithm_id)
    header = f"def {entry['signature']}:\n"
    body = textwrap.indent(entry["code"]["source"], "    ")
    namespace = {
        "math": __import__("math"),
        "prepare_sort_input": prepare_sort_input,
        "prepare_search_input": prepare_search_input,
        "prepare_sorted_search_input": prepare_sorted_search_input,
    }
    exec(header + body, namespace)  # noqa: S102 - our own displayed source
    return namespace[func.__name__]


@per_algorithm
def test_displayed_code_executes_and_behaves_like_the_implementation(by_id, algorithm_id):
    entry = by_id[algorithm_id]
    rebuilt = _rebuild(algorithm_id, entry)
    original = get_function(algorithm_id)
    if entry["category"] == "sorting":
        for data in ([], [1], [3, 1, 2], [5, 5, -1, 0, 9, 2], list(range(10, 0, -1))):
            assert rebuilt(data) == original(data) == sorted(data)
    else:
        data = [1, 3, 4, 8, 10, 15, 21, 22, 40]
        for target in data + [0, 5, 100]:
            assert rebuilt(data, target) == original(data, target)


@per_algorithm
def test_documented_examples_are_true(by_id, algorithm_id):
    func = get_function(algorithm_id)
    for example in by_id[algorithm_id]["examples"]:
        assert func(**example["input"]) == example["output"]
        if by_id[algorithm_id]["category"] == "sorting":
            assert example["output"] == sorted(example["input"]["data"])
        else:
            data, target = example["input"]["data"], example["input"]["target"]
            if target in data:
                assert data[example["output"]] == target
                if algorithm_id == "linear-search":
                    assert example["output"] == data.index(target)
            else:
                assert example["output"] == -1


# ---------------------------------------------------------------------- bilingual text


_CODE_KEYS = {"code", "source"}  # code text is indented on purpose


def _strings(value):
    """Yield every prose string in the catalog (code text is excluded)."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            if key not in _CODE_KEYS:
                yield from _strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)


@per_algorithm
def test_every_line_has_english_and_hinglish_explanations(by_id, algorithm_id):
    for line in by_id[algorithm_id]["code"]["lines"]:
        explanation = line["explanation"]
        assert set(explanation) == {"en", "hinglish"}, line["id"]
        assert len(explanation["en"]) >= 10, line["id"]
        assert len(explanation["hinglish"]) >= 10, line["id"]


@per_algorithm
def test_hinglish_is_not_a_copy_of_english(by_id, algorithm_id):
    entry = by_id[algorithm_id]
    for line in entry["code"]["lines"]:
        explanation = line["explanation"]
        if line["id"].endswith(".init") and entry["category"] == "searching":
            continue  # intentionally shares technical wording (validate_sorted)
        assert explanation["en"] != explanation["hinglish"], line["id"]
    summary = entry["explanation"]["summary"]
    assert summary["en"] != summary["hinglish"]
    for key in ("when_to_use", "how_it_works"):
        block = entry["explanation"][key]
        assert len(block["en"]) == len(block["hinglish"]) >= 2
        assert block["en"] != block["hinglish"]


@per_algorithm
def test_hinglish_text_is_roman_script(by_id, algorithm_id):
    hinglish = [
        by_id[algorithm_id]["explanation"]["summary"]["hinglish"],
        *by_id[algorithm_id]["explanation"]["how_it_works"]["hinglish"],
        *[line["explanation"]["hinglish"] for line in by_id[algorithm_id]["code"]["lines"]],
    ]
    for text in hinglish:
        assert not re.search(r"[ऀ-ॿ]", text), text  # no Devanagari


@per_algorithm
def test_hinglish_actually_contains_hindi_words(by_id, algorithm_id):
    summary = by_id[algorithm_id]["explanation"]["summary"]["hinglish"].lower()
    assert re.search(r"\b(hai|ko|ka|ki|ke|aur|se|mein|karta|karo)\b", summary)


@per_algorithm
def test_complexity_notes_mention_each_stated_bound(by_id, algorithm_id):
    entry = by_id[algorithm_id]
    for language in ("en", "hinglish"):
        notes = entry["complexity"]["notes"][language]
        assert entry["complexity"]["space"]["auxiliary"] in notes["space"]
        time = entry["complexity"]["time"]
        text = notes["time"].replace("sqrt(n)", "√n")
        for bound in {time["best"], time["average"], time["worst"]}:
            assert bound in text or bound.replace("√n", "sqrt(n)") in notes["time"], (
                algorithm_id, language, bound,
            )


def test_no_empty_strings_anywhere(catalog):
    for text in _strings(catalog):
        assert text.strip() == text and text, repr(text)


# ------------------------------------------------------------------------ JSON export


def test_catalog_is_json_serialisable_and_round_trips(catalog):
    text = json.dumps(catalog)
    assert json.loads(text) == catalog


def test_catalog_json_is_deterministic():
    assert catalog_to_json() == catalog_to_json()


def test_exported_json_file_is_up_to_date():
    assert EXPORTED_JSON.is_file(), (
        "data/algovision_learning.json missing; run: python -m algovision_learning "
        "--output data/algovision_learning.json"
    )
    assert EXPORTED_JSON.read_text(encoding="utf-8") == catalog_to_json(), (
        "data/algovision_learning.json is stale; regenerate with: python -m algovision_learning "
        "--output data/algovision_learning.json"
    )


def test_cli_output_and_check(tmp_path, capsys):
    target = tmp_path / "out" / "catalog.json"
    assert cli.main(["--check", str(target)]) == 1  # missing file
    assert cli.main(["--output", str(target)]) == 0
    assert target.read_text(encoding="utf-8") == catalog_to_json()
    assert cli.main(["--check", str(target)]) == 0
    target.write_text("{}", encoding="utf-8")
    assert cli.main(["--check", str(target)]) == 1  # stale file
    capsys.readouterr()
    assert cli.main([]) == 0
    assert json.loads(capsys.readouterr().out)["schema_version"] == pkg.SCHEMA_VERSION
