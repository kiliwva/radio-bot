from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from app.config import PRODUCTS, settings
from app.services.payments import enabled_providers


def main_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🛍 Каталог", callback_data="menu:catalog")],
        [InlineKeyboardButton(text="⭐ Stars баланс", callback_data="menu:stars")],
        [InlineKeyboardButton(text="🎫 Тикет в поддержку", callback_data="menu:ticket")],
        [InlineKeyboardButton(text="🌐 Web App", web_app=WebAppInfo(url=settings.webapp_url))],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def products_keyboard() -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=f"{item.title} — {item.price_rub}₽", callback_data=f"product:{item.slug}")] for item in PRODUCTS]
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="menu:back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def providers_keyboard(product_slug: str) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=provider.title, callback_data=f"buy:{product_slug}:{provider.code}")]
        for provider in enabled_providers()
    ]
    rows.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="menu:catalog")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
