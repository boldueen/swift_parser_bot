import time
import json
from datetime import datetime

import requests
from openpyxl.workbook import Workbook
from pydantic import BaseModel
from bs4 import BeautifulSoup


from schemas import Tariff


YA_PREFIX = 'https://taxi.yandex.ru/'


def extract_include_values(include_values_str: str):
    #  'Минимальная стоимость (включено 6 мин и 3 км)'
    include_values_list = include_values_str.split(' ')
    include_minutes = 0
    include_kilometres = 0
    try:
        include_minutes = float(
            include_values_list[include_values_list.index('мин') - 1])
    except:
        pass

    try:
        include_minutes += float(
            include_values_list[include_values_list.index('сек')-1])/60
    except:
        pass

    try:
        include_kilometres = float(
            include_values_list[include_values_list.index('км)') - 1])
    except:
        pass

    return include_minutes, include_kilometres


def extract_tariffs(tariffs: dict) -> list[Tariff]:

    if tariffs is None:
        return None

    tariffs_pretty = []

    for tariff in tariffs:
        city_name: str
        tariff_class = tariff.get('name')

        min_price: float
        include_minutes: float
        include_kilometres: float
        free_waiting: float
        waiting_price: float
        price_minute_inside: float = 0
        price_km_inside: float = 0
        price_minute_outside: float = 0
        price_km_outside: float = 0

        category_types: dict[dict] = tariff.get('intervals')
        for category_type in category_types:
            price_type = category_type.get('category_type')
            if price_type == 'application':
                price_groups: list[dict] = category_type.get('price_groups')
                for price_group in price_groups:

                    price_group_id = price_group.get('id')
                    if price_group_id == 'free_route':
                        city_name = price_group.get('name').replace(
                            'По городу (', '').replace(')', '')
                        prices = price_group.get('prices')
                        for price in prices:
                            print(price)
                            price_id = price.get('id')
                            if price_id == 'taximeter.min_price_included_distance_and_time' or price_id == 'taximeter.min_price_included' or price_id == 'taximeter.once_price':
                                min_price = extract_number(price.get('price'))
                                include_minutes, include_kilometres = extract_include_values(
                                    price.get('name'))

                            if price_id == 'free_waiting':
                                free_waiting = extract_number(
                                    price.get('price'))

                            if price_id == 'paid_waiting':
                                waiting_price = extract_number(
                                    price.get('price'))

                            if price_id == 'taximeter.meter_next_inside_area' or price_id == 'taximeter.meter_inside_area':
                                if price.get('visual_group') == 'main':
                                    if price.get('price').rfind('мин') != -1:
                                        # price of minute INSIDE
                                        price_minute_inside = extract_number(
                                            price.get('price'))

                                    if price.get('price').rfind('км') != -1:
                                        # price of kilometre INSIDE
                                        price_km_inside = extract_number(
                                            price.get('price'))

                                if price.get('visual_group') == 'other':
                                    # price OUTSIDE city
                                    if price.get('price').rfind('мин') != -1:
                                        # price of minute OUTSIDE
                                        price_minute_outside = extract_number(
                                            price.get('price'))

                                    if price.get('price').rfind('км') != -1:
                                        # price of kilometre OUTSIDE
                                        price_km_outside = extract_number(
                                            price.get('price'))

                tariff_pretty_obj = Tariff(
                    city_name=city_name,
                    tariff_class=tariff_class,
                    min_price=min_price,
                    include_minutes=include_minutes,
                    include_kilometres=include_kilometres,
                    free_waiting=free_waiting,
                    waiting_price=waiting_price,
                    price_minute_inside=price_minute_inside,
                    price_km_inside=price_km_inside,
                    price_minute_outside=price_minute_outside,
                    price_km_outside=price_km_outside
                )

                print(city_name,
                      tariff_class,
                      min_price,
                      include_minutes,
                      include_kilometres,
                      free_waiting,
                      waiting_price,
                      price_minute_inside,
                      price_km_inside,
                      price_minute_outside,
                      price_km_outside, flush=True)

                tariffs_pretty.append(tariff_pretty_obj)
    return tariffs_pretty


def extract_number(price_str: str) -> float:
    print(price_str)
    price_str = price_str.replace(' ', ' ').replace(
        ',', '.').replace('\u202f', '')
    # print(price_str)
    price = price_str.split(' ')
    try:
        return float(price[0])
    except:
        return float(0)


def parse_links():

    all_rates = []

    links = generate_links('./cities.txt')
    print(len(links))

    for link in links:
        response = requests.get(YA_PREFIX+link+'/tariff')
        if response.status_code != 200:
            print(f'{link} IS NOT ACCESSABLE (status_code: {response.status_code})')
            continue
        soup = BeautifulSoup(response.text, 'lxml')
        scripts = soup.find_all('script')
        tariff_obj = scripts[-1].text.replace('__init__.default(', '')[0:-1]
        tariff_obj_parsed = json.loads(tariff_obj)
        tariffs = tariff_obj_parsed.get('initialState', {}).get(
            'zonaltariffdescription', {}).get('max_tariffs', None)

        rates_in_city = extract_tariffs(tariffs=tariffs)

        if rates_in_city is None:
            continue

        for rate in rates_in_city:

            all_rates.append(rate)

    return all_rates


def parse_links():

    all_rates = []

    links = generate_links('./cities.txt')

    for link in links:
        response = requests.get(YA_PREFIX+link+'/tariff')
        if response.status_code != 200:
            print(
                f'{link} IS NOT ACCESSABLE (status_code: {response.status_code})', flush=True)
            continue
        soup = BeautifulSoup(response.text, 'lxml')
        scripts = soup.find_all('script')
        tariff_obj = scripts[-1].text.replace('__init__.default(', '')[0:-1]
        tariff_obj_parsed = json.loads(tariff_obj)
        tariffs = tariff_obj_parsed.get('initialState', {}).get(
            'zonaltariffdescription', {}).get('max_tariffs', None)

        rates_in_city = extract_tariffs(tariffs=tariffs)

        if rates_in_city is None:
            continue

        for rate in rates_in_city:

            all_rates.append(rate)

    return all_rates


def generate_links(filepath: str) -> list[str]:
    return open(filepath, 'r').read().split('\n')
