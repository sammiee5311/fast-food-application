import os

import uvicorn
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from config.env import load_dotenv
from database import UUIDRedis

load_dotenv()

app = FastAPI()
uuid_redis = UUIDRedis()

HOST = os.environ["SERVER_HOST"]
PORT = os.environ["SERVER_PORT"]


class UUID(BaseModel):
    uuid: str


@app.get("/")
async def read_root():
    return {"message": "This server is an api for id generator."}


@app.get("/id")
async def read_uuid() -> JSONResponse:
    _uuid = UUID(uuid=uuid_redis.get_uuid())
    payload = jsonable_encoder(_uuid)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=payload)


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
