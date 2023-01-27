# Standard lib
import logging
from dataclasses import dataclass


def get_logger(name: str):

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setFormatter(
        logging.Formatter('%(asctime)s %(name)s:%(levelname)s %(message)s')
    )
    logger.addHandler(sh)

    return logger


@dataclass(frozen=True)
class MessageText:
    value_error: str = "値が不正です。"
    no_text: str = "値を入力してください。"
    full_pitch: str = "<>は半角英数字で入力してください。"
