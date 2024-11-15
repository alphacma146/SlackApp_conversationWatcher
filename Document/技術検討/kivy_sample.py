from kivy.properties import StringProperty
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivy.config import Config
from kivy.lang import Builder
import sys
from pathlib import Path
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '150')
resource_add_path('c:/Windows/Fonts')
LabelBase.register(DEFAULT_FONT, 'msgothic.ttc')
if getattr(sys, 'frozen', False):
    Builder.load_file(str(Path(sys._MEIPASS, 'kivy_sample.kv')))
else:
    Builder.load_file(str(Path(__file__).parent / 'kivy_sample.kv'))


class TextWidget(Widget):
    # プロパティの追加
    text = StringProperty()

    # ボタンをクリック時
    def on_command(self, **kwargs):
        self.text = self.ids.text1.text


class TestApp(App):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        # ウィンドウのタイトル名
        self.title = 'HelloTheWorld'

    def build(self):
        return TextWidget()


if __name__ == '__main__':
    TestApp().run()
