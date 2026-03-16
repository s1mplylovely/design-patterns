import json
import logging
import time
from .models import ExchangeRates

logger = logging.getLogger(__name__)

class CacheService:
    CACHE_EXPIRY = 3600

    def __init__(
        self,
        cache_file: str | None = None,
        cache_expiry: int = CACHE_EXPIRY
    ) -> None:
        self.cache_file = cache_file
        self.cache_expiry = cache_expiry


    def load_from_cache(self, base_currency: str) -> ExchangeRates | None:
        if not self.cache_file:
            return None

        try:
            with open(self.cache_file, "r") as f:
                data = json.load(f)
                if (
                    time.time() - data["timestamp"] < self.cache_expiry
                    and data.get("base") == base_currency
                ):
                    return ExchangeRates(base=data["base"], rates=data["rates"])
                
        except FileNotFoundError:
            logger.info(f"Cache file '{self.cache_file}' not found. Fetching from API.")

        except (json.JSONDecodeError, KeyError):
            logger.warning(f"Invalid cache file '{self.cache_file}'. Fetching from API.")

        return None


    def save_to_cache(self, rates: ExchangeRates) -> None:
        if not self.cache_file:
            return
        
        try:
            with open(self.cache_file, "w") as f:
                json.dump({
                    "timestamp": time.time(),
                    "base": rates.base,
                    "rates": rates.rates
                    }, f)
        except OSError as e:
            logger.warning(f"Error saving to cache: {e}")