import pytest
from unittest import mock
from pathlib import Path
import os
from datetime import datetime
import pandas as pd
from src.component.output import OutputData


class TestOutputData():

    @pytest.fixture
    def test_obj(self):
        self.chn_name = "test_dataframe"
        self.save_path = "..\\test"
        self.mem_df = pd.DataFrame(data={
            "user_id": [
                "U04XLXCXUXX",
                "U04X7XPXJXX",
                "U04X5XBXMXX",
            ],
            "user_name": [
                "Hayashi Senjyuro",
                "Takahashi Korekiyo",
                "Saionji Kinmochi",
            ],
            "real_name": [
                "林銑十郎",
                "高橋是清",
                "西園寺公望",
            ]
        })
        self.model_mock = mock.MagicMock()
        target = OutputData(self.model_mock)

        yield target

        # df.to_csvで生成されたファイルを削除
        dt = datetime.today().strftime("%y%m%d")
        path = Path(self.save_path, f"{self.chn_name}_{dt}.csv")
        for test_path in (path, path.with_stem(path.stem + "(1)")):
            if test_path.exists():
                os.remove(test_path)

    def test_execute(self, test_obj):
        data_df = pd.DataFrame(data={
            "id": [
                "F153AAAA-9999-45AA-BCBC-11112222EEEE",
                "F153AAAA-9999-45AA-BBCC-11112222EEEE",
                "F153AAAA-9999-45AA-CCBB-11112222EEEE",
            ],
            "user_id": [
                "U04XLXCXUXX",
                "U04X7XPXJXX",
                "U04X5XBXMXX",
            ],
            "timestamp": [
                1675757575.000000,
                1675755555.000000,
                1675757777.000000,
            ],
            "text": [
                "Banker",
                "Barrister",
                "Beaver",
            ],
            "reaction": [0, 1, 2]
        })
        with (
            mock.patch.object(
                self.model_mock,
                "get_member",
                return_value=self.mem_df
            ),
            mock.patch.object(
                self.model_mock,
                "get_history",
                return_value=data_df
            ),
        ):
            assert test_obj.execute(
                self.save_path,
                "chn_id",
                self.chn_name
            ) is True
            assert test_obj.execute(
                self.save_path,
                "chn_id",
                self.chn_name
            ) is True

    def test_execute_anomaly(self, test_obj):
        data_df = pd.DataFrame(data={})
        with (
            mock.patch.object(
                self.model_mock,
                "get_member",
                return_value=self.mem_df
            ),
            mock.patch.object(
                self.model_mock,
                "get_history",
                return_value=data_df
            ),
        ):
            assert test_obj.execute(
                self.save_path,
                "chn_id",
                self.chn_name
            ) is False
