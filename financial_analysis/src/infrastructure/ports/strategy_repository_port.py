from abc import ABC, abstractmethod

from domain.entities import Strategy


class StrategyRepositoryPort(ABC):
    """Represents an interface for interacting with the Strategy aggregate."""

    @abstractmethod
    async def create(self, *args, **kwargs) -> Strategy:
        pass

    @abstractmethod
    async def get(self, id: str) -> Strategy | None:
        """
        Get a strategy from the database.

        Parameters
        ----------
        id : str
            The ID of the strategy to find.

        Returns
        -------
        Strategy | None
            The found strategy object or None if not found.
        """
        pass

    @abstractmethod
    async def find(
        self, sort_by: str = "+name", limit: int | None = None
    ) -> list[Strategy]:
        """
        Find strategies in the database.

        Parameters
        ----------
        sort_by : str = +name
            How to sort the results. Defaults to sort the strategies in alphabetical order.
        limit: int | None
            Limit the number of results. Defaults to no limitation.

        Returns
        -------
        list[Strategy]
            The found strategies.
        """
        pass

    @abstractmethod
    async def update(self, strategy: Strategy) -> Strategy:
        pass

    @abstractmethod
    async def delete(self, strategy: Strategy) -> None:
        """
        Deletes a strategy from the database.

        Parameters
        ----------
        strategy : Strategy
            The strategy to delete.

        Returns
        -------
        None

        Raises
        ------
        NotFoundError
            If the strategy is not found.
        """
        pass
