from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import User


def add_stars(session: Session, tg_id: int, amount: int) -> int:
    user = session.scalar(select(User).where(User.tg_id == tg_id))
    if user is None:
        user = User(tg_id=tg_id, stars_balance=0)
        session.add(user)
    user.stars_balance += amount
    session.commit()
    return user.stars_balance


def create_stars_check(session: Session, tg_id: int, amount: int) -> str:
    user = session.scalar(select(User).where(User.tg_id == tg_id))
    if user is None or user.stars_balance < amount:
        raise ValueError("Недостаточно Stars на балансе")
    user.stars_balance -= amount
    session.commit()
    return f"STAR-CHECK-{tg_id}-{amount}"
