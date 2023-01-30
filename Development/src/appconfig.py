# Standard lib
import logging
from dataclasses import dataclass


def get_logger(name: str) -> logging.Logger:
    """ロガーを生成する

    Parameters
    ----------
    name : str
        ファイル名

    Returns
    ----------
    logging.Logger

    Note
    ----------
    loggerを区別するためファイル名を引数にする
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(
        logging.Formatter('%(asctime)s %(name)s:%(levelname)s %(message)s')
    )
    logger.addHandler(sh)

    return logger


"""constructor

Parameters
----------
control: Control,
version: str,
    表示するバージョン
root_path: Path,
    実行ファイルパス
exe_path: Path
    exeファイルパス
"""


@dataclass(frozen=True)
class MessageText:
    """ポップアップするメッセージを定義する

    Attributes
    ----------
    text : str
    """
    value_error: str = "値が不正です。"
    no_text: str = "値を入力してください。"
    not_ascii: str = "<>は半角英数字で入力してください。"
    delete_item: str = "<>は削除されました。"
    no_channel: str = "チャンネルが選択されていません。"
    output_complete: str = "出力終了\n<>"
    output_none: str = "データがありません。"
