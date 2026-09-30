from typing import Any, Dict, Iterator, List


def filter_by_currency(
    transactions: List[Dict[str, Any]], currency: str
) -> Iterator[Dict[str, Any]]:
    """Фильтрует список транзакций по заданной валюте и возвращает итератор.

    :param transactions: Список словарей с данными о транзакциях.
    :param currency: Буквенный код валюты (например, 'USD', 'RUB').
    :return: Итератор транзакций с указанной валютой.
    """
    for transaction in transactions:
        amount_info = transaction.get("operationAmount", {})
        currency_info = amount_info.get("currency", {})
        if currency_info.get("code") == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """Генератор, возвращающий описание для каждой транзакции по очереди.

    :param transactions: Список словарей с данными о транзакциях.
    :return: Итератор строк с описанием операций.
    """
    for transaction in transactions:
        yield transaction.get("description", "Описание отсутствует")


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Генератор номеров банковских карт в заданном диапазоне.

    Формат номеров: XXXX XXXX XXXX XXXX.

    :param start: Начальное число диапазона.
    :param stop: Конечное число диапазона включительно.
    :return: Итератор строк с отформатированными номерами карт.
    """
    for number in range(start, stop + 1):
        str_num = f"{number:016d}"
        formatted_card = f"{str_num[:4]} {str_num[4:8]} {str_num[8:12]} {str_num[12:]}"
        yield formatted_card
