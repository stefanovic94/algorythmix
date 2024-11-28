from domain.entities import Strategy
from domain.enums import RiskTolerances
from domain.errors import NotFoundError
from infrastructure.dtos import StrategyDto
from infrastructure.ports import StrategyRepositoryPort


class StrategyRepository(StrategyRepositoryPort):
    async def create(self, obj: Strategy) -> Strategy:
        raise NotImplementedError()

    async def get(self, id: str) -> Strategy | None:
        dto = await StrategyDto.get(id)
        if dto is not None:
            return dto.to_domain()

    async def find(
        self,
        risk_tolerances: list[RiskTolerances] | None = None,
        sort_by: str = "+name",
        limit: int | None = None,
    ) -> list[Strategy]:
        query = {}

        if risk_tolerances:
            query["risk_tolerances"] = [x.value for x in risk_tolerances]

        return [
            strategy.to_domain()
            for strategy in await StrategyDto.find(query)
            .sort(sort_by)
            .limit(limit)
            .to_list()
        ]

    async def update(self, strategy: Strategy) -> Strategy:
        raise NotImplementedError()

    async def delete(self, strategy: Strategy) -> None:
        dto = await self.get(str(strategy))

        if dto is None:
            raise NotFoundError(f"Strategy {str(strategy)} not found.")

        await dto.delete()
