from app.config import settings
from app.services.payments import enabled_providers


def test_enabled_providers_not_empty():
    settings.pally_enabled = True
    settings.platega_enabled = False
    settings.cryptobot_enabled = False
    settings.freekassa_enabled = False
    providers = enabled_providers()
    assert len(providers) == 1
    assert providers[0].code == "pally"
