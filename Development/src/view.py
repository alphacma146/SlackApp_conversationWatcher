# Standard lib
import time
from pathlib import Path
# Third party
from kivy.app import App
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
# Self made
from control import Control


class RootWidget(BoxLayout):

    ver_text = StringProperty()

    def __init__(
            self,
            control: Control,
            version: str,
            root_path: Path,
            exe_path: Path
    ):
        super().__init__()
        self.__control = control
        self.__root_path = root_path
        self.__exe_path = exe_path
        self.__license_pu = None
        self.__channelset_pu = None
        self.__fetch_pu = None
        self.__output_pu = None

        self.ver_text = version.rsplit(".", 1)[0]

    def show_license(self):
        if self.__license_pu is None:
            self.__license_pu = Popup(
                title="LICENSE",
                content=LicensePopup(self.__root_path),
                size_hint=(0.9, 0.9),
            )
        self.__license_pu.open()

    def show_channelset(self):
        if self.__channelset_pu is None:
            self.__channelset_pu = Popup(
                title="SET CHANNEL",
                content=ChannelSetPopup(
                    self.__control,
                    close_func=lambda: self.__channelset_pu.dismiss()
                ),
                size_hint=(0.9, 0.9),
                auto_dismiss=False
            )
        self.__channelset_pu.open()

    def show_fetch(self):
        if self.__fetch_pu is None:
            self.__fetch_pu = Popup(
                title="FETCH",
                content=FetchPopup(
                    self.__control,
                    close_func=lambda: self.__fetch_pu.dismiss()
                ),
                size_hint=(0.9, 0.9),
                auto_dismiss=False
            )
        self.__fetch_pu.open()

    def show_output(self):
        if self.__output_pu is None:
            self.__output_pu = Popup(
                title="OUTPUT",
                content=OutputPopup(
                    self.__control,
                    self.__exe_path,
                    close_func=lambda: self.__output_pu.dismiss(),
                ),
                size_hint=(0.9, 0.9),
            )
        self.__output_pu.open()


class BasePopup(BoxLayout):

    def __init__(self, close_func):
        super().__init__()
        self.close = close_func


class LicensePopup(BoxLayout):

    def __init__(self, root_path):
        super().__init__()

        with open(root_path / "LICENSE", "r") as f:
            text = f.read()
        self.ids.license_text.text = text


class ChannelSetPopup(BasePopup):

    def __init__(self, control: Control, close_func):
        super().__init__(close_func)
        self.__control = control

    def on_command(self):
        # self.ver_text = self.ids.text1.text

        pass

    def switch_click(self, widget, active):
        pass


class FetchPopup(BasePopup):

    def __init__(self, control: Control, close_func):
        super().__init__(close_func)
        self.__control = control

    # ボタンをクリック時
    def on_command(self):
        # self.ver_text = self.ids.text1.text
        pass


class OutputPopup(BasePopup):

    save_path = StringProperty()

    def __init__(self, control: Control, exe_path: Path, close_func):
        super().__init__(close_func)
        self.__control = control
        self.save_path = str(exe_path)

    def on_command(self):
        pass

    def show_filedialog(self):
        pass


class InitPopup(BasePopup):

    def __init__(self, control: Control, close_func):
        super().__init__(close_func)
        self.__control = control

    def on_command(self):

        ret = self.__control.release_lock(self.ids.key_input.text)

        if not ret:
            self.ids.result_message.text = "BAD KEY"
        else:
            time.sleep(0.5)
            self.ids.result_message.text = "Congraturations!"

        self.ids.key_input.text = ""

        if ret:
            self.close()


class View(App):
    def __init__(self, version: str, root_path: Path, exe_path: Path):
        super().__init__()
        self.__version = version
        self.__root_path = root_path
        self.__exe_path = exe_path
        self.__control = Control(exe_path, root_path)
        Builder.load_file(str(self.__root_path / "view_layout.kv"))
        self.__set_init()
        self.title = "SlackLogAccumulator"

    def __set_init(self):
        Config.set('graphics', 'fullscreen', '0')
        Config.set('graphics', 'width', '470')
        Config.set('graphics', 'height', '320')
        resource_add_path('c:/Windows/Fonts')
        LabelBase.register(DEFAULT_FONT, 'msgothic.ttc')

    def on_start(self):
        if not self.__control.isexist_dbfile():
            init_pu = Popup(
                title="First Awake!",
                content=InitPopup(
                    self.__control,
                    close_func=lambda: init_pu.dismiss()
                ),
                size_hint=(0.6, 0.6),
                auto_dismiss=False
            )
            init_pu.open()

    def build(self):
        return RootWidget(
            self.__control,
            self.__version,
            self.__root_path,
            self.__exe_path
        )
