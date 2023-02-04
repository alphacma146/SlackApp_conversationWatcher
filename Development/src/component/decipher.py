# Standard lib
from pathlib import Path
# Third party
from Crypto.Cipher import AES
# Saif made
from .abst_app import BaseAppFunction

KEY_TAIL = "TK"


class Decipher(BaseAppFunction):
    """暗号化ファイルを解読
    """

    def __init__(self, crypto_path: Path):
        """constructor

        Parameters
        ----------
        crypto_path: Path
            暗号化ファイルのパス
        """
        self.__file_path = crypto_path

    def execute(self, key: str) -> tuple[bool, str]:
        """暗号化解除を試みる

        Parameters
        ----------
        key: str
            ユーザー入力の解除キー文字列

        Returns
        ----------
        tuple[bool, str]
            解除成功だとTrue, 解読文字列
            解除成功だとFalse, None
        """
        key = (str(key) * 2 + KEY_TAIL).encode()
        if len(key) != AES.block_size:
            return False, None

        with open(self.__file_path, "rb") as f:
            nonce, tag, ciphertext = [f.read(x) for x in (
                AES.block_size, AES.block_size, -1
            )]

        cipher = AES.new(key, AES.MODE_EAX, nonce)
        try:
            decrypted_token = cipher.decrypt_and_verify(ciphertext, tag)
        except ValueError:
            return False, None

        return True, decrypted_token.decode()

    def ciphering(self, key: str, target_text: str) -> bool:
        """テキストを暗号化する

        Parameters
        ----------
        key: str
            キー文字列：7文字
        target_text: str
            ターゲット

        Returns
        ----------
        bool
            暗号化できたらTrue
        """
        key = (str(key) * 2 + KEY_TAIL).encode()
        if len(key) != AES.block_size or len(target_text) == 0:
            return False

        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(target_text)
        nonce = cipher.nonce

        # 上書きなので注意
        with open(self.__file_path, "wb") as f:
            for text in (nonce, tag, ciphertext):
                f.write(text)

        return True
