import os
from typing import Any, Dict, List

import pandas as pd


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла и возвращает список словарей.

    Если файл пустой, не найден или поврежден, возвращает пустой список.
    """
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return []

    try:
        # Читаем CSV с разделителем точки с запятой (стандарт для выгрузок)
        df = pd.read_csv(file_path, sep=";")
        # Заменяем значения NaN на None для корректной сериализации
        df = df.replace({pd.NA: None, float("nan"): None})
        return df.to_dict(orient="records")  # type: ignore
    except Exception:
        return []


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """Считывает финансовые операции из Excel-файла (XLSX) и возвращает список словарей.

    Если файл пустой, не найден или поврежден, возвращает пустой список.
    """
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        return []

    try:
        df = pd.read_excel(file_path, engine="openpyxl")
        df = df.replace({pd.NA: None, float("nan"): None})
        return df.to_dict(orient="records")  # type: ignore
    except Exception:
        return []
