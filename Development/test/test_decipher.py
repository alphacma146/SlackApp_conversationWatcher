import pytest
from unittest import mock
from pathlib import Path
from Crypto.Cipher import AES
from src.component.decipher import Decipher


class TestFetchData():

    @pytest.fixture
    def test_obj(self):
        target = Decipher(Path())

        return target

    @pytest.mark.parametrize("key, ret", [
        ("QWERTYU", (True, "TEXTTEXTTEXT")),
        (1234567, (True, "TEXTTEXTTEXT")),
    ])
    def test_execute(self, test_obj, key, ret):
        file_mock = mock.MagicMock()
        file_mock.read = mock.MagicMock(return_value="text")
        cipher_mock = mock.MagicMock()
        cipher_mock.decrypt_and_verify = mock.MagicMock(
            return_value=ret[1].encode()
        )
        with (
            mock.patch("builtins.open", file_mock),
            mock.patch.object(AES, "new", return_value=cipher_mock)
        ):
            assert test_obj.execute(key) == ret

    @pytest.mark.parametrize("key", [
        "",
        "ASDF",
        1234,
    ])
    def test_execute_anomaly(self, test_obj, key):
        assert test_obj.execute(key) == (False, None)

    @pytest.mark.parametrize("key, ret", [
        ("QWERTYU", (True, "TEXTTEXTTEXT")),
    ])
    def test_execute_error(self, test_obj, key, ret):
        file_mock = mock.MagicMock()
        file_mock.read = mock.MagicMock(return_value="text")
        cipher_mock = mock.MagicMock()
        cipher_mock.decrypt_and_verify = mock.MagicMock(
            side_effect=ValueError
        )
        with (
            mock.patch("builtins.open", file_mock),
            mock.patch.object(AES, "new", return_value=cipher_mock)
        ):
            assert test_obj.execute(key) == (False, None)

    @pytest.mark.parametrize("key, target_text", [
        ("QWERTYU", "TEXTTEXTTEXT"),
        (1234567, "TEXTTEXTTEXT"),
    ])
    def test_ciphering(self, test_obj, key, target_text):
        file_mock = mock.MagicMock()
        cipher_mock = mock.MagicMock()
        cipher_mock.encrypt_and_digest = mock.MagicMock(
            return_value=(b"TEXTTEXTTEXT", b"tagtagtag")
        )
        with (
            mock.patch("builtins.open", file_mock),
            mock.patch.object(AES, "new", return_value=cipher_mock)
        ):
            assert test_obj.ciphering(key, target_text) is True

    @pytest.mark.parametrize("key, target_text", [
        ("", ""),
        ("QWERTYU", ""),
        ("", "TEXTTEXTTEXT"),
        ("QWER", "TEXTTEXTTEXT"),
    ])
    def test_ciphering_anomaly(self, test_obj, key, target_text):
        assert test_obj.ciphering(key, target_text) is False
