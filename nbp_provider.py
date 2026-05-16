import requests
from datetime import datetime, timedelta

class NBPRateProvider:
    BASE_URL = "https://api.nbp.pl/api/exchangerates/rates/a/{currency}/{date}/?format=json"
    RANGE_URL = "https://api.nbp.pl/api/exchangerates/rates/a/{currency}/{start}/{end}/?format=json"

    def __init__(self, max_retry: int = 10, cache: dict[tuple[str, str], float] = None) -> None:
        self.max_retry = max_retry
        self._cache = cache if cache is not None else {}

    @classmethod
    def preload(cls, years: list[int], currencies: list[str]) -> "NBPRateProvider":
        cache = {}
        for currency in currencies:
            for year in years:
                rates = NBPRateProvider._gather_rates(year, currency)
                rate_cache = {(currency, date_str): rate for date_str, rate in rates.items()}
                cache.update(rate_cache)

        return cls(10, cache)

    @staticmethod
    def _gather_rates(year: int, currency: str) -> dict[str, float]:
        date_str_start = f"{year}-01-01"
        date_str_end = f"{year}-12-31"
        url = NBPRateProvider.RANGE_URL.format(currency=currency,
                                              start=date_str_start,
                                              end=date_str_end)
    
        response = requests.get(url)
        if response.status_code != 200:
            return {}
        
        rates = response.json()["rates"]
        rates = {rate["effectiveDate"]: rate["mid"] for rate in rates}
        return rates
    
    @staticmethod
    def _previous_business_day(date: str) -> str:
        date_formatted = datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1)
        while date_formatted.weekday() > 4:
            date_formatted -= timedelta(days=1)
        return date_formatted.strftime("%Y-%m-%d")
    
    def _check_previous_days(self, date: str, currency: str) -> tuple[str, float] | None:
        for _ in range(self.max_retry):
            date = self._previous_business_day(date)
            url = NBPRateProvider.BASE_URL.format(currency=currency, date=date)
            response = requests.get(url)
            if response.status_code == 200:
                return date, response.json()["rates"][0]["mid"]

    def get_rate(self, currency: str, date: str) -> float | None:
        yesterday = self._previous_business_day(date)
        cache_key = (currency, yesterday)
        cache_result = self._cache.get(cache_key, None)
        if cache_result:
            print(f"Successfully retreived rate for {yesterday} from cache.")
            return cache_result
        
        result = self._check_previous_days(yesterday, currency)
        if result is None:
            return None
        
        cache_date, rate = result
        self._cache[(currency, cache_date)] = rate
        return rate        


if __name__ == "__main__":
    provider = NBPRateProvider.preload([2024, 2025], ["USD", "GBP"])
    print(provider._cache)
