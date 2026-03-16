from dataclasses import dataclass

@dataclass
class ExchangeRates:
    base: str
    rates: dict[str, float]