# Standard lib
import time
from pathlib import Path
import threading
import re
# Third party
from kivy.app import App
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.clock import mainthread
# Self made
from control import Control
from appconfig import get_logger, MessageText


class RootWidget(BoxLayout):
    """ウィジェット

    Attributes
    ----------
    """

    ver_text = StringProperty()

    def __init__(
            self,
            control: Control,
            version: str,
            root_path: Path,
            exe_path: Path
    ):
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
        super().__init__()
        self.__control = control
        self.__root_path = root_path
        self.__exe_path = exe_path
        self.__msgtex = MessageText()

        self.__create_popup()
        self.ver_text = version.rsplit(".", 1)[0]

    def update_layout(self) -> None:
        """スピナーとインフォメーションテキストを更新
        """
        self.ids.spinner.values = self.__control.get_channelname_list(True)
        self.ids.information.text = self.make_infotext()

    def make_infotext(self) -> str:
        """DBの情報からテキストを生成する

        Returns
        ----------
        str
            インフォメーションテキストのテキスト
        """
        file_size = round(self.__control.dbfile_size(), 3)
        size_text = f"{file_size}".ljust(5, "0")

        file_info = (
            "DataBase SIZE"
            + f"{size_text} MB".rjust(18, " ")
        )
        table_info = "\n"

        for key, value in self.__control.db_info().items():
            name = self.__control.convert_channel_name_id(key)
            if name is None:
                continue
            table_info += (
                "\n"
                + name
                + "\n"
                + f"mem:{value[0]} record:{value[1]}".rjust(31, " ")
            )

        self.ids.progressbar.value = file_size / 16 / 1024

        return file_info + table_info

    def __create_popup(self) -> None:
        """ポップアップを生成
        """
        self.__license_pu = Popup(
            title="LICENSE",
            content=LicensePopup(self.__root_path),
            size_hint=(0.9, 0.9),
        )

        self.__message_pu = Popup(
            title="MESSAGE",
            content=MessagePopup(),
            size_hint=(0.5, 0.5),
        )

        self.__channelset_pu = Popup(
            title="SET CHANNEL",
            content=ChannelSetPopup(
                self.__control,
                self.__msgtex,
                self.ids.spinner,
                close_func=lambda: self.__channelset_pu.dismiss(),
                show_func=self.show_message,
                update_func=self.update_layout
            ),
            size_hint=(0.9, 0.9),
            auto_dismiss=False
        )

        self.__fetch_pu = Popup(
            title="FETCH",
            content=FetchPopup(
                self.__control,
                self.__msgtex,
                close_func=lambda: self.__fetch_pu.dismiss(),
                show_func=self.show_message,
                update_func=self.update_layout
            ),
            size_hint=(0.9, 0.9),
            auto_dismiss=False
        )

        self.__output_pu = Popup(
            title="OUTPUT",
            content=OutputPopup(
                self.__control,
                self.__msgtex,
                self.__exe_path,
                self.ids.spinner,
                close_func=lambda: self.__output_pu.dismiss(),
                show_func=self.show_message
            ),
            size_hint=(0.9, 0.9),
            auto_dismiss=False
        )

    def show_license(self) -> None:
        """ポップアップを表示する
        """
        self.__license_pu.open()

    @mainthread
    def show_message(self, text: str) -> None:
        """ポップアップを表示する

        Parameters
        ----------
        text: str
            ポップアップで表示するテキスト

        Note
        ----------
        サブスレッドからコールするためデコレータでmainthreadを指定する
        """
        self.__message_pu.content.ids.message_text.text = text
        self.__message_pu.open()

    def show_channelset(self) -> None:
        """ポップアップを表示する
        """
        self.__channelset_pu.open()

    def show_fetch(self) -> None:
        """ポップアップを表示する
        """
        self.__fetch_pu.content.ids.channel_name.text = self.ids.spinner.text
        self.__fetch_pu.open()

    def show_output(self) -> None:
        """ポップアップを表示する
        """
        self.__output_pu.open()


class BasePopup(BoxLayout):
    """ポップアップクラスの基底クラス
    """

    def __init__(self, close_func, popshow_func):
        """constructor

        Parameters
        ----------
        close_func
            ポップアップを閉じる関数
        popshow_func
            ポップアップ内でメッセージポップアップ表示する関数
        """
        super().__init__()
        self.close = close_func
        self.error_pop = popshow_func


class LicensePopup(BoxLayout):
    """ライセンス表示用ポップアップ
    """

    def __init__(self, root_path):
        """constructor

        Parameters
        ----------
        root_path
            実行ファイルのパス
        """
        super().__init__()

        with open(root_path / "LICENSE", "r") as f:
            text = f.read()
        self.ids.license_text.text = text


class MessagePopup(BoxLayout):
    """主にエラーメッセージなどを表示するポップアップ
    """

    def __init__(self):
        """constructor
        """
        super().__init__()


