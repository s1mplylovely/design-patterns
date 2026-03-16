import logging
from converter import CurrencyConverter, ExchangeRatesService, CacheService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

BASE_CURRENCY : str = "USD"
TARGET_CURRENCIES : tuple[str] = ("CNY", "EUR", "GBP", "RUB", "88")
CACHE_FILE : str = "exchange_rates.json"


def build_converter() -> CurrencyConverter:
    cache = CacheService(cache_file=CACHE_FILE)
    api_service = ExchangeRatesService(cache=cache)
    return CurrencyConverter(api_service)


def main() -> None:
    try: 
        amount = float(input(f"Введите значение в {BASE_CURRENCY}: \n"))
    except ValueError:
        print("Ошибка: введите число.")
        return

    converter = build_converter()

    
    try:
        for currency in TARGET_CURRENCIES:
            result = converter.convert(amount, BASE_CURRENCY, currency)
            print(f"{amount} {BASE_CURRENCY} to {currency}: {result:.2f}")
    except ValueError as e:
        print(f"Конвертация в {currency} невозможна: {e}")
    except RuntimeError as e:
            print(f"Сервис недоступен: {e}")


if __name__ == "__main__":
    main()