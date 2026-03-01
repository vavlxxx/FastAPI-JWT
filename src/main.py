import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

sys.path.append(str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI

from src.api import router as main_router
from src.config import settings
from src.db import engine, sessionmaker
from src.schemas.rules import RuleAddDTO
from src.services.rules import RuleService
from src.utils.db_tools import DBHealthChecker, DBManager
from src.utils.logging import (
    configurate_logging,
    get_logger,
)


@asynccontextmanager
async def lifespan(
    app: FastAPI,
) -> AsyncGenerator[None, None]:
    logger = get_logger("src")

    await DBHealthChecker(engine=engine).check()

    async with DBManager(
        session_factory=sessionmaker
    ) as db:
        try:
            await RuleService(db=db).add_rules(
                rules=[
                    RuleAddDTO(
                        code="test",
                        title="test",
                        description="test",
                        error_message="test",
                    ),
                ]
            )
        except Exception:
            logger.error(
                "Health check failed. Shutting down...",
                exc_info=True,
            )

    logger.info("All checks passed!")
    yield
    logger.info("Shutting down...")


configurate_logging()
app = FastAPI(
    lifespan=lifespan,
    title=settings.app.title,
)
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.uvicorn.host,
        port=settings.uvicorn.port,
        reload=settings.uvicorn.reload,
    )
