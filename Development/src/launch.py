# Standard lib
import sys
from pathlib import Path
# Self made
from view import View


def main():
    """main
    """
    root_path = get_root()
    exe_path = get_exe_directory()
    version = get_version()
    View(version=version, root_path=root_path, exe_path=exe_path).run()


def get_version() -> str:
    """app version

    Returns:
    ----------
    str
        Ver. a.b.c.d
        a: メジャーバージョン
        b: マイナーバージョン
        c: ビルドバージョン
        d: リビジョン
    """

    return "Ver. 1.0.0.0"


def get_root() -> Path:
    """実行ファイルのルートディレクトリパス

    Returns
    ----------
    Path
        Windows path

    Note
    ----------
    exeファイルで実行時はtempフォルダの_MEIPASSに展開される
    """
    if getattr(sys, "frozen", False):
        ret = Path(sys._MEIPASS)
    else:
        ret = Path(__file__).parent

    return ret.absolute()


def get_exe_directory() -> Path:
    """exeファイルのパス

    Returns
    ----------
    Path
        Windows path
    """
    if getattr(sys, "frozen", False):
        ret = Path(sys.argv[0])
    else:
        ret = Path(__file__)

    return ret.parent.absolute()


if __name__ == "__main__":
    main()
