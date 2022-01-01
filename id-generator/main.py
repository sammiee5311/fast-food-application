from pydantic import BaseModel
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from generator import generate_id

app = FastAPI()


class Id(BaseModel):
    id: str


@app.get("/")
def read_root():
    return {"message": "This server is an api for id generator."}


@app.get("/id")
async def read_id() -> JSONResponse:
    id = Id(id=generate_id())
    payload = jsonable_encoder(id)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=payload)
