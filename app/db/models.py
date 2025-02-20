import datetime

from sqlalchemy import Integer, Date, Float, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Respondent(Base):
    """Модель респондента"""
    __tablename__ = "respondents"

    id: Mapped[int]             = mapped_column(Integer, primary_key=True,
                                                autoincrement=True)
    date: Mapped[datetime.date] = mapped_column(Date, index=True)
    respondent: Mapped[int]     = mapped_column(Integer)
    sex: Mapped[int]            = mapped_column(Integer, index=True)
    age: Mapped[int]            = mapped_column(Integer, index=True)
    weight: Mapped[float]       = mapped_column(Float)

    __table_args__ = (Index("idx_sex_age", "sex", "age"),)