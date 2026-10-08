import json
import os
from typing import Any, Dict, List


def get_financial_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Читает данные о транзакциях из JSON-файла.

    Если файл пустой, содержит не список или не найден, функция возвращает пустой список.
    """
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, TypeError):
        return []
