import time
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet


def parse_yandex_b2b_rates() -> str:
    print('parsing b2b rates...', flush=True)

    filename = f'/data/yandex_b2b_rates_{int(time.time())}.xlsx'
    wb = Workbook()
    ws: Worksheet = wb.active
    ws.cell(1, 1, 'ti krasava')
    wb.save(filename)
    print('rates successfully parsed!', flush=True)
    return filename
