from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
async def root() -> JSONResponse:
    """
    Simple endpoint to be used for health checks on the service.
    """
    return JSONResponse({"status": "ok"})
