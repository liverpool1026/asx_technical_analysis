import enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from asx_analysis.src.data_collector import StockData


class VerdictSignal(enum.Enum):
    STRONG_BUY: str = "Strong Buy"
    BUY: str = "Buy"
    HOLD: str = "Hold"
    SELL: str = "Sell"
    STRONG_SELL: str = "Strong Sell"
    NO_DATA: str = "N / A"


class AnalysisResult(object):
    def verdict(self) -> str:
        raise NotImplementedError

    def get_verdict_signal(self) -> VerdictSignal:
        raise NotImplementedError


class Analyser(object):
    @classmethod
    def populate(cls, data: "StockData") -> AnalysisResult:
        raise NotImplementedError


__all__ = [
    "VerdictSignal",
    "Analyser",
    "AnalysisResult",
]