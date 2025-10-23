import datetime
from typing import Dict, Optional

import jwt

from app.core import settings


class ClientJWT:
    def __init__(self, data: Optional[Dict[str, str]]):
        self.data = data

    def create_token(self):
        payload: Dict = {}
        payload.update(self.data)
        payload["exp"] = datetime.datetime.now() + datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        return jwt.encode(
            payload=payload, key=settings.SECRET, algorithm=settings.ALGORYTHM
        )


