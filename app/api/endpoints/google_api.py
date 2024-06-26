from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (set_user_permissions, spreadsheets_create,
                                     spreadsheets_update_value)
from app.schemas.google_api import GoogleAPIBase

router = APIRouter()


@router.post(
    '/',
    response_model=GoogleAPIBase,
    dependencies=[Depends(current_superuser)],
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    # Новый код
    """Только для суперюзеров."""
    charity_projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await spreadsheets_update_value(spreadsheet_id,
                                    charity_projects,
                                    wrapper_services)
    return {'message': (f'Был создан документ с ID {spreadsheet_id}'
            f' https://docs.google.com/spreadsheets/d/{spreadsheet_id}')}
