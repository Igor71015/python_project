import json
import logging
import os
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
    """Читает данные о транзакциях из JSON-файла ..."""
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
