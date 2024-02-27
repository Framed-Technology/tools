import enum
from typing import Annotated, List
from fastapi import APIRouter, Query
from pydantic import BaseModel, validator

from src.tools.risk_calculator import portfolio_to_rvol_ret


tool_router = APIRouter(prefix="/tool", tags=["Tools"])


class AssetAllocation(BaseModel):
    ticker: str
    allocation: float

    @validator('allocation')
    def allocation_must_be_between_zero_and_one(cls, v):
        if not (0 <=v <= 1):
            raise ValueError('allocation must be between 0 and 1')
        return v

class Portfolio(BaseModel):
    asset_allocations: List[AssetAllocation]

    @validator('asset_allocations', each_item=False)
    def allocations_must_sum_to_one(cls, v):
        total_allocation = sum(stock.allocation for stock in v)
        tolerance = 1e-5 
        if not (1 - tolerance <= total_allocation <= 1 + tolerance):
            raise ValueError(f'The sum of allocations must be 1 within a tolerance of {tolerance}, but is {total_allocation}')
        return v
    
class RiskReturn(BaseModel):
    rvol: float
    ret: float

class Period(enum.Enum):
    ONE_MONTH = "1mo"
    SIX_MONTHS = "6mo"
    ONE_YEAR = "1y"
    TWO_YEARS = "2y"
    THREE_YEARS = "3y"


@tool_router.post("/risk", response_model=RiskReturn)
def health(
    portfolio: Portfolio,
    period: Annotated[Period, Query()] = Period.ONE_YEAR,
):
    portfolio_dict = {asset.ticker: asset.allocation for asset in  portfolio.asset_allocations}
    rvol, ret = portfolio_to_rvol_ret(portfolio=portfolio_dict, period=period.value)
    return RiskReturn(rvol=rvol, ret=ret, period=period.value)