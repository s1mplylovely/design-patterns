from typing import Protocol
from .models import ExchangeRates

class ExchangeRatesProvider(Protocol):
    def get_rates(self, base_currency: str) -> ExchangeRates:
        ...


class CurrencyConverter:
    def __init__(self, provider: ExchangeRatesProvider):
        self.provider = provider

    def convert(self, amount: float, base_currency: str, to_currency: str) -> float:
        rates = self.provider.get_rates(base_currency)
        rate = rates.rates.get(to_currency.upper())

        if rate is None:
            raise ValueError(f"Unknown currency: '{to_currency}'")

        return amount * rate