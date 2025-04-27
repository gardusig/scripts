from kirby.instruction.instruction_model import Instruction

UNIT_TEST_INSTRUCTION = Instruction(
    instructions=[
        "✅ MANDATORY: Generate exactly one test file for each non-test source file.",
        "Use the pytest framework and place all tests under a top-level `tests/` directory.",
        "Name each test file following the pattern:"
        "  • `tests/<module>/test_<module>_<filename>.py`",
        "Stub every external dependency imported at the top of your module.",
        "Example: `import path.to.lib` must be replaced with",
        '`patch("your.module.name.dep_name", return_value=...):`',
        'Don\'t use `patch("path.to.lib", ...)`, patch the current module directly.',
        "Use pytest fixtures (e.g. `tmp_path`, `monkeypatch`) for setup/teardown and file system isolation.",
        "Leverage `pytest.mark.parametrize` to cover multiple input/output variations in one test function.",
        "Ensure tests are independent—no shared state—by mocking I/O, network, and DB calls.",
        "Assert both return values and side effects (e.g., file writes, log messages, DB updates).",
        "Cover normal cases, boundary conditions, and expected exceptions (use `with pytest.raises(...)`).",
        "Give each test function a clear, descriptive name in snake_case that states the behavior under test.",
        "Keep each test focused on a single behavior or scenario for maximum clarity and maintainability.",
    ],
    allow_file_patterns=[
        r"^tests/(?:[A-Za-z0-9_]+/)*test_[A-Za-z0-9_]+(?:_[A-Za-z0-9_]+)*\.py$",
    ],
)
