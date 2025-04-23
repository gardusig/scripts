import base64
import pytest
from util.string_util import decode_b64, extract_base64json_block


def test_extract_base64json_block_simple():
    b64 = base64.b64encode(b"print('hello')").decode()
    resp = f"```base64json\n{b64}\n```"
    assert extract_base64json_block(resp) == b64


def test_extract_base64json_block_with_whitespace():
    b64 = base64.b64encode(b"print('x')").decode()
    messy = f"```base64json \n   {b64.strip()} \n```"
    assert extract_base64json_block(messy) == b64.strip()


def test_extract_base64json_block_missing():
    with pytest.raises(RuntimeError, match="No ```base64json``` fenced block"):
        extract_base64json_block("no base64json block here")


def test_decode_b64_valid():
    s = "hello"
    b64 = base64.b64encode(s.encode()).decode()
    assert decode_b64("f.py", b64) == s


def test_decode_b64_with_linebreaks():
    val = "hello\nworld\n"
    b64 = base64.b64encode(val.encode()).decode()
    b64_messy = f"\n{b64[:4]} \n{b64[4:]}\n"
    assert decode_b64("x", b64_messy) == val


def test_decode_b64_empty_string():
    assert decode_b64("f", "") == ""


def test_decode_b64_invalid_format():
    with pytest.raises(ValueError, match="Failed to Base64-decode `bad.txt`"):
        decode_b64("bad.txt", "not_base64!!")
