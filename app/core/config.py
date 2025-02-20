from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Конфигурация приложения, загружаемая из переменных окружения"""
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Возвращает URL для подключения к базе данных в асинхронном режиме"""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()

