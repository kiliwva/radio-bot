from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import Order, OrderStatus, User


def top_users_by_stars(session: Session, limit: int = 10) -> list[dict]:
    stmt = (
        select(
            User.tg_id,
            func.sum(Order.amount_rub).label("total_amount"),
            func.count(Order.id).label("transactions"),
        )
        .join(Order, User.id == Order.user_id)
        .where(Order.product_slug == "tg_stars", Order.status == OrderStatus.paid)
        .group_by(User.tg_id)
        .order_by(func.sum(Order.amount_rub).desc())
        .limit(limit)
    )
    rows = session.execute(stmt).all()
    return [
        {"tg_id": row.tg_id, "total_amount": int(row.total_amount or 0), "transactions": int(row.transactions)}
        for row in rows
    ]


def calculate_profit(revenue: float, commission_percent: float, cost: float) -> float:
    commission = revenue * (commission_percent / 100)
    return round(revenue - commission - cost, 2)
