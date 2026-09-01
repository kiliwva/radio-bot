from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select

from app.bot.keyboards.inline import main_menu_keyboard, products_keyboard, providers_keyboard
from app.config import PRODUCTS
from app.database import SessionLocal, User

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    with SessionLocal() as session:
        user = session.scalar(select(User).where(User.tg_id == message.from_user.id))
        if user is None:
            session.add(User(tg_id=message.from_user.id, username=message.from_user.username))
            session.commit()

    await message.answer(
        "Добро пожаловать в магазин цифровых товаров! Выберите действие:",
        reply_markup=main_menu_keyboard(),
    )


@router.callback_query(lambda c: c.data in {"menu:catalog", "menu:back"})
async def open_catalog(callback: CallbackQuery) -> None:
    await callback.message.edit_text("Выберите товар:", reply_markup=products_keyboard())
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.startswith("product:"))
async def select_product(callback: CallbackQuery) -> None:
    _, slug = callback.data.split(":", 1)
    product = next((item for item in PRODUCTS if item.slug == slug), None)
    if product is None:
        await callback.answer("Товар не найден", show_alert=True)
        return
    await callback.message.edit_text(
        f"{product.title}\n\n{product.description}\nЦена: {product.price_rub}₽\n\nВыберите платежную систему:",
        reply_markup=providers_keyboard(product.slug),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "menu:stars")
async def show_stars(callback: CallbackQuery) -> None:
    with SessionLocal() as session:
        user = session.scalar(select(User).where(User.tg_id == callback.from_user.id))
        balance = user.stars_balance if user else 0
    await callback.message.edit_text(
        f"Ваш баланс Stars: {balance}\n\nДля генерации чека отправьте команду: /check <amount>",
        reply_markup=main_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "menu:ticket")
async def ticket_hint(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "Создать обращение: /ticket Тема | Текст обращения",
        reply_markup=main_menu_keyboard(),
    )
    await callback.answer()
