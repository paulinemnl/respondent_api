from pydantic import BaseModel

class PercentResponse(BaseModel):
    """Модель ответа с процентным значением"""
    percent: float
