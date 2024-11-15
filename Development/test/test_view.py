import pytest
from unittest import mock
from pathlib import Path
from src.view import (
    RootWidget,
    BasePopup,
    LicensePopup,
    MessagePopup,
    ChannelSetPopup,
    FetchPopup,
    OutputPopup,
    InitPopup,
    View
)


class DummyPopUp():

    def __init__(self, *args, **kwargs) -> None:
        pass


class TestRootWidget():

    @pytest.fixture
    def test_obj(self):
        self.control_mock = mock.MagicMock()
        self.root_path_mock = mock.MagicMock()
        self.exe_path_mock = mock.MagicMock()
        with mock.patch.object(RootWidget, "_RootWidget__create_popup"):
            target = RootWidget(
                self.control_mock,
                "VERSION",
                self.root_path_mock,
                self.exe_path_mock
            )

        return target

    def test_update_layout(self, test_obj):
        self.control_mock.get_channelname_list.return_value = []
        spinner_mock = mock.MagicMock()
        information_mock = mock.MagicMock()
        setattr(test_obj.ids, "spinner", spinner_mock)
        setattr(test_obj.ids, "information", information_mock)
        with (
            mock.patch.object(test_obj.ids.spinner, "values"),
            mock.patch.object(test_obj, "make_infotext")
        ):
            assert test_obj.update_layout() is None

    @pytest.mark.parametrize("name", [
        "CHANNELIDn",
        None
    ])
    def test_make_infotext(self, test_obj, name):
        self.control_mock.dbfile_size.return_value = 16.1616
        self.control_mock.db_info.return_value = {
            "CHANNELNAME1": (10, 210),
            "CHANNELNAME2": (5, 9500)
        }
        self.control_mock.convert_channel_name_id.return_value = name
        progressbar_mock = mock.MagicMock()
        setattr(test_obj.ids, "progressbar", progressbar_mock)
        with mock.patch.object(test_obj.ids.progressbar, "value"):
            assert isinstance(test_obj.make_infotext(), str)

    def test___create_popup(self, test_obj):
        # with (
        #     mock.patch("kivy.uix.popup.Popup", new=DummyPopUp),
        #     mock.patch("src.view.LicensePopup", new=DummyPopUp),
        #     mock.patch("src.view.MessagePopup", new=DummyPopUp),
        #     mock.patch("src.view.ChannelSetPopup", new=DummyPopUp),
        #     mock.patch("src.view.FetchPopup", new=DummyPopUp),
        #     mock.patch("src.view.OutputPopup", new=DummyPopUp),
        # ):
        #     assert test_obj._RootWidget__create_popup() is None
        pass

    def test_show_license(self, test_obj):
        setattr(test_obj, "_RootWidget__license_pu", None)
        with mock.patch.object(test_obj, "_RootWidget__license_pu"):
            assert test_obj.show_license() is None

    def test_show_message(self, test_obj):
        pass

    def test_show_channelset(self, test_obj):
        setattr(test_obj, "_RootWidget__channelset_pu", None)
        with mock.patch.object(test_obj, "_RootWidget__channelset_pu"):
            assert test_obj.show_channelset() is None

    def test_show_fetch(self, test_obj):
        setattr(test_obj, "_RootWidget__fetch_pu", None)
        spinner_mock = mock.MagicMock()
        setattr(test_obj.ids, "spinner", spinner_mock)
        with mock.patch.object(test_obj, "_RootWidget__fetch_pu"):
            assert test_obj.show_fetch() is None

    def test_show_output(self, test_obj):
        setattr(test_obj, "_RootWidget__output_pu", None)
        with mock.patch.object(test_obj, "_RootWidget__output_pu"):
            assert test_obj.show_output() is None


class TestView():

    @pytest.fixture
    def test_obj(self):
        root_path_mock = Path(r"..\src")
        self.exe_path_mock = mock.MagicMock()
        target = View("VERSION", root_path_mock, self.exe_path_mock)

        return target

    @pytest.mark.parametrize("isexist, ret", [
        (True, True),
        (True, False),
        (False, True),
    ])
    def test_on_start(self, test_obj, isexist, ret):
        control_mock = mock.MagicMock()
        control_mock.isexist_dbfile.return_value = isexist
        control_mock.start_up.return_value = ret
        with (
            mock.patch.object(test_obj, "_View__control", control_mock),
            mock.patch.object(test_obj, "_View__widget")
        ):
            assert test_obj.on_start() is None

    def test_on_stop(self, test_obj):
        with mock.patch.object(test_obj, "_View__control"):
            assert test_obj.on_stop() is None

    def test_build(self, test_obj):
        assert test_obj.build()
