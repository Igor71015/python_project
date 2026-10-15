from typing import Any, Dict, List


def filter_by_state(
    data: List[Dict[str, Any]], state: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """Фильтрует список словарей по значению ключа state.

    :param data: Список словарей с данными о транзакциях.
    :param state: Статус для фильтрации (например, EXECUTED, CANCELED).
    :return: Отфильтрованный список словарей.
    """
    return [
        transaction
        for transaction in data
        if transaction.get("state") == state
    ]


def sort_by_date(
    data: List[Dict[str, Any]], reverse: bool = True
) -> List[Dict[str, Any]]:
    """Сортирует список словарей по дате.

    :param data: Список словарей с данными о транзакциях.
    :param reverse: Порядок сортировки (True - по убыванию, False - по возрастанию).
    :return: Отсортированный список словарей.
    """
    return sorted(
        data,
        key=lambda transaction: transaction.get("date", ""),
        reverse=reverse,
    )
