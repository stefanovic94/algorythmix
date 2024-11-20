import asyncio
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from beanie import init_beanie
from fastapi import FastAPI, status, Depends
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi_pagination import add_pagination
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from application.controllers.graphql import graphql_app
from application.controllers.http import health_check
from configs.logger import get_logger
from configs.services import get_services
from configs.settings import get_settings

logger = get_logger(__name__)
services = get_services()
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    logger.info("starting %s...", settings.APP_NAME)

    loop = asyncio.get_event_loop()
    scheduler = AsyncIOScheduler()
    await FastAPILimiter.init(services.cache)

    await init_beanie(
        database=services.mongodb.FinancialAnalysis,
        document_models=[],
    )

    for task in []:
        logger.info("enqueueing task: %s", task.name)
        # executing the task and then adding to scheduler
        # to avoid getting a heartbeat alert if frequent
        # deployments are made in a short period
        loop.create_task(task.execute())
        scheduler.add_job(
            task.execute,
            "interval",
            seconds=15,  # trigger check every few seconds, each task will have its own interval
        )
    scheduler.start()

    # await services.event_broker.connect()
    # streams: list[str] = [x.value for x in []]
    # if streams:
    #     loop.create_task(
    #         services.event_broker.subscribe(
    #             event_handler=EventHandler(supported_events=[]),
    #             topics=streams,
    #             timeout=1.0,
    #         )
    #     )

    logger.info("%s ready", settings.APP_NAME)

    try:
        yield
    finally:
        logger.info("stopping %s...", settings.APP_NAME)
        scheduler.shutdown()
        services.mongodb.close()
        # await services.event_broker.close()
        await FastAPILimiter.close()
        await services.cache.aclose(close_connection_pool=True)
        logger.info("clean up completed")


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "If the user is not authenticated."
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "If the user does not have permission to the requested action."
        },
        status.HTTP_429_TOO_MANY_REQUESTS: {
            "description": "If the user has exceeded the rate limit."
        },
    },
)
app.include_router(
    graphql_app,
    prefix="/graphql",
    include_in_schema=False if settings.ENVIRONMENT == "production" else True,
)
app.include_router(
    health_check.router, dependencies=[Depends(RateLimiter(times=100, seconds=60))]
)
add_pagination(app)


def main() -> None:
    uvicorn.run("main:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    main()
