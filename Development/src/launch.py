# Standard lib
import sys
from pathlib import Path
# Self made
from view import View


def main():
    root_path = get_root()
    version = get_version()
    View(root_path=root_path, version=version).run()


def get_version() -> str:

    return "Ver. 0.9.0.0"


def get_root() -> Path:
    if getattr(sys, "frozen", False):
        ret = Path(sys._MEIPASS)
    else:
        ret = Path(__file__).parent

    return ret


if __name__ == "__main__":
    main()
