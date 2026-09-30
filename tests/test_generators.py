from typing import Any, Dict, List
import pytest
from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def transactions_mock() -> List[Dict[str, Any]]:
    """Фикстура с тестовым набором транзакций."""
    return [
        {
            "id": 1,
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Перевод организации",
        },
        {
            "id": 2,
            "operationAmount": {"currency": {"code": "USD"}},
            "description": "Перевод со счета на счет",
        },
        {
            "id": 3,
            "operationAmount": {"currency": {"code": "RUB"}},
            "description": "Перевод со счета на счет",
        },
    ]


def test_filter_by_currency_success(transactions_mock: List[Dict[str, Any]]) -> None:
    """Тест успешной фильтрации по валюте."""
    usd_iterator = filter_by_currency(transactions_mock, "USD")
    assert next(usd_iterator)["id"] == 1
    assert next(usd_iterator)["id"] == 2
    with pytest.raises(StopIteration):
        next(usd_iterator)


def test_filter_by_currency_empty() -> None:
    """Тест фильтрации пустого списка."""
    iterator = filter_by_currency([], "USD")
    with pytest.raises(StopIteration):
        next(iterator)


def test_transaction_descriptions(transactions_mock: List[Dict[str, Any]]) -> None:
    """Тест получения описаний операций."""
    descriptions = transaction_descriptions(transactions_mock)
    assert next(descriptions) == "Перевод организации"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод со счета на счет"
    with pytest.raises(StopIteration):
        next(descriptions)


@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (1, 2, ["0000 0000 0000 0001", "0000 0000 0000 0002"]),
        (999, 1000, ["0000 0000 0000 0999", "0000 0000 0000 1000"]),
    ],
)
def test_card_number_generator(start: int, stop: int, expected: List[str]) -> None:
    """Параметризованный тест генератора номеров карт."""
    result = list(card_number_generator(start, stop))
    assert result == expected
