from abc import ABC, abstractmethod
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from app.db.models import Respondent


class RespondentRepository(ABC):
    """Абстрактный репозиторий для работы с респондентами"""

    @abstractmethod
    async def get_respondents(self) -> list[Respondent]:
        """Возвращает список всех респондентов"""
        pass

    @abstractmethod
    async def get_average_weight_by_filter(self, filter_query) -> dict:
        """Возвращает средний вес респондентов по заданному фильтру"""
        pass


class SqlAlchemyRespondentRepository(RespondentRepository):
    """Реализация репозитория для работы с респондентами через SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        """
        :param session: Асинхронная сессия SQLAlchemy.
        """
        self.session = session

    async def get_respondents(self) -> list[Respondent]:
        """
        Список всех респондентов.

        :return: Список объектов Respondent.
        """
        stmt = select(Respondent)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_average_weight_by_filter(self, filter_query: str) -> dict:
        """
        Рассчитывает средний вес респондентов по заданному SQL-фильтру.

        :param filter_query: Строка SQL-фильтра.
        :return: Словарь {id_респондента: средний вес}.
        """
        stmt = (
            select(Respondent.respondent, func.avg(Respondent.weight).label("avg_weight"))
            .where(text(filter_query))
            .group_by(Respondent.respondent)
        )
        result = await self.session.execute(stmt)
        return dict(result.all())

    async def bulk_insert(self, respondents: list[dict]) -> None:
        """
        Выполняет массовую вставку данных о респондентах

        :param respondents: Список словарей с данными респондентов
        """
        await self.session.execute(Respondent.__table__.insert(), respondents)

