import os
from typing import Any, Dict
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """Возвращает сумму транзакции в рублях (float).

    Если транзакция в USD или EUR, запрашивает курс через API.
    """
    amount_info = transaction.get("operationAmount", {})
    amount = float(amount_info.get("amount", 0.0))
    currency_info = amount_info.get("currency", {})
    currency_code = currency_info.get("code", "RUB")

    if currency_code == "RUB":
        return amount

    if currency_code in ["USD", "EUR"]:
        url = f"https://marketstack.com{currency_code}"
        try:
            params = {"access_key": API_KEY}
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                rate = float(data.get("rates", {}).get("RUB", 1.0))
                return amount * rate
        except requests.RequestException:
            return 0.0

    return 0.0
