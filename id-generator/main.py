import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.env import load_dotenv
from routers.id import router as id_router

load_dotenv()

HOST = os.environ["SERVER_HOST"]
PORT = int(os.environ["SERVER_PORT"])
ORIGINS = ["django-backend:8000"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(id_router)


@app.get("/")
async def read_root():
    return {"message": "This server is an api for id generator."}


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
