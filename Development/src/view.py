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
# Self made
from control import Control
from appconfig import get_logger, MessageText


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
        self.__msgtex = MessageText()

        self.__create_popup()
        self.ver_text = version.rsplit(".", 1)[0]

    def update_layout(self):

        self.ids.spinner.values = self.__control.get_channelname_list(True)
        self.ids.information.text = self.make_infotext()

    def make_infotext(self) -> str:

        file_size = self.__control.dbfile_size()

        file_info = (
            "DataBase SIZE".ljust(23, " ")
            + f"{file_size} MB"
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

    def __create_popup(self):

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

    def show_license(self):
        self.__license_pu.open()

    def show_message(self, text: str):
        self.__message_pu.content.ids.message_text.text = text
        self.__message_pu.open()

    def show_channelset(self):
        self.__channelset_pu.open()

    def show_fetch(self):
        self.__fetch_pu.content.ids.channel_name.text = self.ids.spinner.text
        self.__fetch_pu.open()

    def show_output(self):
        self.__output_pu.open()


class BasePopup(BoxLayout):

    def __init__(self, close_func, popshow_func):
        super().__init__()
        self.close = close_func
        self.error_pop = popshow_func


class LicensePopup(BoxLayout):

    def __init__(self, root_path):
        super().__init__()

        with open(root_path / "LICENSE", "r") as f:
            text = f.read()
        self.ids.license_text.text = text


class MessagePopup(BoxLayout):

    def __init__(self):
        super().__init__()


class ChannelSetPopup(BasePopup):

    def __init__(
            self,
            control: Control,
            message: MessageText,
            spinner,
            close_func,
            show_func,
            update_func
    ):
        super().__init__(close_func, show_func)
        self.__control = control
        self.__msgtex = message
        self.__spinner = spinner
        self.update_window = update_func

    def close_popup(self):
        self.close()
        self.refresh_layout()

    def on_command(self):

        if self.ids.remove_switch.active:
            result = self.__delete_channel()

        else:
            result = self.__new_channel()

        if result:
            self.update_window()
            self.refresh_layout()
            self.close()

    def __new_channel(self):

        def replace_space(text: str):
            return text.replace(" ", "_").replace("　", "＿")

        name_text = replace_space(self.ids.channel_name.text)
        id_text = replace_space(self.ids.channel_id.text)

        if any([len(name_text) == 0, len(id_text) == 0]):
            self.error_pop(self.__msgtex.no_text)
            return

        if not id_text.isascii():
            self.error_pop(self.__msgtex.not_ascii.replace("<>", "ID"))
            return

        self.__control.set_channel(id_text, name_text)

        return True

    def __delete_channel(self):

        target = self.__spinner.text
        id_text = self.ids.channel_id.text
        self.error_pop(self.__msgtex.delete_item.replace("<>", target))
        self.__control.del_channel(id_text)

        return True

    def switch_click(self):

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

    def refresh_layout(self):

        self.ids.channel_name.text = ""
        self.ids.channel_id.text = ""
        self.ids.remove_switch.active = False

    def __abled_button(self, able: bool):

        self.ids.ok_button.disabled = not able
        self.ids.cancel_button.disabled = not able
        self.ids.channel_name.disabled = not able
        self.ids.channel_id.disabled = not able


class FetchPopup(BasePopup):

    def __init__(self, control: Control, close_func, show_func, update_func):
        super().__init__(close_func, show_func)
        self.__control = control
        self.update_window = update_func

    def close_popup(self):
        self.update_window()
        self.close()
        self.refresh_layout()

    def on_command(self):

        self.refresh_layout()
        self.__abled_button(False)
        threading.Thread(target=self.__process).start()

    def __process(self):

        ret = self.__control.fetch_data(
            self.ids.channel_name.text,
            self.ids.progressbar,
            self.ids.progress_label
        )
        if ret is not None:
            self.error_pop(ret)

        self.__abled_button(True)

    def __abled_button(self, able: bool):

        self.ids.ok_button.disabled = not able
        self.ids.cancel_button.disabled = not able

    def refresh_layout(self):

        self.ids.progressbar.value = 0
        self.ids.progress_label.text = "xxxx / xxxx"


class OutputPopup(BasePopup):

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
        super().__init__(close_func, show_func)
        self.__control = control
        self.__msgtex = message
        self.save_path = str(exe_path)
        self.__spinner = spinner

    def close_popup(self):
        self.close()
        self.refresh_layout()

    def on_command(self):

        target = self.__spinner.text
        start = self.ids.start_date.text
        end = self.ids.end_date.text
        save_path = self.ids.save_directory.text
        save_path = re.sub("^\\[.{,10}\\]", "", save_path)
        save_path = re.sub("\\[.{,5}\\]$", "", save_path)

        if target is None:
            self.error_pop(self.__msgtex.no_channel)
            return

        self.__control.output_data(save_path, target, start, end)
        self.error_pop(self.__msgtex.output_complete.replace("<>", target))

    def show_filedialog(self):
        pass

    def refresh_layout(self):

        self.ids.start_date.text = ""
        self.ids.end_date.text = ""


class InitPopup(BasePopup):

    def __init__(self, control: Control, close_func, setlayout_func):
        super().__init__(close_func, None)
        self.__control = control
        self.update_layout = setlayout_func

    def on_command(self):

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
    def __init__(self, version: str, root_path: Path, exe_path: Path):
        super().__init__()
        self.__version = version
        self.__root_path = root_path
        self.__exe_path = exe_path
        self.__widget = None
        self.__control = Control(exe_path, root_path)
        Builder.load_file(str(self.__root_path / "view_layout.kv"))
        self.__set_init()
        self.title = "SlackLogAccumulator"

        self.__logger = get_logger(__name__)

    def __set_init(self):
        Config.set('graphics', 'fullscreen', '0')
        Config.set('graphics', 'width', '520')
        Config.set('graphics', 'height', '350')
        resource_add_path('c:/Windows/Fonts')
        LabelBase.register(DEFAULT_FONT, 'msgothic.ttc')

    def on_start(self):
        if not self.__control.isexist_dbfile():
            self.__logger.info("isexist_dbfile FALSE")
            init_pu = Popup(
                title="First StartUp!",
                content=InitPopup(
                    self.__control,
                    close_func=lambda: init_pu.dismiss(),
                    setlayout_func=self.__widget.update_layout
                ),
                size_hint=(0.6, 0.6),
                auto_dismiss=False
            )
            init_pu.open()
        else:
            self.__logger.info("isexist_dbfile TRUE")
            self.__control.start_up()
            self.__widget.update_layout()

    def build(self):

        self.__widget = RootWidget(
            self.__control,
            self.__version,
            self.__root_path,
            self.__exe_path
        )

        return self.__widget
