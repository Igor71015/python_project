def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты."""

    card_number = card_number.replace(" ", "")

    if len(card_number) != 16:
        raise ValueError("Номер карты должен состоять из 16 цифр")

    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"


def get_mask_account(account_number: str) -> str:

    account_number = account_number.replace(" ", "")

    if len(account_number) < 4:
        raise ValueError("Номер счета должен содержать минимум 4 символа")

    return f"**{account_number[-4:]}"
