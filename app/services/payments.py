from dataclasses import dataclass

from app.config import settings


@dataclass
class PaymentProvider:
    code: str
    title: str
    enabled: bool


def get_providers() -> list[PaymentProvider]:
    return [
        PaymentProvider("pally", "Pally", settings.pally_enabled),
        PaymentProvider("platega", "Platega", settings.platega_enabled),
        PaymentProvider("cryptobot", "CryptoBot", settings.cryptobot_enabled),
        PaymentProvider("freekassa", "FreeKassa", settings.freekassa_enabled),
    ]


def enabled_providers() -> list[PaymentProvider]:
    return [provider for provider in get_providers() if provider.enabled]


def mock_invoice_link(provider_code: str, order_id: int) -> str:
    return f"https://pay.local/{provider_code}/invoice/{order_id}"
