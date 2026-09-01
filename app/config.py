from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Product(BaseModel):
    slug: str
    title: str
    price_rub: int
    description: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    bot_token: str = "CHANGE_ME"
    admin_ids: str = ""
    database_url: str = "sqlite:///./radio_bot.db"
    webapp_url: str = "https://example.com/webapp"

    pally_enabled: bool = True
    platega_enabled: bool = True
    cryptobot_enabled: bool = True
    freekassa_enabled: bool = True


PRODUCTS = [
    Product(
        slug="tg_stars",
        title="Telegram Stars",
        price_rub=100,
        description="Пополнение Stars с быстрым зачислением.",
    ),
    Product(
        slug="nft_rent",
        title="Аренда NFT",
        price_rub=450,
        description="Почасовая/дневная аренда NFT-активов.",
    ),
    Product(
        slug="virtual_numbers",
        title="Аренда виртуальных номеров",
        price_rub=150,
        description="Номера для регистрации сервисов и мессенджеров.",
    ),
    Product(
        slug="tg_premium",
        title="Telegram Premium",
        price_rub=350,
        description="Оформление Premium подписки для аккаунта.",
    ),
]


settings = Settings()
