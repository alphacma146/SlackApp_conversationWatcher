# Standard lib
from pathlib import Path
from datetime import datetime
# Third party
import pandas as pd
# Saif made
from .abst_app import BaseAppFunction


class Output_Data(BaseAppFunction):

    def __init__(self, model) -> None:
        super().__init__()
        self.__model = model

    def execute(
        self,
        save_path: str,
        chn_id: str,
        chn_name: str,
        start: int = None,
        end: int = None
    ) -> bool:

        mem_df = self.__model.get_member(chn_id)
        data_df = self.__model.get_history(chn_id, start, end)

        # timestamp=>date
        data_df["date"] = (
            pd.to_datetime(
                data_df["timestamp"].astype(float) * 10**9,
                utc=True
            )
            .apply(lambda x: x.tz_convert("Asia/Tokyo"))
            .dt.strftime("%Y-%m-%d %H:%M:%S")
        )

        df = (
            pd.merge(data_df, mem_df, how="left", on="user_id")
            .sort_values(by="date", ascending=False)
        )

        dt = datetime.today().strftime("%y%m%d")
        path = self.recusion_search(Path(save_path, f"{chn_name}_{dt}.csv"))

        df.to_csv(
            path,
            index=False,
            columns=["id", "date", "real_name", "text", "reaction"]
        )

        return True

    def recusion_search(self, path: Path, count: int = 0) -> Path:

        if path.exists():
            stem = path.stem.rstrip(f"({count})")
            num = count + 1
            next_path = path.with_stem(stem + f"({num})")
            ret = self.recusion_search(next_path, num)
        else:
            ret = path

        return ret
