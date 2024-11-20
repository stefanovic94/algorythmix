from domain.entities import Strategy
from domain.enums import RiskTolerances
from infrastructure.adapters import StrategyRepository

strategy_repository = StrategyRepository()


async def find_strategies_query(
    risk_tolerances: list[RiskTolerances] | None = None,
    sort_by: str = "+name",
    limit: int | None = None,
) -> list[Strategy]:
    """
    Finds strategies.

    Parameters
    ----------
    risk_tolerances : list[RiskTolerances] | None
        Filters by a list of risk tolerances. Defaults to None.
    sort_by : str
        Sorting the strategies by a field. Defaults to sorting by the `name` field in alphabetical order.
    limit : int | None
        Limits the number of strategies returned. Defaults to no limit.

    Returns
    -------
    list[Strategy]
        The found strategies.
    """

    return await strategy_repository.find(
        risk_tolerances=risk_tolerances, sort_by=sort_by, limit=limit
    )
