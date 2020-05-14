import pandas as pd

from asx_analysis.src.data_collector import StockData
from asx_analysis.src.analyiser import Analyser, AnalysisResult, VerdictSignal

from typing import List


class RSIIndicatorAnalysisResult(AnalysisResult):
    def __init__(self, result: VerdictSignal, msg: str):
        self._result = result
        self._msg = msg

    def verdict(self) -> str:
        return f"{self._msg} -> {self._result.value}"


class RSIIndicatorAnalyser(Analyser):
    @classmethod
    def populate_rsi_values(cls, df: pd.DataFrame, days: int) -> List[float]:
        data = [None] * (days - 1)

        for i in range(len(df) - days + 1):
            up_value = df.iloc[i: i + days]["change"].apply(lambda x: x if x > 0 else 0).sum()
            down_value = df.iloc[i: i + days]["change"].apply(lambda x: -x if x < 0 else 0).sum()
            
            data.append((100 * up_value) / (up_value + down_value))

        return data

    @classmethod
    def populate(cls, data: "StockData") -> AnalysisResult:
        df = data.data.sort_values(["timestamp"])
        df["previous_close"] = df.close.shift(1)
        df["change"] = df["close"] - df["previous_close"]

        df = df.dropna()

        df["5_day_rsi"] = cls.populate_rsi_values(df, 5)
        df["10_day_rsi"] = cls.populate_rsi_values(df, 10)

        df["turn"] = df["5_day_rsi"] > df["10_day_rsi"]

        if df.iloc[-1].turn != df.iloc[-2].turn:
            if df.iloc[-1].turn:
                if df.iloc[-1]["5_day_rsi"] > 80 and df.iloc[-1]["10_day_rsi"] > 80:
                    return RSIIndicatorAnalysisResult(VerdictSignal.SELL, "Both RSI is over 80 when 5 day RSI overtakes 10 day RSI")
                elif df.iloc[-1]["5_day_rsi"] > 80 or df.iloc[-1]["10_day_rsi"] > 80:
                    if df.iloc[-1]["5_day_rsi"] > 80:
                        return RSIIndicatorAnalysisResult(VerdictSignal.HOLD,
                                                          f"5 day RSI value is over 80 at {df.iloc[-1]['5_day_rsi']} while 10 day RSI value is at {df.iloc[-1]['10_day_rsi']} when 5 day RSI overtakes 10 day RSI")
                    else:
                        return RSIIndicatorAnalysisResult(VerdictSignal.HOLD,
                                                          f"10 day RSI value is over 80 at {df.iloc[-1]['10_day_rsi']} while 5 day RSI value is at {df.iloc[-1]['5_day_rsi']} when 5 day RSI overtakes 10 day RSI")
                elif df.iloc[-1]["5_day_rsi"] < 20 and df.iloc[-1]["10_day_rsi"] < 20:
                    return RSIIndicatorAnalysisResult(VerdictSignal.STRONG_BUY, "Both RSI is under 20 when 5 day RSI overtakes 10 day RSI")
                elif df.iloc[-1]["5_day_rsi"] < 20 or df.iloc[-1]["10_day_rsi"] < 20:
                    if df.iloc[-1]["5_day_rsi"] < 20:
                        return RSIIndicatorAnalysisResult(VerdictSignal.STRONG_BUY,
                                                          f"5 day RSI value is under 20 at {df.iloc[-1]['5_day_rsi']} while 10 day RSI value is at {df.iloc[-1]['10_day_rsi']} when 5 day RSI overtakes 10 day RSI")
                    else:
                        return RSIIndicatorAnalysisResult(VerdictSignal.STRONG_BUY,
                                                          f"10 day RSI value is under 20 at {df.iloc[-1]['10_day_rsi']} while 5 day RSI value is at {df.iloc[-1]['5_day_rsi']} when 5 day RSI overtakes 10 day RSI")
                else:
                    return RSIIndicatorAnalysisResult(VerdictSignal.BUY,
                                                      f"10 day RSI value is at {df.iloc[-1]['10_day_rsi']} while 5 day RSI value is at {df.iloc[-1]['5_day_rsi']} when 5 day RSI overtakes 10 day RSI")
            else:
                if df.iloc[-1]["5_day_rsi"] > 80 and df.iloc[-1]["10_day_rsi"] > 80:
                    return RSIIndicatorAnalysisResult(VerdictSignal.STRONG_SELL, "Both RSI is over 80 when 10 day RSI overtakes 5 day RSI")
                elif df.iloc[-1]["5_day_rsi"] > 80 or df.iloc[-1]["10_day_rsi"] > 80:
                    if df.iloc[-1]["5_day_rsi"] > 80:
                        return RSIIndicatorAnalysisResult(VerdictSignal.STRONG_SELL,
                                                          f"5 day RSI value is over 80 at {df.iloc[-1]['5_day_rsi']} while 10 day RSI value is at {df.iloc[-1]['10_day_rsi']} when 10 day RSI overtakes 5 day RSI")
                    else:
                        return RSIIndicatorAnalysisResult(VerdictSignal.STRONG_SELL,
                                                          f"10 day RSI value is over 80 at {df.iloc[-1]['10_day_rsi']} while 5 day RSI value is at {df.iloc[-1]['5_day_rsi']} when 10 day RSI overtakes 5 day RSI")
                elif df.iloc[-1]["5_day_rsi"] < 20 and df.iloc[-1]["10_day_rsi"] < 20:
                    return RSIIndicatorAnalysisResult(VerdictSignal.BUY, "Both RSI is under 20 when 10 day RSI overtakes 5 day RSI")
                elif df.iloc[-1]["5_day_rsi"] < 20 or df.iloc[-1]["10_day_rsi"] < 20:
                    if df.iloc[-1]["5_day_rsi"] < 20:
                        return RSIIndicatorAnalysisResult(VerdictSignal.HOLD,
                                                          f"5 day RSI value is under 20 at {df.iloc[-1]['5_day_rsi']} while 10 day RSI value is at {df.iloc[-1]['10_day_rsi']} when 10 day RSI overtakes 5 day RSI")
                    else:
                        return RSIIndicatorAnalysisResult(VerdictSignal.HOLD,
                                                          f"10 day RSI value is under 20 at {df.iloc[-1]['10_day_rsi']} while 5 day RSI value is at {df.iloc[-1]['5_day_rsi']} when 10 day RSI overtakes 5 day RSI")
                else:
                    return RSIIndicatorAnalysisResult(VerdictSignal.SELL,
                                                      f"10 day RSI value is at {df.iloc[-1]['10_day_rsi']} while 5 day RSI value is at {df.iloc[-1]['5_day_rsi']} when 10 day RSI overtakes 5 day RSI")

        if df.iloc[-1]["5_day_rsi"] > 80 and df.iloc[-1]["10_day_rsi"] > 80:
            return RSIIndicatorAnalysisResult(VerdictSignal.STRONG_SELL, "Both RSI is over 80")
        elif df.iloc[-1]["5_day_rsi"] > 80 or df.iloc[-1]["10_day_rsi"] > 80:
            if df.iloc[-1]["5_day_rsi"] > 80:
                return RSIIndicatorAnalysisResult(VerdictSignal.SELL, f"5 day RSI value is over 80 at {df.iloc[-1]['5_day_rsi']} while 10 day RSI value is at {df.iloc[-1]['10_day_rsi']}")
            else:
                return RSIIndicatorAnalysisResult(VerdictSignal.SELL, f"10 day RSI value is over 80 at {df.iloc[-1]['10_day_rsi']} while 5 day RSI value is at {df.iloc[-1]['5_day_rsi']}")
        elif df.iloc[-1]["5_day_rsi"] < 20 and df.iloc[-1]["10_day_rsi"] < 20:
            return RSIIndicatorAnalysisResult(VerdictSignal.STRONG_BUY, "Both RSI is under 20")
        elif df.iloc[-1]["5_day_rsi"] < 20 or df.iloc[-1]["10_day_rsi"] < 20:
            if df.iloc[-1]["5_day_rsi"] < 20:
                return RSIIndicatorAnalysisResult(VerdictSignal.BUY, f"5 day RSI value is under 20 at {df.iloc[-1]['5_day_rsi']} while 10 day RSI value is at {df.iloc[-1]['10_day_rsi']}")
            else:
                return RSIIndicatorAnalysisResult(VerdictSignal.BUY, f"10 day RSI value is under 20 at {df.iloc[-1]['10_day_rsi']} while 5 day RSI value is at {df.iloc[-1]['5_day_rsi']}")

        return RSIIndicatorAnalysisResult(VerdictSignal.HOLD, f"10 day RSI value is at {df.iloc[-1]['10_day_rsi']} while 5 day RSI value is at {df.iloc[-1]['5_day_rsi']}")


__all__ = [
    "RSIIndicatorAnalyser",
]








