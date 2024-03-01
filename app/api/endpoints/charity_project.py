from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_closed,
                                check_charity_project_donated,
                                check_charity_project_donated_sum,
                                check_charity_project_exists,
                                check_charity_project_fully_invested,
                                check_name_duplicate,
                                check_unallocated_donations)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectFull,
                                         CharityProjectUpdate)
from app.services.charity_project import invest_donations

router = APIRouter()


@router.post('/',
             response_model=CharityProjectFull,
             response_model_exclude_none=True,
             dependencies=[Depends(current_superuser)],)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзера."""
    await check_name_duplicate(charity_project.name, session)
    new_charity = await charity_project_crud.create(charity_project, session)
    unallocated_donations = await check_unallocated_donations(session)
    if unallocated_donations:
        new_charity = await invest_donations(new_charity, unallocated_donations, session)
    return new_charity


@router.get('/',
            response_model=list[CharityProjectFull],
            response_model_exclude_none=True,)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    charities = await charity_project_crud.get_multi(session)
    return charities


@router.patch(
    '/{project_id}',
    response_model=CharityProjectFull,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    check_charity_project_fully_invested(charity_project.fully_invested)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if charity_project.invested_amount > 0:
        check_charity_project_donated_sum(
            charity_project.invested_amount, obj_in.full_amount)
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectFull,
    dependencies=[Depends(current_superuser)],)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    check_charity_project_closed(charity_project.fully_invested)
    check_charity_project_donated(charity_project.invested_amount)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project
