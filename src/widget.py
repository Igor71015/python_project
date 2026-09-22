from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """Принимает строку с типом и номером карты/счета и возвращает строку с маскированным номером."""

    parts = info.split()

    number = parts[-1]

    type_name = " ".join(parts[:-1])

    if type_name.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{type_name} {masked_number}"


def get_date(date_str: str) -> str:
    """Принимает строку с датой в формате ISO и возвращает её в формате ДД.ММ.ГГГГ."""
    date_part = date_str[:10]

    year, month, day = date_part.split("-")

    return f"{day}.{month}.{year}"
