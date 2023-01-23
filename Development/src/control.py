# Standard lib
from pathlib import Path
# Third party
from Crypto.Cipher import AES
# Saif made
from model import Model


class Control():

    def __init__(self, exe_path: Path, root_path: Path) -> None:

        self.__model = Model(exe_path)
        self.__exe_path = exe_path
        self.__root_path = root_path

    def isexist_dbfile(self):

        path = self.__exe_path / self.__model.get_dbfilename()

        return path.exists()

    def release_lock(self, key: str):

        key = (key * 2 + "TK").encode()
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

        self.__model.initialize()
        print(decrypted_token)

        return True

    def set_spinneritems(self):

        tables = self.__model.get_dbtable()

    def create_table(self):
        pass
