from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio
import logging
import sys
from app.api import api_router
from app.services import upload_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s - %(asctime)s - %(name)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("app.log", mode="a", encoding="utf-8")
        ],
    )

    logger = logging.getLogger(__name__)
    logger.info("Starting File Processing API")

    # Start cleanup task
    cleanup_task = asyncio.create_task(cleanup_background_task(logger))

    yield

    # Shutdown
    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass

    logger.info("File Processing API shutdown complete")


async def cleanup_background_task(logger: logging.Logger):
    """Background task to periodically clean up old tasks."""
    while True:
        try:
            await asyncio.sleep(3600)  # 1 hour
            upload_service.cleanup_old_tasks(max_age_hours=24)
            logger.debug("Cleanup task executed successfully")
        except Exception as e:
            logger.error(f"Error in cleanup task: {str(e)}")


app = FastAPI(
    title="File Processing API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api/v1")
