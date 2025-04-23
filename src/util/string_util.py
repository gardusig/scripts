import base64
import re
from typing import Optional

pattern = re.compile(
    r"""
    (?P<fence>`{3,})        # capture opening fence of 3+ backticks
    (?P<inner>[\s\S]*?)     # lazily grab everything inside the fence
    (?P=fence)              # closing fence (must match opener)
    """,
    re.VERBOSE
)


def extract_base64json_block(response: str) -> str:
    """
    Extracts the Base64 string from a ```base64json ... ``` fenced block.
    Raises if not found.
    """
    pattern = re.compile(
        r"```base64json\s*\n(?P<b64>[\s\S]+?)\n?```",
        re.DOTALL
    )
    match = pattern.search(response)
    if not match:
        raise RuntimeError("⛔️ No ```base64json``` fenced block found in response")
    return match.group("b64").strip()


def decode_b64(path: str, b64_content: str) -> Optional[str]:
    if not isinstance(path, str) or not isinstance(b64_content, str):
        print("Skipping invalid entry: %r → %r", path, b64_content)
        return None
    try:
        clean_b64 = "".join(b64_content.split())
        raw = base64.b64decode(clean_b64)
        return raw.decode("utf-8", errors="replace")
    except Exception as err:
        raise ValueError(f"Failed to Base64-decode `{path}`: {err}")
