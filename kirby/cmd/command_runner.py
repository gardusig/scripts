# from __future__ import annotations

# import os
# import subprocess
# from dataclasses import dataclass
# from pathlib import Path
# from typing import Mapping


# @dataclass(slots=True)
# class CommandResult:
#     code: int
#     out: str
#     err: str


# class CommandRunner:
#     """Run commands inside *base_path* (optionally inside its venv)."""

#     def __init__(self, base_path: Path | str) -> None:
#         self.base_path = Path(base_path).resolve(strict=True)

#     # ──────────────────────────────────────────────────────────
#     def get_startup_commands(self) -> list[str]:
#         venv_bin = self.base_path / "venv" / "bin" / "activate"
#         return [f"source {venv_bin}"]

#     def _run(
#         self,
#         cmd_list: list[str],
#         env: Mapping[str, str] | None = None,
#         check: bool = False,
#     ) -> CommandResult:
#         commands = self.get_startup_commands()
#         commands.extend(cmd_list)

#         cmd = " && ".join(commands)

#         proc = subprocess.run(
#             cmd,
#             cwd=self.base_path,
#             env={**os.environ, **(env or {})},
#             text=True,
#             capture_output=True,
#             check=check,
#         )
#         return CommandResult(proc.returncode, proc.stdout.strip(), proc.stderr.strip())

#     # ───────────── public helpers ─────────────
#     def pytest(self, paths: list[str]) -> CommandResult:
#         paths = [str(p) for p in paths] or ["tests"]
#         return self._run(["pytest", *paths])

#     def black(self, *targets: str, use_venv: bool = True) -> CommandResult:
#         return self._run(["black", targets], use_venv=use_venv)

#     def custom(
#         self,
#         *cmd: str,
#         env: Mapping[str, str] | None = None,
#         use_venv: bool = True,
#     ) -> CommandResult:
#         return self._run([str(c) for c in cmd], env=env, use_venv=use_venv)
