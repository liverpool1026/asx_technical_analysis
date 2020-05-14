from asx_analysis.configs.base import Configuration


class AnalysisConfig(Configuration):
    @classmethod
    def get_api_key(cls) -> str:
        return "EUV0VCWNQHZ2M7PJ"
