import os
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.respondent_repository import SqlAlchemyRespondentRepository

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "../../data/data.csv")


async def load_csv_to_db(session: AsyncSession):
    """Загружает CSV в базу данных, если она пустая."""
    repo = SqlAlchemyRespondentRepository(session)

    all_respondents = await repo.get_respondents()

    if all_respondents:
        return

    df = pd.read_csv(CSV_FILE, delimiter=";", dtype=str).drop(columns=["Unnamed: 0"], errors="ignore")
    df.columns = df.columns.str.strip().str.lower()

    df = df.assign(
        date=pd.to_datetime(df["date"], format="%Y%m%d"),
        respondent=pd.to_numeric(df["respondent"]).astype("Int64"),
        sex=pd.to_numeric(df["sex"]).astype("Int64"),
        age=pd.to_numeric(df["age"]).astype("Int64"),
        weight=pd.to_numeric(df["weight"]).astype(float)
    ).where(pd.notna(df), None)

    await repo.bulk_insert(df.to_dict(orient="records"))