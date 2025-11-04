import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router
from app.utils import logger

app = FastAPI()
app.include_router(router)


origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    logger.info("Запуск ASGI uvicorn и приложения")
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
    logger.info("Выключение приложения")
