from fastapi import APIRouter, status
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
async def root() -> JSONResponse:
    return JSONResponse({"status": "ok"})
