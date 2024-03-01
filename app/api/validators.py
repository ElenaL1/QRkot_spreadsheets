from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation


async def check_name_duplicate(
        name: str,
        session: AsyncSession,
) -> None:
    charity_project_id = await charity_project_crud.get_charity_project_id_by_name(
        name, session)
    if charity_project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


def check_charity_project_closed(fully_invested: bool) -> None:
    if fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


def check_charity_project_fully_invested(fully_invested: bool) -> None:
    if fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


def check_charity_project_donated(invested_amount: int,) -> None:
    if invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


def check_charity_project_donated_sum(
        invested_amount: int,
        full_amount: int,) -> None:
    if invested_amount > full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'В проект уже сделаны пожертвования на сумму {invested_amount} ,'
            ' ее нельзя уменьшать!'
        )


async def check_unallocated_donations(
        session: AsyncSession,
) -> list[Donation]:
    donations = await donation_crud.get_unallocated_fund(session)
    return donations


async def check_unallocated_charities(
        session: AsyncSession,
) -> list[CharityProject]:
    charity_projects = await charity_project_crud.get_unallocated_fund(session)
    return charity_projects
