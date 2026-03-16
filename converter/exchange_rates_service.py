import json
import logging
import time
import requests
from .models import ExchangeRates
from .cache_service import CacheService

logger = logging.getLogger(__name__)

class ExchangeRatesService:
    BASE_URL = "https://api.exchangerate-api.com/v4/latest"
    TIMEOUT = 10
    MAX_RETRIES = 3
    RETRY_DELAY = 2

    def __init__(
        self,
        cache: CacheService | None = None,
        max_retries: int = MAX_RETRIES,
        retry_delay: int = RETRY_DELAY
    ) -> None:
        self.cache = cache
        self.max_retries = max_retries
        self.retry_delay = retry_delay


    def _fetch_from_api(self, base_currency: str) -> ExchangeRates:
        url = f"{self.BASE_URL}/{base_currency}"

        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.get(url, timeout=self.TIMEOUT)
                response.raise_for_status()
                data = response.json()
                return ExchangeRates(
                    base=data["base"],
                    rates=data["rates"]
                )
            
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed (attempt {attempt}/{self.max_retries}): {e}")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)
                else:
                    raise RuntimeError("Max retries reached. Unable to fetch rates.")

            except (json.JSONDecodeError, KeyError) as e:
                raise RuntimeError(f"Error processing JSON response: {e}")
         
        raise RuntimeError("Unexpected error while fetching from api")
    

    def get_rates(self, base_currency: str) -> ExchangeRates:
        if self.cache:
            rates = self.cache.load_from_cache(base_currency)
            if rates:
                return rates

        rates = self._fetch_from_api(base_currency)

        if self.cache:
            self.cache.save_to_cache(rates)

        return rates