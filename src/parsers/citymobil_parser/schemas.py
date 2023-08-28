from pydantic import BaseModel


class Tariff(BaseModel):
    city: str
    ride_class: str
    min_price: float = 0
    include_min: float = 0
    include_km: float = 0
    min_inside_price: float = 0
    km_inside_price: float = 0
    min_outside_price: float = 0
    km_outside_price: float = 0
    free_wait: float = 0
    min_wait_price: float = 0

    def to_list(self):
        return [
            self.city,
            self.ride_class,
            self.min_price,
            self.include_min,
            self.include_km,
            self.min_inside_price,
            self.km_inside_price,
            self.min_outside_price,
            self.km_outside_price,
            self.free_wait,
            self.min_wait_price
        ]
