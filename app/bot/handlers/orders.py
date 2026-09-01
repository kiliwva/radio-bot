from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy import select

from app.database import Order, OrderStatus, SessionLocal, User
from app.services.payments import mock_invoice_link

router = Router()


@router.callback_query(lambda c: c.data and c.data.startswith("buy:"))
async def create_order(callback: CallbackQuery) -> None:
    _, product_slug, provider = callback.data.split(":", 2)

    with SessionLocal() as session:
        user = session.scalar(select(User).where(User.tg_id == callback.from_user.id))
        if user is None:
            user = User(tg_id=callback.from_user.id, username=callback.from_user.username)
            session.add(user)
            session.flush()
        order = Order(
            user_id=user.id,
            product_slug=product_slug,
            amount_rub=100,
            provider=provider,
            status=OrderStatus.pending,
        )
        session.add(order)
        session.commit()
        session.refresh(order)

    pay_link = mock_invoice_link(provider, order.id)
    await callback.message.edit_text(
        f"Заказ #{order.id} создан.\nПлатежка: {provider}\nОплатить: {pay_link}\n\nПосле оплаты заказ переведите в paid через админ-панель.",
    )
    await callback.answer("Заказ создан")
