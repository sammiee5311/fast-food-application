import os

import uvicorn
from config.env import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from routers.id import router as id_router

load_dotenv()

OTLP_ENDPOINT = os.environ.get("OTLP_ENDPOINT")
HOST = os.environ["SERVER_HOST"]
PORT = int(os.environ["SERVER_PORT"])
ORIGINS = ["django-backend:8000"]

app = FastAPI()

if OTLP_ENDPOINT:
    FastAPIInstrumentor().instrument_app(app)

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
