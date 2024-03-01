from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example='Название проекта')
    description: str = Field(..., min_length=1, example='Описание проекта')
    full_amount: PositiveInt = Field(..., example=100)

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):

    @validator('name')
    def name_valid(cls, value: str):
        if len(value) > 100 or value is None:
            raise ValueError('Создание проектов с пустым названием '
                             'или с названием длиннее 100 символов запрещено.')
        return value


class CharityProjectUpdate(CharityProjectCreate):
    name: str = Field(None, min_length=1, max_length=100, example='Название проекта')
    description: str = Field(None, min_length=1, example='Описание проекта')
    full_amount: PositiveInt = Field(None, example=100)


class CharityProjectFull(CharityProjectBase):
    id: int
    create_date: datetime
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True