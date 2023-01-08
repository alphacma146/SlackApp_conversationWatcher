# Standard lib
import sys
from pathlib import Path
# Self made
from view import View


def main():
    root_path = get_root()
    exe_path = get_exe_directory()
    version = get_version()
    View(version=version, root_path=root_path, exe_path=exe_path).run()


def get_version() -> str:

    return "Ver. 0.9.0.0"


def get_root() -> Path:
    if getattr(sys, "frozen", False):
        ret = Path(sys._MEIPASS)
    else:
        ret = Path(__file__).parent

    return ret.absolute()


def get_exe_directory() -> Path:
    if getattr(sys, "frozen", False):
        ret = Path(sys.argv[0])
    else:
        ret = Path(__file__).parent

    return ret.absolute()


if __name__ == "__main__":
    main()
