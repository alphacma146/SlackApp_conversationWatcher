# Third party
from kivy.app import App
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
# Self made
from control import Control


class RootWidget(BoxLayout):

    ver_text = StringProperty()

    def __init__(self, version):
        super().__init__()
        self.ver_text = version.rsplit(".", 1)[0]

    # ボタンをクリック時
    def on_command(self, **kwargs):
        # self.ver_text = self.ids.text1.text
        pass


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
