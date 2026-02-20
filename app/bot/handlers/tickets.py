from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database import SessionLocal, Ticket, User

router = Router()


@router.message(Command("ticket"))
async def create_ticket(message: Message) -> None:
    payload = (message.text or "").replace("/ticket", "", 1).strip()
    if "|" not in payload:
        await message.answer("Формат: /ticket Тема | Текст")
        return

    subject, body = [part.strip() for part in payload.split("|", 1)]
    with SessionLocal() as session:
        user = session.query(User).filter(User.tg_id == message.from_user.id).first()
        if user is None:
            user = User(tg_id=message.from_user.id, username=message.from_user.username)
            session.add(user)
            session.flush()

        ticket = Ticket(user_id=user.id, subject=subject, message=body)
        session.add(ticket)
        session.commit()

    await message.answer(f"Тикет #{ticket.id} создан. Поддержка ответит в ближайшее время.")
