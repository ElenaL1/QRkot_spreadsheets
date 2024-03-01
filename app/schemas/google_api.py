from pydantic import BaseModel, Field


class GoogleAPIBase(BaseModel):
    message: str = Field(None, example='Был создан документ с ID '
                         ' https://docs.google.com/spreadsheets/d/ID')
