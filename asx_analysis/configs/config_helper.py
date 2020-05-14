from asx_analysis.configs.base import Config
from asx_analysis.configs.config import AnalysisConfig


def read_config() -> Config:
    return Config(api_key=AnalysisConfig.get_api_key())


__all__ = [
    "read_config",
]
