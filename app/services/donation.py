from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def invest_in_charity(
        charities: list[CharityProject],
        donation: Donation,
        session: AsyncSession
):
    for charity in charities:
        current_donation = donation.full_amount - donation.invested_amount
        charity_capacity = charity.full_amount - charity.invested_amount
        if current_donation <= charity_capacity:
            charity.invested_amount += current_donation
            donation.invested_amount = donation.full_amount
            donation = get_closed(donation)
            if current_donation == charity_capacity:
                charity = get_closed(charity)
                session.add(donation)
            break
        if current_donation > charity_capacity:
            charity.invested_amount = charity.full_amount
            donation.invested_amount += charity_capacity
            charity = get_closed(charity)
            session.add(donation)
        session.add(donation)
        session.add(charity)
    await session.commit()
    await session.refresh(donation)
    return donation


def get_closed(entity):
    entity.fully_invested = True
    entity.close_date = datetime.now()
    return entity