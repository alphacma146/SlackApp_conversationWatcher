# Standard lib
from pathlib import Path
# Third party
from Crypto.Cipher import AES
# Saif made
from model import Model

KEY_TAIL = "TK"


class Control():

    def __init__(self, exe_path: Path, root_path: Path) -> None:

        self.__model = Model(exe_path)
        self.__exe_path = exe_path
        self.__root_path = root_path
        self.__token = None

    def isexist_dbfile(self):

        path = self.__exe_path / self.__model.get_dbfilename()

        return path.exists()

    def start_up(self, token: str = None):

        self.__model.initialize(first=True)
        if token is None:
            token = self.__model.get_token()
        else:
            self.__model.insert_token(token)
        self.__token = token

    def release_lock(self, key: str):

        key = (key * 2 + KEY_TAIL).encode()
        if len(key) != AES.block_size:
            return False

        with open(self.__root_path / "cripto_token.dat", "rb") as f:
            nonce, tag, ciphertext = [f.read(x) for x in (
                AES.block_size, AES.block_size, -1
            )]

        cipher = AES.new(key, AES.MODE_EAX, nonce)
        try:
            decrypted_token = cipher.decrypt_and_verify(ciphertext, tag)
        except ValueError:
            return False

        self.start_up(decrypted_token)

        return True

    def get_channel_list(self):

        ret = self.__model.get_channel()

        return ret.values()
