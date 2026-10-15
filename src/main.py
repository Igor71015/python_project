import os
from src.utils import (
    get_financial_transactions,
    process_bank_search,
)
from src.file_readers import read_csv_file, read_excel_file
from src.processing import filter_by_state, sort_by_date
from src.generators import filter_by_currency
from src.widget import mask_account_card


def format_transaction_output(transaction: dict) -> str:
    """Форматирует транзакцию для вывода в консоль в соответствии с ТЗ."""
    raw_date = transaction.get("date", "")
    formatted_date = ""
    if raw_date and len(raw_date) >= 10:
        parts = raw_date[:10].split("-")
        if len(parts) == 3:
            formatted_date = f"{parts[2]}.{parts[1]}.{parts[0]}"

    description = transaction.get("description", "Описание отсутствует")

    from_info = transaction.get("from", "")
    to_info = transaction.get("to", "")

    from_masked = mask_account_card(from_info) if from_info else ""
    to_masked = mask_account_card(to_info) if to_info else ""

    if from_masked:
        direction = f"{from_masked} -> {to_masked}"
    else:
        direction = to_masked

    amount_info = transaction.get("operationAmount", {})
    amount = amount_info.get("amount", "0")
    currency = amount_info.get("currency", {}).get("name", "руб.")

    return (
        f"{formatted_date} {description}\n"
        f"{direction}\n"
        f"Сумма: {amount} {currency}\n"
    )


def main() -> None:
    """Основная логика программы для взаимодействия с пользователем."""
    print(
        "Привет! Добро пожаловать в программу работы "
        "с банковскими транзакциями."
    )
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input("Пользователь: ").strip()
        if choice == "1":
            print("\nПрограмма: Для обработки выбран JSON-файл.")
            transactions = get_financial_transactions(
                os.path.join("data", "operations.json")
            )
            break
        elif choice == "2":
            print("\nПрограмма: Для обработки выбран CSV-файл.")
            transactions = read_csv_file(
                os.path.join("data", "transactions.csv")
            )
            break
        elif choice == "3":
            print("\nПрограмма: Для обработки выбран XLSX-файл.")
            transactions = read_excel_file(
                os.path.join("data", "transactions_excel.xlsx")
            )
            break
        else:
            print("Неверный пункт меню. Пожалуйста, выберите 1, 2 или 3.")

    available_statuses = {"EXECUTED", "CANCELED", "PENDING"}
    while True:
        print(
            "\nПрограмма: Введите статус, по которому "
            "необходимо выполнить фильтрацию."
        )
        print(
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"
        )
        status_input = input("Пользователь: ").strip().upper()

        if status_input in available_statuses:
            transactions = filter_by_state(transactions, status_input)
            print(
                f'\nПрограмма: Операции отфильтрованы '
                f'по статусу "{status_input}"'
            )
            break
        else:
            print(f'\nПрограмма: Статус операции "{status_input}" недоступен.')

    print("\nПрограмма: Отсортировать операции по дате? Да/Нет")
    date_sort_choice = input("Пользователь: ").strip().lower()
    if date_sort_choice in ["да", "yes"]:
        print("\nПрограмма: Отсортировать по возрастанию или по убыванию?")
        sort_order = input("Пользователь: ").strip().lower()
        is_reverse = sort_order in ["по убыванию", "убывание", "desc"]
        transactions = sort_by_date(transactions, reverse=is_reverse)

    print("\nПрограмма: Выводить только рублевые транзакции? Да/Нет")
    rub_choice = input("Пользователь: ").strip().lower()
    if rub_choice in ["да", "yes"]:
        transactions = list(filter_by_currency(transactions, "RUB"))

    print(
        "\nПрограмма: Отfilter_by_currency список транзакций "
        "по определенному слову в описании? Да/Нет"
    )
    search_choice = input("Пользователь: ").strip().lower()
    if search_choice in ["да", "yes"]:
        print("\nПрограмма: Введите слово для поиска:")
        word_input = input("Пользователь: ").strip()
        transactions = process_bank_search(transactions, word_input)

    print("\nПрограмма: Распечатываю итоговый список транзакций...")
    if not transactions:
        print(
            "\nПрограмма: Не найдено ни одной транзакции, "
            "подходящей под ваши условия фильтрации"
        )
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")
    for trans in transactions:
        print(format_transaction_output(trans))


if __name__ == "__main__":
    main()
