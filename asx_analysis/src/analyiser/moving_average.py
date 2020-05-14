import pandas as pd

from asx_analysis.src.data_collector import StockData
from asx_analysis.src.analyiser import Analyser, AnalysisResult, VerdictSignal

from typing import Tuple


class MovingAverageAnalysisResult(AnalysisResult):
    def __init__(self, period: str, result: VerdictSignal):
        self._period = period
        self._result = result

    def verdict(self) -> str:
        return f"{self._period} days Moving Average is indicating a {self._result.value} signal"

    def get_verdict_signal(self) -> VerdictSignal:
        return self._result

class MovingAverageAnalyser(Analyser):
    @classmethod
    def get_period_type(cls) -> str:
        raise NotImplementedError

    @classmethod
    def get_periods(cls) -> Tuple[int, int]:
        raise NotImplementedError

    @classmethod
    def populate(cls, data: StockData) -> AnalysisResult:
        df = data.data.sort_values(["timestamp"])
        short_period, long_period = cls.get_periods()

        df["short_moving_average"] = df.rolling(window=short_period).mean().close
        df["long_moving_average"] = df.rolling(window=long_period).mean().close

        if pd.isna(df.iloc[-1].long_moving_average):
            return MovingAverageAnalysisResult(period=cls.get_period_type(), result=VerdictSignal.NO_DATA)

        if df.iloc[-1].close > df.iloc[-1].short_moving_average > df.iloc[-1].long_moving_average:
            return MovingAverageAnalysisResult(period=cls.get_period_type(), result=VerdictSignal.STRONG_BUY)

        if df.iloc[-1].close < df.iloc[-1].short_moving_average < df.iloc[-1].long_moving_average:
            return MovingAverageAnalysisResult(period=cls.get_period_type(), result=VerdictSignal.STRONG_SELL)

        if df.iloc[-1].short_moving_average < df.iloc[-1].close < df.iloc[-1].long_moving_average:
            return MovingAverageAnalysisResult(period=cls.get_period_type(), result=VerdictSignal.HOLD)

        else:
            return MovingAverageAnalysisResult(period=cls.get_period_type(), result=VerdictSignal.NO_DATA)


class ShortTermMovingAverageAnalyser(MovingAverageAnalyser):
    @classmethod
    def get_period_type(cls) -> str:
        return "Short"

    @classmethod
    def get_periods(cls) -> Tuple[int, int]:
        return 5, 10


class MidTermMovingAverageAnalyser(MovingAverageAnalyser):
    @classmethod
    def get_period_type(cls) -> str:
        return "Mid"

    @classmethod
    def get_periods(cls) -> Tuple[int, int]:
        return 20, 60


class LongTermMovingAverageAnalyser(MovingAverageAnalyser):
    @classmethod
    def get_period_type(cls) -> str:
        return "Long"

    @classmethod
    def get_periods(cls) -> Tuple[int, int]:
        return 120, 240


__all__ = [
    "ShortTermMovingAverageAnalyser",
    "MidTermMovingAverageAnalyser",
    "LongTermMovingAverageAnalyser",
]
