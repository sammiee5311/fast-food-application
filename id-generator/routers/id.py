from database import UUIDRedis
from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from redis.exceptions import ConnectionError
from utils.log import logger

router = APIRouter(
    tags=["id"],
    responses={404: {"message": "Not found"}},
)

uuid_redis = UUIDRedis()


class UUID(BaseModel):
    uuid: str


@router.get("/id/", tags=["id"])
async def read_uuid() -> JSONResponse:
    try:
        _uuid = UUID(uuid=uuid_redis.get_uuid())
        payload = jsonable_encoder(_uuid)

        return JSONResponse(status_code=status.HTTP_200_OK, content=payload)
    except ConnectionError:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": f"Redis connection error."})


@router.get("/id-generator/", tags=["id"])
async def generate_uuid() -> JSONResponse:
    message = "UUID generated in redis: %s"

    try:
        uuid_redis.generate_ids()
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": message % "success"})
    except:
        logger.warn("Fail to generate uuids.")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": message % "fail"})
