from app.repositories.respondent_repository import SqlAlchemyRespondentRepository


class RespondentService:
    """Сервис для работы с респондентами."""

    def __init__(self, repo: SqlAlchemyRespondentRepository):
        """
        :param repo: Репозиторий для работы с респондентами.
        """
        self.repo = repo

    async def calculate_percent(self, audience1_filter: str, audience2_filter: str) -> float:
        """Вычисляет процент вхождения второй аудитории в первую на основе среднего weight.

        :param audience1_filter: SQL-условие для фильтрации первой аудитории.
        :param audience2_filter: SQL-условие для фильтрации второй аудитории.
        :return: Процент вхождения второй аудитории в первую на основе среднего weight.
        """
        data1 = await self.repo.get_average_weight_by_filter(audience1_filter)
        data2 = await self.repo.get_average_weight_by_filter(audience2_filter)

        common_respondents = set(data1.keys()) & set(data2.keys())

        if not data1 or not data2 or not common_respondents:
            return 0.0

        weight_sum_1 = sum(data1.values())
        weight_sum_common = sum(data1[resp] for resp in common_respondents)

        return round(weight_sum_common / weight_sum_1, 2)
