import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tokenizers import Tokenizer
import pytest


ARTIFACTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "artefacts"))


def test_tokenizer_load_and_roundtrip():
    path = os.path.join(ARTIFACTS, "tokenizer.json")
    tokenizer = Tokenizer.from_file(path)
    assert tokenizer is not None
    # smoke test encode/decode
    enc = tokenizer.encode("test")
    ids = enc.ids
    decoded = tokenizer.decode(ids)
    assert isinstance(decoded, str)


def test_missing_tokenizer_file_raises():
    with pytest.raises(Exception):
        Tokenizer.from_file(os.path.join(ARTIFACTS, "this_file_does_not_exist.json"))
