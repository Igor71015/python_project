from typing import Any
from unittest.mock import patch
from src.external_api import convert_to_rub


def test_convert_to_rub_currency() -> None:
    """Тест работы функции, если валюта изначально RUB."""
    transaction = {"operationAmount": {"amount": "150.50", "currency": {"code": "RUB"}}}
    assert convert_to_rub(transaction) == 150.50


@patch("requests.get")
def test_convert_to_rub_with_mock_api(mock_get: Any) -> None:
    """Тест конвертации USD с использованием подмены ответа API (Mock)."""
    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}

    # Подменяем ответ сервера на наш фейковый словарь
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"rates": {"RUB": 75.00}}

    assert convert_to_rub(transaction) == 7500.00
