from domain.entities import Strategy
from infrastructure.adapters import StrategyRepository

strategy_repository = StrategyRepository()


async def get_strategy_query(id: str) -> Strategy | None:
    """
    Get a strategy.

    Parameters
    ----------
    id : str
        ID of the strategy to get.

    Returns
    -------
    strategy : Strategy | None
        The found strategy or None if not found.
    """
    return await strategy_repository.get(id=id)
