import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from tortoise.contrib.fastapi import RegisterTortoise
from tortoise.exceptions import BaseORMException
from src.app.core.config import TORTOISE_ORM
from src.app.router import router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with RegisterTortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    ):
        yield


app = FastAPI(title="Fitech Finanças", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(BaseORMException)
async def orm_exception_handler(_: Request, exc: BaseORMException):
    return JSONResponse(status_code=400, content={"detail": str(exc), "status_code": 400})


@app.exception_handler(Exception)
async def generic_exception_handler(_: Request, exc: Exception):
    logger.exception("Unhandled error: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error", "status_code": 500})


app.include_router(router)
