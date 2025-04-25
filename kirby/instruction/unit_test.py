UNIT_TEST_INSTRUCTIONS = [
    "✅ MANDATORY: Your response must only include generated test files.",
    "Use the `pytest` framework. Place each test file inside a top-level `tests/` directory using the format `tests/module/test_<moduleA/moduleB>_<filename>.py`.",
    "Import and test only the public functions or classes defined in the corresponding source module.",
    "Inspect function signatures, docstrings, and logic to infer intended behavior before writing tests.",
    "Enumerate normal cases, boundary values, and error conditions for every function.",
    "Use the Arrange-Act-Assert pattern and group tests using descriptive test functions or `pytest` classes.",
    "Leverage `pytest.mark.parametrize` to consolidate similar cases and reduce repetition.",
    "Stub or mock external dependencies (file I/O, network, databases) using fixtures or `monkeypatching` to isolate logic.",
    "Ensure tests are independent: use setup/teardown fixtures and avoid shared state.",
    "Assert both return values and side effects such as written files, logs, or state changes.",
    "Verify exceptions: test both the raised types and relevant message content.",
]
