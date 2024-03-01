from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import extract

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDСharityProject(CRUDBase):
    async def get_charity_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_charity_project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ):
        db_obj = await session.execute(
            select(
                CharityProject.name,
                (extract('epoch', CharityProject.close_date) -
                 extract('epoch', CharityProject.create_date)
                 ).label('close_period'),
                CharityProject.description
            ).where(CharityProject.fully_invested == 1)
            .order_by('close_period')
        )
        return db_obj.all()


charity_project_crud = CRUDСharityProject(CharityProject)
