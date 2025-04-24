import pytest
from util.string_util import DEFAULT_FENCE, parse_code_response


def block(path: str, body: str = "") -> str:
    quoted = f'"{path}"' if path[0] not in "\"'`" else path
    return (
        "!@# random_text !@#"
        f"{DEFAULT_FENCE}"
        f"{quoted}{body}"
        f"{DEFAULT_FENCE} "
        "!@# random_text !@#"
    )


# ────────────────────────── happy-path table ────────────────────
GOOD = [
    (
        block("src/app.py", "kappa('hi')\n"),
        {"src/app.py": "kappa('hi')\n"},
    ),
    (
        "\n".join(
            [
                block("a.py", "\nA\n"),
                block("b.txt", "\nB\n"),
                block("c.js", "\nC\n"),
            ]
        ),
        {"a.py": "\nA\n", "b.txt": "\nB\n", "c.js": "\nC\n"},
    ),
    (
        block("notes.md", "\n# Title ```python\nimport ...```"),
        {"notes.md": "\n# Title ```python\nimport ...```"},
    ),
    (
        block("dir with space/data.txt", "\nX\n"),
        {"dir with space/data.txt": "\nX\n"},
    ),
    (
        block("empty.py", ""),
        {"empty.py": ""},
    ),
]


@pytest.mark.parametrize("source, expected", GOOD, ids=[c[0] for c in GOOD])
def test_parse_code_response_good(source, expected):
    result = parse_code_response(source)
    assert result == expected
    assert list(result) == list(expected)


def test_duplicate_paths_last_one_wins():
    src = "\n".join(
        [
            block("dup.py", "\nONE\n"),
            block("dup.py", "\nTWO\n"),
        ]
    )
    res = parse_code_response(src)
    assert res == {"dup.py": "\nTWO\n"}
    assert next(iter(res)) == "dup.py"


@pytest.mark.parametrize("quote", ["'", "`"])
def test_different_quote_styles(quote):
    src = block(f'{quote}quoted.txt{quote}', "\nX\n")
    res = parse_code_response(src)
    assert res == {"quoted.txt": "\nX\n"}


def test_reject_path_outside_root(tmp_path):
    root = tmp_path / "sandbox"
    root.mkdir()
    src = block("../escape.txt", "\nZ\n")
    res = parse_code_response(src, root=root)
    assert res == {}


def test_carriage_return_line_endings():
    src = "~~~\"foo.txt\"\r\nFOO\r\n~~~\r\n"
    assert parse_code_response(src) == {"foo.txt": "\r\nFOO\r\n"}
