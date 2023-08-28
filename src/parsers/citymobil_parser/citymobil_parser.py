import time
import requests
import json
from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from schemas import Tariff
# from logger import Logger


def fetch_data() -> dict:
    headers = {
        'cookie': f'_ym_uid=1680622743785135669; _ym_d=1680622743; _ga=GA1.1.897388559.1680622743; _ym_isad=1; city=%D0%90%D0%B4%D0%BB%D0%B5%D1%80; _ym_visorc=w; _ga_C7TJW524WJ=GS1.1.1680622742.1.1.1680622750.0.0.0; _ga_EKRYN3QXRQ=GS1.1.1680622742.1.1.1680622750.0.0.0',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    response = requests.get(
        'https://city-mobil.ru/tariffs', headers=headers)

    soup = BeautifulSoup(response.text, 'lxml')
    raw_json_tariffs = soup.find(id='__NEXT_DATA__')
    tariffs_objects = json.loads(raw_json_tariffs.text)

    cities_objects = tariffs_objects.get(
        'props').get('pageProps').get('tariffs')

    return cities_objects


def process_response(cities_objects: dict) -> list[Tariff]:
    pretty_tariffs: list[Tariff] = []
    for city_name, tariffs_in_city in cities_objects.items():
        for tariff_name, raw_tariffs in tariffs_in_city.get('app').items():
            tariff = extract_tariff(city_name, tariff_name, raw_tariffs)
            pretty_tariffs.append(tariff)

    return pretty_tariffs


def extract_tariff(tariff_city: str, ride_class: str, raw_tariff: dict) -> Tariff:
    tariff = Tariff(city=tariff_city, ride_class=ride_class)
    tariff.min_price = raw_tariff.get('minPrice', 0)
    tariff.include_min = raw_tariff.get('prepaidTime', 0)
    tariff.include_km = raw_tariff.get('prepaidWay', 0)
    tariff.min_inside_price = raw_tariff.get('priceTime', 0)
    tariff.km_inside_price = raw_tariff.get('priceWay', 0)
    tariff.min_outside_price = 0
    tariff.km_outside_price = raw_tariff.get('services', {}).get(
        'serviceWay2', {}).get('price', 0)
    tariff.free_wait = raw_tariff.get('freeWaitingTime', 0)
    tariff.min_wait_price = raw_tariff.get('waitingPrice', 0)
    return tariff


def get_headers():
    return [
        'Город',
        'Класс',
        'Минимальная стоимость',
        'включено минут',
        'вклчено км',
        'стоимость минуты (в городе)',
        'стоимость километра (в городе)',
        'стоимость минуты (за городом)',
        'стоимость километра (за городом)',
        'бесплатное ожидание',
        'стоимость минуты платного ожидания'
    ]


def save_to_excel(tariffs: list[Tariff]):
    wb = Workbook()
    wb_name = f'/data/citymobil_rates_{int(time.time())}.xlsx'
    ws = wb.active

    ws.append(get_headers())
    for tariff in tariffs:
        ws.append(tariff.to_list())

    wb.save(wb_name)
    return wb_name


def parse_citymobil_rates():
    print('starting... .. .', flush=True)
    tariffs_response = fetch_data()
    tariffs = process_response(tariffs_response)
    filename = save_to_excel(tariffs)
    print(f'SUCCESS! parsed {len(tariffs)} tariffs', flush=True)

    return filename
