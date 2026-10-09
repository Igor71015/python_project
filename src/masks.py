import logging
import os

# Создаем папку logs, если её нет (для локального запуска)
os.makedirs("logs", exist_ok=True)

# Настраиваем логер для модуля masks
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

# Создаем файловый обработчик с режимом перезаписи 'w'
file_handler = logging.FileHandler(
    "logs/masks.log", mode="w", encoding="utf-8"
)

# Настраиваем формат записи логов
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)

# Добавляем обработчик к логеру
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Принимает номер карты ..."""
    clean_number = card_number.replace(" ", "")

    if not clean_number.isdigit() or len(clean_number) != 16:
        logger.error(
            f"Некорректный номер карты: {card_number}. Должно быть 16 цифр."
        )
        raise ValueError("Номер карты должен состоять из 16 цифр")

    masked = (
        f"{clean_number[:4]} {clean_number[4:6]}** **** {clean_number[-4:]}"
    )
    logger.info(f"Успешно замаскирован номер карты. Результат: {masked}")
    return masked


def get_mask_account(account_number: str) -> str:
    """Принимает номер счета ..."""
    if not account_number.isdigit() or len(account_number) < 4:
        logger.error(
            f"Некорректный номер счета: {account_number}. "
            f"Должен содержать минимум 4 цифры."
        )
        raise ValueError("Номер счета должен содержать минимум 4 символа")

    masked = f"**{account_number[-4:]}"
    logger.info(f"Успешно замаскирован номер счета. Результат: {masked}")
    return masked
