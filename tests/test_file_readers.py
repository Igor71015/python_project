from unittest.mock import MagicMock, patch

import pandas as pd

from src.file_readers import read_csv_file, read_excel_file


@patch("os.path.exists")
@patch("os.path.getsize")
@patch("pandas.read_csv")
def test_read_csv_file_success(
    mock_read_csv: MagicMock, mock_getsize: MagicMock, mock_exists: MagicMock
) -> None:
    """Тест успешного чтения корректного CSV-файла."""
    mock_exists.return_value = True
    mock_getsize.return_value = 100

    # Создаем фейковый DataFrame от pandas
    mock_df = pd.DataFrame([{"id": 123, "amount": 500.0}])
    mock_read_csv.return_value = mock_df

    result = read_csv_file("dummy.csv")
    assert result == [{"id": 123, "amount": 500.0}]


@patch("os.path.exists")
def test_read_csv_file_not_found(mock_exists: MagicMock) -> None:
    """Тест возврата пустого списка, если CSV-файл не найден."""
    mock_exists.return_value = False
    assert read_csv_file("missing.csv") == []


@patch("os.path.exists")
@patch("os.path.getsize")
@patch("pandas.read_excel")
def test_read_excel_file_success(
    mock_read_excel: MagicMock, mock_getsize: MagicMock, mock_exists: MagicMock
) -> None:
    """Тест успешного чтения корректного Excel-файла."""
    mock_exists.return_value = True
    mock_getsize.return_value = 200

    mock_df = pd.DataFrame([{"id": 456, "amount": 1000.0}])
    mock_read_excel.return_value = mock_df

    result = read_excel_file("dummy.xlsx")
    assert result == [{"id": 456, "amount": 1000.0}]


@patch("os.path.exists")
def test_read_excel_file_not_found(mock_exists: MagicMock) -> None:
    """Тест возврата пустого списка, если Excel-файл не найден."""
    mock_exists.return_value = False
    assert read_excel_file("missing.xlsx") == []
