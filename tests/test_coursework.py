from unittest.mock import MagicMock, patch
import pandas as pd
import pytest
from src.views import get_welcome_message, generate_main_page_data
from src.services import search_transactions
from src.reports import spending_by_category


@pytest.fixture
def sample_transactions():
    return [
        {"Дата операции": "01.12.2021 10:00:00", "Сумма операции": -150.0, "Номер карты": "*4556", "Категория": "Супермаркеты", "Описание": "Магнит"},
        {"Дата операции": "15.12.2021 14:00:00", "Сумма операции": -3000.0, "Номер карты": "*5091", "Категория": "Супермаркеты", "Описание": "Пятерочка"},
        {"Дата операции": "20.12.2021 19:00:00", "Сумма операции": 5000.0, "Номер карты": "*4556", "Категория": "Пополнения", "Описание": "Перевод"},
    ]


def test_get_welcome_message():
    """Тест генерации приветствий в зависимости от времени."""
    from datetime import datetime
    assert get_welcome_message(datetime(2021, 12, 31, 9, 0, 0)) == "Доброе утро"
    assert get_welcome_message(datetime(2021, 12, 31, 14, 0, 0)) == "Добрый день"
    assert get_welcome_message(datetime(2021, 12, 31, 20, 0, 0)) == "Добрый вечер"
    assert get_welcome_message(datetime(2021, 12, 31, 23, 0, 0)) == "Доброй ночи"


def test_search_transactions(sample_transactions):
    """Тест сервиса умного поиска."""
    assert len(search_transactions(sample_transactions, "Магнит")) == 1
    assert len(search_transactions(sample_transactions, "Супермаркеты")) == 2
    assert len(search_transactions(sample_transactions, "Несуществующий")) == 0


def test_spending_by_category(sample_transactions):
    """Тест генерации отчета по категории."""
    df = pd.DataFrame(sample_transactions)
    result_df = spending_by_category(df, "Супермаркеты", "2021-12-31 23:59:59")
    assert len(result_df) == 2


@patch("os.path.exists")
def test_generate_main_page_data_empty(mock_exists):
    """Тест генерации главной страницы при отсутствии данных."""
    mock_exists.return_value = False
    result = generate_main_page_data("2021-12-31 14:00:00", [])
    assert "greeting" in result