class ChannelSetPopup(BasePopup):
    """チャンネルを操作するポップアップ
    """

    def __init__(
            self,
            control: Control,
            message: MessageText,
            spinner,
            close_func,
            show_func,
            update_func
    ):
        """constructor

        Parameters
        ----------
        control: Control
        message: MessageText
        spinner
            スピナーオブジェクト
        close_func
            ポップアップを閉じる関数
        show_func
            ポップアップ内でメッセージポップアップ表示する関数
        update_func
            メインウィンドウをアップデートする関数
        """
        super().__init__(close_func, show_func)
        self.__control = control
        self.__msgtex = message
        self.__spinner = spinner
        self.update_window = update_func

    def close_popup(self) -> None:
        """自身を閉じる

        Note
        ----------
        ボタンにバインドしている
        """
        self.close()
        self.refresh_layout()

    def on_command(self) -> None:
        """ボタン押下時の挙動

        Note
        ----------
        トグルスイッチの状態で処理が変わる
        """
        if self.ids.remove_switch.active:
            result = self.__delete_channel()
        else:
            result = self.__new_channel()

        if result:
            self.update_window()
            self.refresh_layout()
            self.close()

    def __new_channel(self) -> bool:
        """新しいチャンネルを登録する

        Returns
        ----------
        bool
            成功ならTrue
            失敗ならFalse

        Note
        ----------
        入力エラー
            テキストインプットが空
            半角英数字じゃない
            一文字目が数字
        """
        def replace_space(text: str):
            return text.replace(" ", "_").replace("　", "＿")

        name_text = replace_space(self.ids.channel_name.text)
        id_text = replace_space(self.ids.channel_id.text)

        if any([len(name_text) == 0, len(id_text) == 0]):
            self.error_pop(self.__msgtex.no_text)
            return False

        if not id_text.isascii():
            self.error_pop(self.__msgtex.not_ascii.replace("<>", "ID"))
            return False

        if id_text[0].isdecimal():
            self.error_pop(self.__msgtex.not_ascii.replace("<>", "ID"))
            return False

        self.__control.set_channel(id_text, name_text)

        return True

    def __delete_channel(self) -> bool:
        """登録してあるチャンネルを消す
        """
        target = self.__spinner.text
        id_text = self.ids.channel_id.text
        self.error_pop(self.__msgtex.delete_item.replace("<>", target))
        self.__control.del_channel(id_text)

        return True

    def switch_click(self) -> None:
        """トグルスイッチ押下時の挙動
        """
        target = self.__spinner.text

        if self.ids.remove_switch.active:
            if len(target) == 0:
                self.__abled_button(False)
            else:
                df = self.__control.get_channelname_list()
                target_id = df[df["channel_name"] == target]["channel_id"]
                self.ids.channel_name.text = target
                self.ids.channel_name.disabled = True
                self.ids.channel_id.text = target_id.to_string(index=False)
                self.ids.channel_id.disabled = True

        else:
            self.__abled_button(True)
            self.ids.channel_name.text = ""
            self.ids.channel_id.text = ""

    def refresh_layout(self) -> None:
        """ポップアップウィンドウの表示を初期化
        """
        self.ids.channel_name.text = ""
        self.ids.channel_id.text = ""
        self.ids.remove_switch.active = False

    def __abled_button(self, able: bool):
        """ボタンの利用可否を操作、ついでにテキストインプットも
        """

        self.ids.ok_button.disabled = not able
        self.ids.cancel_button.disabled = not able
        self.ids.channel_name.disabled = not able
        self.ids.channel_id.disabled = not able


class FetchPopup(BasePopup):
    """ログを取得するポップアップ
    """

    def __init__(
            self,
            control: Control,
            message: MessageText,
            close_func,
            show_func,
            update_func
    ):
        """constructor

        Parameters
        ----------
        control: Control
        message: MessageText
        close_func
            ポップアップを閉じる関数
        show_func
            ポップアップ内でメッセージポップアップ表示する関数
        update_func
            メインウィンドウをアップデートする関数
        """
        super().__init__(close_func, show_func)
        self.__control = control
        self.__msgtex = message
        self.update_window = update_func

    def close_popup(self) -> None:
        """自身を閉じる

        Note
        ----------
        ボタンにバインドしている
        """
        self.update_window()
        self.close()
        self.refresh_layout()

    def on_command(self) -> None:
        """ボタン押下時の処理

        Note
        ----------
        ウィンドウのレンダリングの関係でサブスレッドで回す
        孫スレッドまでたつ
        """
        if self.ids.channel_name.text == "":
            self.error_pop(self.__msgtex.no_channel)
            return

        self.refresh_layout()
        self.__abled_button(False)
        th = threading.Thread(target=self.__process)
        th.start()
        th.join()

    def __process(self) -> None:
        """ボタン押下時の処理

        Note
        ----------
        サブスレッドで実行する処理
        """
        ret = self.__control.fetch_data(
            self.ids.channel_name.text,
            self.ids.progressbar,
            self.ids.progress_label
        )
        if ret is not None:
            self.error_pop(ret)

        self.__abled_button(True)

    def __abled_button(self, able: bool) -> None:
        """ボタンの有効化切り替え

        Parameters
        ----------
        able : str
            有効にするならTrue
        """
        self.ids.ok_button.disabled = not able
        self.ids.cancel_button.disabled = not able

    def refresh_layout(self) -> None:
        """ポップアップウィンドウの表示を初期化
        """
        self.ids.progressbar.value = 0
        self.ids.progress_label.text = "xxxx / xxxx"


