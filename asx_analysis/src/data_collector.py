import io
import attr
import requests

import pandas as pd

from asx_analysis.configs.config_helper import read_config


def get_api_key() -> str:
    return read_config().api_key


def construct_code(code: str) -> str:
    return "{}.AX".format(code)


def construct_api_url(
        code: str,
        *,
        function: str = "TIME_SERIES_DAILY",
        output_size: str = "full",
) -> str:
    return "https://www.alphavantage.co/query?function={}&symbol={}&outputsize={}&datatype=csv&apikey={}".format(
        function, construct_code(code), output_size, get_api_key()
    )


@attr.attrs
class StockData(object):
    code = attr.attrib(validator=attr.validators.instance_of(str), kw_only=True)
    data = attr.attrib(validator=attr.validators.instance_of(pd.DataFrame), kw_only=True)


def grab_stock_data(code: str) -> StockData:
    response = requests.get(construct_api_url(code=code))
    df = pd.read_csv(io.StringIO(response.content.decode()))

    return StockData(
        code=code,
        data=df,
    )



