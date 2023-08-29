from pydantic import BaseModel


class Tariff(BaseModel):
    city_name: str
    tariff_class: str
    min_price: float = 0
    include_minutes: float = 0
    include_kilometres: float = 0
    free_waiting: float = 0
    price_minute_inside: float = 0
    price_km_inside: float = 0
    price_minute_outside: float = 0
    price_km_outside: float = 0
    waiting_price: float = 0