class OutputPopup(BasePopup):
    """ファイル出力ポップアップ
    """

    save_path = StringProperty()

    def __init__(
            self,
            control: Control,
            message: MessageText,
            exe_path: Path,
            spinner,
            close_func,
            show_func
    ):
        """constructor

        Parameters
        ----------
        control: Control
        message: MessageText
        exe_path: Path
            exeファイルのパス
        spinner
            スピナーオブジェクト
        close_func
            ポップアップを閉じる関数
        show_func
            ポップアップ内でメッセージポップアップ表示する関数
        """
        super().__init__(close_func, show_func)
        self.__control = control
        self.__msgtex = message
        self.save_path = str(exe_path)
        self.__spinner = spinner

    def close_popup(self) -> None:
        """自身を閉じる
        """
        self.close()
        self.refresh_layout()

    def on_command(self) -> None:
        """ボタン押下時の処理
        """
        if self.__spinner.text == "":
            self.error_pop(self.__msgtex.no_channel)
            return

        target = self.__spinner.text
        start = self.ids.start_date.text
        end = self.ids.end_date.text
        save_path = self.ids.save_directory.text
        save_path = re.sub("^\\[.{,10}\\]", "", save_path)
        save_path = re.sub("\\[.{,5}\\]$", "", save_path)

        if target is None:
            self.error_pop(self.__msgtex.no_channel)
            return

        ret = self.__control.output_data(save_path, target, start, end)
        if ret:
            self.error_pop(self.__msgtex.output_complete.replace("<>", target))
        else:
            self.error_pop(self.__msgtex.output_none)

    def show_filedialog(self) -> None:
        """filechooserがうまく使えないので未実装
        """
        pass

    def refresh_layout(self) -> None:
        """ポップアップウィンドウの表示を初期化
        """
        self.ids.start_date.text = ""
        self.ids.end_date.text = ""


class InitPopup(BasePopup):
    """初回起動時に表示するポップアップ"""

    def __init__(self, control: Control, close_func, update_func):
        """constructor

        Parameters
        ----------
        control: Control
        close_func
            ポップアップを閉じる関数
        update_func
            メインウィンドウをアップデートする関数
        """
        super().__init__(close_func, None)
        self.__control = control
        self.update_layout = update_func

    def on_command(self) -> None:
        """ボタン押下時の処理
        """
        ret = self.__control.release_lock(self.ids.key_input.text)

        if not ret:
            self.ids.result_message.text = "Failure"
        else:
            time.sleep(0.5)
            self.ids.result_message.text = "Congratulations!"

        self.ids.key_input.text = ""

        if ret:
            self.update_layout()
            self.close()


class View(App):
    """GUIのウィンドウを生成する
    """

    def __init__(self, version: str, root_path: Path, exe_path: Path):
        """constructor

        Parameters
        ----------
        version: str
        root_path: Path
            実行ファイルのパス
        exe_path: Path
            exeファイルのパス
        """
        super().__init__()
        self.__version = version
        self.__root_path = root_path
        self.__exe_path = exe_path
        self.__widget = None
        self.__control = Control(root_path, exe_path)
        Builder.load_file(str(self.__root_path / "view_layout.kv"))
        self.__set_init()
        self.title = "SlackLogAccumulator"

        self.__logger = get_logger(__name__)

    def __set_init(self) -> None:
        """初期設定
        """
        Config.set('graphics', 'fullscreen', '0')
        Config.set('graphics', 'width', '520')
        Config.set('graphics', 'height', '350')
        resource_add_path('c:/Windows/Fonts')
        LabelBase.register(DEFAULT_FONT, 'msgothic.ttc')

    def on_start(self) -> None:
        """起動直後の処理
        """
        if not self.__control.isexist_dbfile():
            self.__logger.info("isexist_dbfile FALSE")
            init_pu = Popup(
                title="First StartUp!",
                content=InitPopup(
                    self.__control,
                    close_func=lambda: init_pu.dismiss(),
                    update_func=self.__widget.update_layout
                ),
                size_hint=(0.6, 0.6),
                auto_dismiss=False
            )
            init_pu.open()
        else:
            self.__logger.info("isexist_dbfile TRUE")
            self.__control.start_up()
            self.__widget.update_layout()

    def on_stop(self) -> None:
        """終了時の処理
        """
        self.__control.close_window()

    def build(self) -> RootWidget:
        """run()でコールされる
        """
        self.__widget = RootWidget(
            self.__control,
            self.__version,
            self.__root_path,
            self.__exe_path
        )

        return self.__widget
