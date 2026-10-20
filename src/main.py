import os
import pandas as pd
from src.utils import load_excel_transactions
from src.views import generate_main_page_data
from src.services import search_transactions
from src.reports import spending_by_category


def main() -> None:
    """Основная точка входа для демонстрации работы функций."""
    print("--- ЗАПУСК КУРСОВОЙ РАБОТЫ: АНАЛИЗ БАНКОВСКИХ ТРАНЗАКЦИЙ ---")

    excel_path = os.path.join("data", "operations.xlsx")
    print(f"\nШаг 1. Загрузка данных из {excel_path}...")
    transactions = load_excel_transactions(excel_path)

    if not transactions:
        print("Критическая ошибка: Не удалось загрузить данные.")
        return

    df_temp = pd.DataFrame(transactions)
    df_temp["parsed_date"] = pd.to_datetime(
        df_temp["Дата операции"], errors="coerce", dayfirst=True
    )
    latest_transaction_date = df_temp["parsed_date"].max()

    if pd.notna(latest_transaction_date):
        test_date = latest_transaction_date.strftime("%Y-%m-%d 14:00:00")
        report_date_str = latest_transaction_date.strftime("%d.%m.%Y")
    else:
        test_date = "2021-12-31 14:00:00"
        report_date_str = "31.12.2021"

    print(
        f"\nШаг 2. Генерация JSON для Главной страницы "
        f"на реальную дату файла: {test_date}..."
    )
    json_response = generate_main_page_data(test_date, transactions)
    print("Ответ сервера (JSON):")
    print(json_response)

    search_query = "Супермаркеты"
    print(
        f"\nШаг 3. Тестирование сервиса умного поиска "
        f"по запросу: '{search_query}'..."
    )
    found_transactions = search_transactions(transactions, search_query)
    print(f"Найдено релевантных транзакций: {len(found_transactions)}")

    print(
        f"\nШаг 4. Формирование отчета 'Траты по категории' "
        f"на дату: {report_date_str}..."
    )
    df_all = pd.DataFrame(transactions)
    report_df = spending_by_category(df_all, "Супермаркеты", test_date)
    print(
        f"Отчет успешно сформирован в pandas DataFrame. "
        f"Строк за 3 месяца: {len(report_df)}"
    )


if __name__ == "__main__":
    main()
