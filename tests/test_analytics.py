from app.services.analytics import calculate_profit


def test_calculate_profit():
    assert calculate_profit(1000, 10, 200) == 700
