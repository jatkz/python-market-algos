"""Test the api module."""
import api
import pandas as pd

def test_get_candle():
    """Test the get_candle function."""
    collection = "Short"
    symbol = "TSLA"
    candles = api.query_candle(collection, symbol)
    print("Type ", type(candles))
    assert type(candles) == pd.DataFrame
