from typing import Any, Dict, List


def filter_by_state(data: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтрует список словарей по значению ключа 'state'.

    :param data: Исходный список словарей с данными об операциях.
    :param state: Статус для фильтрации (по умолчанию 'EXECUTED').
    :return: Новый список словарей, соответствующих указанному статусу.
    """
    filtered_list = []
    for item in data:
        if item.get("state") == state:
            filtered_list.append(item)
    return filtered_list


def sort_by_date(data: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """Сортирует список словарей по дате операции.

    :param data: Исходный список словарей с данными об операциях.
    :param reverse: Порядок сортировки. True — по убыванию (по умолчанию),
                    False — по возрастанию.
    :return: Новый отсортированный список словарей.
    """
    return sorted(data, key=lambda item: item.get("date", ""), reverse=reverse)
