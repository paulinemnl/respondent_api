from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.repositories.respondent_repository import SqlAlchemyRespondentRepository
from app.schemas.query_params import SQLQueryParams
from app.schemas.responses import PercentResponse
from app.services.respondent_service import RespondentService

respondent_router = APIRouter()


def get_respondent_service(
        session: AsyncSession = Depends(get_async_session)
) -> RespondentService:
    """
    Возвращает сервис для работы с респондентами

    :param session: Асинхронная сессия базы данных
    :return: Экземпляр RespondentService.
    """
    return RespondentService(SqlAlchemyRespondentRepository(session))


@respondent_router.get("/getPercent", response_model=PercentResponse)
async def get_percent(
        filter_query: Annotated[SQLQueryParams, Query()],
        respondent_service: RespondentService = Depends(get_respondent_service)
) -> PercentResponse:
    """
    Вычисляет процент вхождения второй аудитории в первую, основываясь на среднем весе
    \f
    :param filter_query: Параметры запроса, содержащие аудитории 1 и 2
    :param respondent_service: Сервис для работы с респондентами
    :return: Объект PercentResponse с рассчитанным процентом
    """
    percent = await respondent_service.calculate_percent(
        filter_query.audience1,
        filter_query.audience2
    )
    return PercentResponse(percent=percent)




