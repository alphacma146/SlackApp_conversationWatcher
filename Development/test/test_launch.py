
from unittest import mock
from pathlib import Path
import pytest
from src.launch import (
    main,
    get_version,
    get_root,
    get_exe_directory
)


# @pytest.mark.asyncio
# def test_main():
#    assert main() is None

def test_get_version():
    assert get_version() == 'Ver. 0.9.0.0'


# def test_get_root():
#    assert get_root() is Path
#
#
# def test_get_exe_directory():
#    assert get_exe_directory() is Path
