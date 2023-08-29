from time import time

from openpyxl.workbook import Workbook

from schemas import Tariff


def save_to_excel(rates: list[Tariff]):
    filepath = f'/data/yandex_tares_b2c_{int(time())}.xlsx'
    wb = Workbook()
    ws = wb.active
    titles = [
        'city_name',
        'tariff_class',
        'min_price',
        'include_minutes',
        'include_kilometres',
        'free_waiting',
        'price_minute_inside',
        'price_km_inside',
        'price_minute_outside',
        'price_km_outside',
        'waiting_price'
    ]
    ws.append(titles)
    for rate in rates:
        ws.append([
            rate.city_name,
            rate.tariff_class,
            rate.min_price,
            rate.include_minutes,
            rate.include_kilometres,
            rate.free_waiting,
            rate.price_minute_inside,
            rate.price_km_inside,
            rate.price_minute_outside,
            rate.price_km_outside,
            rate.waiting_price
        ])
    wb.save(filepath)
    print('yandex_b2c rates successfully parsed!', flush=True)
    return filepath
