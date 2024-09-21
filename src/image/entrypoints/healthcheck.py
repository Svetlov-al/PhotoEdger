import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/")
async def healthcheck() -> JSONResponse:
    logger.info("healthcheck")
    return JSONResponse({"success": True})
