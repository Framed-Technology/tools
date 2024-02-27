import pandas as pd
import yfinance as yf
import numpy as np
import random
from functools import lru_cache, reduce
import math
import operator


@lru_cache
def get_portfolio_history(
        ticker_codes: str, 
        period: str = "1y"
    ) -> pd.DataFrame:
    tickers = yf.Tickers(ticker_codes)
    try:
        history_df = tickers.history(period=period)
        close_history_df = history_df.Close
        return close_history_df
    except Exception as e:
        print(f"An error occured: {str(e)}")
        

def get_daily_returns(
    portfolio_history: pd.DataFrame
) -> pd.DataFrame:
    shifted_df = portfolio_history.shift(1)
    merged_df = portfolio_history.merge(shifted_df, on="Date", suffixes=("", "_T-1"))
    for ticker in shifted_df.columns:
        merged_df[f"{ticker}_DR"] = 100 * (merged_df[ticker] / merged_df[f"{ticker}_T-1"] - 1)
    dr_df = merged_df[[f'{ticker}_DR' for ticker in shifted_df.columns]]
    dr_df_cleaned = dr_df.dropna(axis = 0, how = 'all').fillna(0)
    return dr_df_cleaned


def get_rvol(daily_returns: pd.DataFrame, portfolio: dict[str, float]) -> float:
    observations = np.array([
        daily_returns[ticker + "_DR"] for ticker in portfolio.keys()
    ])
    covar_matrix = np.cov(observations)
    alloc_vector =  np.array([alloc for alloc in portfolio.values()])
    return math.sqrt(alloc_vector.dot(covar_matrix.dot(alloc_vector)))


def get_return(daily_returns: pd.DataFrame, portfolio: dict[str, float]) -> float:
    prod = lambda l: reduce(operator.mul, l)
    ret = 0
    observations = np.array([
        daily_returns[ticker + "_DR"] for ticker in portfolio.keys()
    ])
    for drs, alloc in zip(observations, portfolio.values()):
        roll_up = prod([1 + dr/100 for dr in drs])
        ret += roll_up * alloc
    return 100 * (ret - 1)


def portfolio_to_rvol_ret(portfolio: dict[str, float], period: str="1y"):
    ticker_codes = ",".join(portfolio.keys())
    ph_df = get_portfolio_history(ticker_codes, period=period)
    dr_df = get_daily_returns(ph_df)
    rvol = get_rvol(dr_df, portfolio)
    ret = get_return(dr_df, portfolio)
    return rvol, ret 