import pytest
from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number_success() -> None:
    """Тест успешного маскирования номера карты."""
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"
    assert get_mask_card_number("7000 7922 8960 6361") == "7000 79** **** 6361"


def test_get_mask_card_number_invalid_length() -> None:
    """Тест вызова ошибки ValueError при неверной длине номера карты."""
    with pytest.raises(ValueError, match="Номер карты должен состоять из 16 цифр"):
        get_mask_card_number("12345")


def test_get_mask_account_success() -> None:
    """Тест успешного маскирования номера счета."""
    assert get_mask_account("73654108430135874305") == "**4305"


def test_get_mask_account_invalid_length() -> None:
    """Тест вызова ошибки ValueError при коротком номере счета."""
    with pytest.raises(ValueError, match="Номер счета должен содержать минимум 4 символа"):
        get_mask_account("123")
