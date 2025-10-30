import uvicorn
from fastapi import FastAPI

from app.api import router
from app.utils import logger

app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    logger.info("Запуск ASGI uvicorn и приложения")
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
    logger.info("Выключение приложения")
