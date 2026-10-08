import json
from unittest.mock import mock_open, patch
from src.utils import get_financial_transactions


def test_get_financial_transactions_success() -> None:
    """Тест успешного чтения корректного JSON-файла."""
    mock_data = [{"id": 1, "state": "EXECUTED"}]
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        with patch("os.path.exists", return_value=True):
            assert get_financial_transactions("data/operations.json") == mock_data


def test_get_financial_transactions_not_found() -> None:
    """Тест возврата пустого списка, если файл не найден."""
    with patch("os.path.exists", return_value=False):
        assert get_financial_transactions("invalid.json") == []
