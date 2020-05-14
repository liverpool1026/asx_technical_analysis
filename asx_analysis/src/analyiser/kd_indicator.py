from asx_analysis.src.data_collector import StockData
from asx_analysis.src.analyiser import Analyser, AnalysisResult, VerdictSignal


class KDIndicatorAnalysisResult(AnalysisResult):
    def __init__(self, result: VerdictSignal, msg: str):
        self._result = result
        self._msg = msg

    def verdict(self) -> str:
        return f"{self._msg} -> {self._result.value}"

    def get_verdict_signal(self) -> VerdictSignal:
        return self._result


class KDIndicatorAnalyser(Analyser):
    @classmethod
    def populate(cls, data: "StockData") -> AnalysisResult:
        df = data.data.sort_values(["timestamp"])

        nine_day_max = [None] * 8
        nine_day_min = [None] * 8

        for i in range(len(df) - 8):
            nine_day_max.append(df.iloc[i: i+9].max().high)
            nine_day_min.append(df.iloc[i: i+9].min().low)

        df["nine_day_max"] = nine_day_max
        df["nine_day_min"] = nine_day_min

        df["rsv"] = 100 * (df["close"] - df["nine_day_min"]) / (df["nine_day_max"] - df["nine_day_min"])

        df = df[["rsv"]].dropna()

        k_values = []
        d_values = []

        for i in df.itertuples():
            if k_values:
                k_values.append(2 * k_values[-1] / 3 + i.rsv / 3)
            else:
                # Default as 50
                k_values.append(2 * 50 / 3 + i.rsv / 3)

            if d_values:
                d_values.append(2 * d_values[-1] / 3 + k_values[-1] / 3)
            else:
                # Default as 50
                d_values.append(2 * 50 / 3 + k_values[-1] / 3)

        df["k_value"] = k_values
        df["d_value"] = d_values

        if (df[-3:].k_value > 80).all():
            # 高檔鈍化
            return KDIndicatorAnalysisResult(result=VerdictSignal.STRONG_BUY, msg="K value over 80 for 3 days")
        elif (df[-3:].k_value < 20).all():
            # 低檔鈍化
            return KDIndicatorAnalysisResult(result=VerdictSignal.STRONG_SELL, msg="K value under 20 for 3 days")

        df["turn"] = df["k_value"] > df["d_value"]

        if df.iloc[-1].turn != df.iloc[-2].turn:
            if df.iloc[-1].turn:
                if df.iloc[-1].k_value < 20:
                    return KDIndicatorAnalysisResult(result=VerdictSignal.STRONG_BUY, msg="K over D and K < 20")
                else:
                    return KDIndicatorAnalysisResult(result=VerdictSignal.BUY, msg="K over D")
            else:
                if df.iloc[-1].k_value > 80:
                    return KDIndicatorAnalysisResult(result=VerdictSignal.STRONG_SELL, msg="D over K and K > 80")
                else:
                    return KDIndicatorAnalysisResult(result=VerdictSignal.SELL, msg="D over K")

        return KDIndicatorAnalysisResult(result=VerdictSignal.HOLD, msg=f"Not yet analysed, current K value: {df.iloc[-1].k_value} D value: {df.iloc[-1].d_value}")


__all__ = [
    "KDIndicatorAnalyser",
]








