import json
import logging
import os
import re
from collections import Counter
from typing import Any, Dict, List

# Настраиваем логер для модуля utils
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

# Создаем файловый обработчик с режимом перезаписи 'w'
file_handler = logging.FileHandler(
    "logs/utils.log", mode="w", encoding="utf-8"
)

# Настраиваем формат записи логов
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)

# Добавляем обработчик к логеру
logger.addHandler(file_handler)


def get_financial_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Читает данные о транзакциях из JSON-файла.

    Если файл пустой, содержит не список или не найден,
    функция возвращает пустой список.
    """
    logger.info(f"Попытка чтения транзакций из файла: {file_path}")

    if not os.path.exists(file_path):
        logger.error(f"Файл не найден по пути: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                logger.info(f"Успешно прочитано транзакций: {len(data)}")
                return data
            logger.error(f"Данные в файле {file_path} не являются списком")
            return []
    except (json.JSONDecodeError, TypeError) as e:
        logger.error(
            f"Ошибка при декодировании JSON в файле {file_path}: {str(e)}"
        )
        return []


def process_bank_search(
    data: List[Dict[str, Any]], search_string: str
) -> List[Dict[str, Any]]:
    """Ищет транзакции по заданной строке в описании через регулярные выражения.

    Поиск выполняется с использованием библиотеки re.
    """
    logger.info(
        f"Запущен поиск транзакций по регулярному выражению: '{search_string}'"
    )
    if not search_string:
        return data

    result = []
    try:
        pattern = re.compile(re.escape(search_string), re.IGNORECASE)
        for transaction in data:
            description = transaction.get("description", "")
            if pattern.search(description):
                result.append(transaction)
        logger.info(f"Поиск завершен. Найдено транзакций: {len(result)}")
    except Exception as e:
        logger.error(
            f"Ошибка при выполнении поиска по регулярному выражению: {str(e)}"
        )
        return []

    return result


def process_bank_operations(
    data: List[Dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
    """Подсчитывает количество банковских операций определенного типа.

    Подсчет выполняется на основе поля description с использованием Counter.
    """
    logger.info("Запущен подсчет транзакций по категориям на основе поля desc")
    descriptions = [
        transaction.get("description", "")
        for transaction in data
        if "description" in transaction
    ]

    counts = Counter(descriptions)

    result = {category: counts[category] for category in categories}
    logger.info(f"Подсчет категорий завершен. Результат: {result}")
    return result
