import uvicorn
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from generator import generate_id

app = FastAPI()

HOST = "0.0.0.0"
PORT = 8008
UUID_HEX = str


class UUID(BaseModel):
    uuid: UUID_HEX


@app.get("/")
def read_root():
    return {"message": "This server is an api for id generator."}


@app.get("/id")
async def read_id() -> JSONResponse:
    _uuid = UUID(uuid=generate_id())
    payload = jsonable_encoder(_uuid)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=payload)


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
