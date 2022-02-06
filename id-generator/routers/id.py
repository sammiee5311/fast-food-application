from database import UUIDRedis
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter(
    tags=["id"],
    responses={404: {"message": "Not found"}},
)

uuid_redis = UUIDRedis()


class UUID(BaseModel):
    uuid: str


@router.get("/id/", tags=["id"])
async def read_uuid() -> JSONResponse:
    _uuid = UUID(uuid=uuid_redis.get_uuid())
    payload = jsonable_encoder(_uuid)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=payload)
