import pytest
import sys
from unittest import mock
from pathlib import Path
from src.launch import (
    get_version,
    get_root,
    get_exe_directory
)


def test_get_version():
    assert isinstance(get_version(), str)


@pytest.mark.parametrize("isexist", [
    True,
    False
])
def test_get_root(isexist):
    setattr(sys, "frozen", None)
    setattr(sys, "_MEIPASS", None)
    with (
        mock.patch.object(sys, "frozen", isexist),
        mock.patch.object(sys, "_MEIPASS")
    ):
        assert isinstance(get_root(), Path)


@pytest.mark.parametrize("isexist", [
    True,
    False
])
def test_get_exe_directory(isexist):
    setattr(sys, "frozen", None)
    with mock.patch.object(sys, "frozen", isexist):
        assert isinstance(get_exe_directory(), Path)
