from abc import ABC, abstractmethod

from domain.entities import Strategy
from domain.enums import RiskTolerances


class StrategyRepositoryPort(ABC):
    """
    Represents an interface for interacting with the Strategy aggregate.

    None of the methods exposed by this class checks for object permissions. It is
    anticipated that the client calling these methods ensures correct object permissions.
    """

    @abstractmethod
    async def create(self, obj: Strategy) -> Strategy:
        """
        Create a strategy in the database.

        It is assumed that the `CreateStrategyCommand` makes pre-creation validation like
        checking for duplicate strategies, etc.

        This method will write the strategy object to the database and only verify the uniqueness
        of the ID.

        Parameters
        ----------
        obj : Strategy
            The created strategy object from the `CreateStrategyCommand` command.

        Returns
        -------
        Strategy
            The created strategy object.

        Raises
        ------
        AlreadyExistsError
            If a strategy with the same ID already exists.
        """
        pass

    @abstractmethod
    async def get(self, id: str) -> Strategy | None:
        """
        Get a strategy from the database. If a strategy with
        the specified ID is not found, it will return None.

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
        self,
        risk_tolerances: list[RiskTolerances] | None = None,
        sort_by: str = "+name",
        limit: int | None = None,
    ) -> list[Strategy]:
        """
        Find strategies in the database with optional filtering and sorting.

        Parameters
        ----------
        risk_tolerances : list[RiskTolerances] | None
            A list of risk tolerances to filter by. Defaults to None. Supporting a list
            of risk tolerances for better filtering flexibility.
        sort_by : str = +name
            How to sort the results. Defaults to sort the strategies in alphabetical order.

            + means ascending order, - means descending order.
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
        """
        Updates an existing strategy in the database, and raises an error if the
        strategy is not found.

        Parameters
        ----------
        strategy : Strategy
            The strategy to update.

        Returns
        -------
        Strategy
            The updated strategy object.

        Raises
        ------
        NotFoundError
            If the strategy is not found.
        """
        pass

    @abstractmethod
    async def delete(self, strategy: Strategy) -> None:
        """
        Deletes a strategy from the database, and raises an error if the strategy
        is not found.

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
