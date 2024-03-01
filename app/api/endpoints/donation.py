from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_unallocated_charities
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationFull
from app.services.donation import invest_in_charity

router = APIRouter()


@router.post('/',
             response_model_exclude_none=True,
             response_model=DonationDB)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(donation, session, user)
    unallocated_charities = await check_unallocated_charities(session)
    if unallocated_charities:
        new_donation = await invest_in_charity(unallocated_charities, new_donation, session)
    return new_donation


@router.get('/',
            response_model=list[DonationFull],
            response_model_exclude_none=True,
            dependencies=[Depends(current_superuser)],)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзера."""
    donations = await donation_crud.get_multi(session)
    return donations


@router.get('/my',
            response_model=list[DonationDB],
            response_model_exclude={'user_id'},
            )
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Получает список всех пожертвований для текущего пользователя."""
    donations = await donation_crud.get_by_user(
        user_id=user.id, session=session)
    return donations
