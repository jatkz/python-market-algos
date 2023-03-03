"""
Library of functions for the project
    Returns:
        _type_: _description_
"""
import pandas as pd


def bar_metrics(dataframe: pd.DataFrame) -> pd.DataFrame:
    """_summary_

    Args:
        dateframe (_type_): _description_

    Returns:
        _type_: _description_
    """
    barratios = bar_ratios(
        dataframe
    )  # middle ratio, top whisker ratio, bottom whisker ratio, open to top ratio, open to bottom ratio, open to close ratio
    # they are ratios of the entire bar size. (high to low)
    barpercents = bar_percentages(
        dataframe
    )  # open to close, open to high, open to low % change

    zstats = z_score(dataframe)  # rolling zscore everything

    return dataframe


# def bar_metrics(dateframe: pd.DataFrame) -> pd.DataFrame:
#     """_summary_

#     Args:
#         dateframe (_type_): _description_

#     Returns:
#         _type_: _description_
#     """
#     dateframe["rsi"] = rsi(close=dateframe["close"], window=14, fillna=True)
#     dateframe["macd"] = macd(
#         close=dateframe["close"], fast=12, slow=26, signal=9, fillna=True
#     )
#     dateframe["cci"] = cci(
#         high=dateframe["high"],
#         low=dateframe["low"],
#         close=dateframe["close"],
#         window=20,
#         constant=0.015,
#         fillna=True,
#     )
#     dateframe["sma"] = sma(close=dateframe["close"], window=20, fillna=True)
#     dateframe["ema"] = ema(close=dateframe["close"], window=20, fillna=True)
#     dateframe["wma"] = wma(close=dateframe["close"], window=20, fillna=True)
#     dateframe["dema"] = dema(close=dateframe["close"], window=20, fillna=True)
#     dateframe["tema"] = tema(close=dateframe["close"], window=20, fillna=True)
#     dateframe["trima"] = trima(close=dateframe["close"], window=20, fillna=True)
#     dateframe["kama"] = kama(close=dateframe["close"], window=20, fillna=True)
#     dateframe["mama"] = mama(close=dateframe["close"], fast_limit=0.5, slow_limit=0.05)
#     dateframe["t3"] = t3(close=dateframe["close"], window=20, fillna=True)
#     dateframe["vwap"] = vwap(
#         high=dateframe["high"],
#         low=dateframe["low"],
#         close=dateframe["close"],
#         volume=dateframe["volume"],
#         fillna=True,
#     )
#     dateframe["vwap"] = vwap(
#         high=dateframe["high"],
#         low=dateframe["low"],
#         close=dateframe["close"],
#         volume=dateframe["volume"],
#         fillna=True,
#     )
#     dateframe["vwap"] = vwap(
#         high=dateframe["high"],
#         low=dateframe["low"],
#         close=dateframe["close"],
#         volume=dateframe["volume"],
#         fillna=True,
#     )
#     date
