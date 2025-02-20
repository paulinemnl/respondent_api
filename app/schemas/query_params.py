import re

from pydantic import BaseModel, field_validator, ConfigDict, Field
from pydantic_core import PydanticCustomError

from app.db.models import Respondent

ALLOWED_COLUMNS = {column.name for column in Respondent.__table__.columns}
ALLOWED_OPERATORS = {
    "=", "!=", "<", ">", "<=", ">=",
    "BETWEEN", "AND", "OR", "NOT", "IN"
}

TOKEN_PATTERN = r"[a-zA-Z_]+|[!=<>]+|;|--|#"


def validate_sql_condition(value: str) -> str:
    """
    Валидация SQL-фильтра: проверяет, содержатся ли в нем только допустимые колонки и операторы.

    :param value: Строка SQL-фильтра
    :return: Исходное значение, если оно безопасно
    :raises PydanticCustomError: Если в фильтре есть запрещенные токены
    """
    tokens = re.findall(TOKEN_PATTERN, value)

    unsafe_tokens = {
        token for token in tokens
        if token.lower() not in ALLOWED_COLUMNS and token.upper() not in ALLOWED_OPERATORS
    }

    if unsafe_tokens:
        raise PydanticCustomError(
            "unsafe_sql_query",
            'Unsafe tokens found in query',
            {
                "tokens": sorted(unsafe_tokens)
            },
        )

    return value


class SQLQueryParams(BaseModel):
    """Модель запроса с SQL-фильтрами"""
    model_config = ConfigDict(extra="forbid")

    audience1: str = Field(..., description="SQL-условие для первой аудитории")
    audience2: str = Field(..., description="SQL-условие для второй аудитории")

    @field_validator("audience1", "audience2", mode="before")
    def validate_audience(cls, value: str) -> str:
        """Валидация"""
        return validate_sql_condition(value)
