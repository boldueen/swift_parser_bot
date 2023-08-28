from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message


class AdminFilter(BaseFilter):  # [1]
    def __init__(self, admins: Union[int, list]):  # [2]
        print('initing filter...', flush=True)
        self.admins = admins

    async def __call__(self, message: Message) -> bool:  # [3]
        if isinstance(self.admins, str):
            return message.from_user.id == self.admins
        else:
            return message.from_user.id in self.admins
