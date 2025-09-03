import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI

from src.api import router as main_router
from src.config import settings

app = FastAPI()
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        reload=settings.UVICORN_RELOAD,
    )
