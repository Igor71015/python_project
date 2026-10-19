import logging
from datetime import datetime, timedelta
from typing import Optional
import pandas as pd

logger = logging.getLogger("reports")


def spending_by_category(
    df: pd.DataFrame, category: str, date_str: Optional[str] = None
) -> pd.DataFrame:
    """Возвращает транзакции по заданной категории за последние 3 месяца.

    Если дата не передана, берется текущая дата.
    """
    logger.info(f"Генерация отчета 'Траты по категории' для: {category}")
    if df.empty:
        return pd.DataFrame()

    if date_str:
        try:
            end_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                end_date = datetime.strptime(date_str, "%d.%m.%Y")
            except ValueError:
                logger.error(f"Неверный формат даты в отчете: {date_str}")
                return pd.DataFrame()
    else:
        end_date = datetime.now()

    start_date = end_date - timedelta(days=90)

    df_copy = df.copy()
    df_copy["date_parsed"] = pd.to_datetime(
        df_copy["Дата операции"], errors="coerce", dayfirst=True
    )

    mask = (
        (df_copy["date_parsed"] >= start_date)
        & (df_copy["date_parsed"] <= end_date)
        & (df_copy["Категория"].str.lower() == category.lower())
    )

    result_df = df_copy[mask]
    logger.info(f"Отчет успешно сформирован. Строк: {len(result_df)}")
    return result_df.drop(columns=["date_parsed"], errors="ignore")
