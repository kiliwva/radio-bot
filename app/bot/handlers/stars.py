from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database import SessionLocal
from app.services.stars import add_stars, create_stars_check

router = Router()


@router.message(Command("topup"))
async def topup_stars(message: Message) -> None:
    parts = (message.text or "").split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Использование: /topup <amount>")
        return

    amount = int(parts[1])
    with SessionLocal() as session:
        balance = add_stars(session, message.from_user.id, amount)
    await message.answer(f"Баланс пополнен. Текущий баланс: {balance} Stars")


@router.message(Command("check"))
async def make_check(message: Message) -> None:
    parts = (message.text or "").split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Использование: /check <amount>")
        return

    amount = int(parts[1])
    with SessionLocal() as session:
        try:
            code = create_stars_check(session, message.from_user.id, amount)
        except ValueError as exc:
            await message.answer(str(exc))
            return
    await message.answer(f"Чек создан: `{code}`", parse_mode="Markdown")
