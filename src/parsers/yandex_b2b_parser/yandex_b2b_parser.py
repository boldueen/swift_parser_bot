import time
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from logger import Logger


def parse_yandex_b2b_rates() -> str:
    Logger.info('startig to parse yandex_b2b rates')

    filename = f'/data/yandex_b2b_rates_{int(time.time())}.xlsx'
    wb = Workbook()
    ws: Worksheet = wb.active
    ws.cell(1, 1, 'ti krasava')
    wb.save(filename)
    Logger.info('successfully parsed new yandex_b2b rates')
    return filename
