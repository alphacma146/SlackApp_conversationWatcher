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

    def __init__(self, version):
        super().__init__()
        self.__widgets = {

        }
        self.__control = Control()
        self.ver_text = version.rsplit(".", 1)[0]

    def show_license(self):
        popup = Popup(
            title="LICENSE",
            content=LicensePopup(),
            size_hint=(0.9, 0.9),
        )
        popup.open()

    def show_channelset(self):

        popup = Popup(
            title="SET CHANNEL",
            content=ChannelSetPopup(
                self.__control,
                close_func=lambda: popup.dismiss()
            ),
            size_hint=(0.9, 0.9),
            auto_dismiss=False
        )
        popup.open()

    def show_fetch(self):
        popup = Popup(
            title="FETCH",
            content=FetchPopup(
                self.__control,
                close_func=lambda: popup.dismiss()
            ),
            size_hint=(0.9, 0.9),
            auto_dismiss=False
        )
        popup.open()

    def show_output(self):
        popup = Popup(
            title="OUTPUT",
            content=OutputPopup(
                self.__control,
                close_func=lambda: popup.dismiss()
            ),
            size_hint=(0.9, 0.9),
        )
        popup.open()


class LicensePopup(BoxLayout):

    def __init__(self):
        super().__init__()

        with open("LICENSE", "r") as f:
            text = f.read()
        self.ids.license_text.text = text


class ChannelSetPopup(BoxLayout):

    def __init__(self, control, close_func):
        super().__init__()
        self.__control = control
        self.close = close_func

    # ボタンをクリック時
    def on_command(self):
        # self.ver_text = self.ids.text1.text
        pass

    def switch_click(self, widget, active):
        pass


class FetchPopup(BoxLayout):

    def __init__(self, control, close_func):
        super().__init__()
        self.__control = control
        self.close = close_func


class OutputPopup(BoxLayout):

    def __init__(self, control, close_func):
        super().__init__()
        self.__control = control
        self.close = close_func


class View(App):
    def __init__(self, root_path, version):
        super().__init__()
        Builder.load_file(str(root_path / "view_layout.kv"))
        self.__set_init()
        self.__version = version
        self.title = "SlackLogAccumulator"

    def __set_init(self):
        Config.set('graphics', 'fullscreen', '0')
        Config.set('graphics', 'width', '470')
        Config.set('graphics', 'height', '320')
        resource_add_path('c:/Windows/Fonts')
        LabelBase.register(DEFAULT_FONT, 'msgothic.ttc')

    def build(self):
        return RootWidget(self.__version)
