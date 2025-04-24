import os
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple


class CommandRunner:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path).resolve()
        if not self.base_path.is_dir():
            raise ValueError(f"Invalid base path: {self.base_path}")

    def run(
        self, cmd: List[str], env: Optional[dict] = None, activate_venv: bool = True
    ) -> Tuple[int, str, str]:
        shell_commands = []

        if activate_venv:
            activate_path = self.base_path / "venv" / "bin" / "activate"
            shell_commands.append(f"source {activate_path}")
        shell_commands.append(cmd)

        shell_command = " && ".join(shell_commands)

        result = subprocess.run(
            shell_command,
            cwd=self.base_path,
            capture_output=True,
            text=True,
            env={**os.environ, **(env or {})},
            shell=True,
            executable="/bin/bash",
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()

    def run_pytest(self, test_path: str = "tests") -> Tuple[int, str, str]:
        return self.run([f"pytest {test_path}"])

    def run_black(self, target: str = ".") -> Tuple[int, str, str]:
        return self.run(["black", target])
