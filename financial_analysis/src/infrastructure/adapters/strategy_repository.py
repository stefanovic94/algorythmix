from domain.entities import Strategy
from domain.errors import NotFoundError
from infrastructure.dtos import StrategyDto
from infrastructure.ports import StrategyRepositoryPort


class StrategyRepository(StrategyRepositoryPort):
    async def create(self, *args, **kwargs) -> Strategy:
        pass

    async def get(self, id: str) -> Strategy | None:
        dto = await StrategyDto.get(id)
        if dto is not None:
            return dto.to_domain()

    async def find(
        self, some: str | None = None, sort_by: str = "+name", limit: int | None = None
    ) -> list[Strategy]:
        query = {}

        if some is not None:
            query["some"] = "query"

        return [
            strategy.to_domain()
            for strategy in await StrategyDto.find(query)
            .sort(sort_by)
            .limit(limit)
            .to_list()
        ]

    async def update(self, strategy: Strategy) -> Strategy:
        pass

    async def delete(self, strategy: Strategy) -> None:
        dto = await self.get(str(strategy))

        if dto is None:
            raise NotFoundError(f"Strategy {str(strategy)} not found.")

        await dto.delete()
