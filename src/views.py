import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List
import pandas as pd

logger = logging.getLogger("views")


def get_welcome_message(current_time: datetime) -> str:
    """Возвращает приветствие в зависимости от временного интервала."""
    hour = current_time.hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def generate_main_page_data(
    date_str: str,
    transactions: List[Dict[str, Any]],
    user_settings_path: str = "user_settings.json",
) -> str:
    """Генерирует JSON-данные для главной страницы."""
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        welcome = get_welcome_message(target_date)

        start_of_month = target_date.replace(
            day=1, hour=0, minute=0, second=0
        )

        if os.path.exists(user_settings_path):
            with open(user_settings_path, "r", encoding="utf-8") as f:
                settings = json.load(f)
        else:
            settings = {
                "user_currencies": ["USD", "EUR"],
                "user_stocks": ["AAPL"],
            }

        df = pd.DataFrame(transactions)
        if df.empty:
            return json.dumps(
                {
                    "greeting": welcome,
                    "cards": [],
                    "top_transactions": [],
                    "currency_rates": [],
                    "stock_prices": [],
                },
                ensure_ascii=False,
                indent=2,
            )

        df["date_parsed"] = pd.to_datetime(
            df["Дата операции"], errors="coerce", dayfirst=True
        )
        mask = (df["date_parsed"] >= start_of_month) & (
            df["date_parsed"] <= target_date
        )
        filtered_df = df[mask]

        cards_list = []
        if "Номер карты" in filtered_df.columns:
            spend_df = filtered_df[
                filtered_df["Сумма операции"] < 0
            ].dropna(subset=["Номер карты"])

            for card, card_group in spend_df.groupby("Номер карты"):
                card_str = str(card).strip()
                if card_str:
                    total_spend = abs(card_group["Сумма операции"].sum())
                    cashback = int(total_spend // 100)
                    cards_list.append(
                        {
                            "last_digits": (
                                card_str[-4:]
                                if len(card_str) >= 4
                                else card_str
                            ),
                            "total_spend": round(total_spend, 2),
                            "cashback": cashback,
                        }
                    )

        top_transactions = []
        if not filtered_df.empty:
            top_df = filtered_df.sort_values(
                by="Сумма операции", ascending=True
            ).head(5)
            for _, row in top_df.iterrows():
                t_date = row["date_parsed"]
                top_transactions.append(
                    {
                        "date": (
                            t_date.strftime("%d.%m.%Y")
                            if pd.notna(t_date)
                            else ""
                        ),
                        "amount": round(abs(row["Сумма операции"]), 2),
                        "category": row.get("Категория", "Остальное"),
                        "description": row.get("Описание", ""),
                    }
                )

        response = {
            "greeting": welcome,
            "cards": cards_list,
            "top_transactions": top_transactions,
            "currency_rates": [
                {"currency": curr, "rate": 1.0}
                for curr in settings.get("user_currencies", [])
            ],
            "stock_prices": [
                {"stock": stock, "price": 1.0}
                for stock in settings.get("user_stocks", [])
            ],
        }
        return json.dumps(response, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Ошибка главной страницы: {str(e)}")
        return json.dumps(
            {"error": "Внутренняя ошибка сервера"}, ensure_ascii=False
        )
