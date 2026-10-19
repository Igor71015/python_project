import logging
from typing import Any, Dict, List

logger = logging.getLogger("services")


def search_transactions(
    transactions: List[Dict[str, Any]], query: str
) -> List[Dict[str, Any]]:
    """Ищет транзакции по подстроке в полях 'Описание' или 'Категория'.

    Поиск нечувствителен к регистру.
    """
    logger.info(f"Запущен сервис поиска транзакций по запросу: '{query}'")
    if not query:
        return []

    query_lower = query.lower()
    result = []

    for transaction in transactions:
        description = str(transaction.get("Описание", "")).lower()
        category = str(transaction.get("Категория", "")).lower()

        if query_lower in description or query_lower in category:
            result.append(transaction)

    logger.info(f"Сервис поиска завершил работу. Найдено транзакций: {len(result)}")
    return result
