from src.widget import get_date, mask_account_card

# Проверка маскировки карт и счетов
print(mask_account_card("Visa Platinum 7000792289606361"))
print(mask_account_card("Счет 73654108430135874305"))

# Проверка работы с датой
print(get_date("2024-03-11T02:26:18.671407"))
