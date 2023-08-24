from redis import Redis


class CustomRedis(Redis):
    yandes_b2b_key: str = ''
    yandes_b2c_key: str = ''
    citymobil_key: str = ''

    def __init__(self) -> None:
        print('connecting to redis...', flush=True)
        super().__init__(host='redis', decode_responses=True)
        print('connected to redis!!!', flush=True)

        pass

    def get_filepath_by_filetype(self, filetype: str) -> str:
        if filetype == 'yandex_b2b':
            return super().get('parsed:rates:yandex_b2b')
        # TODO: all filetypes
        return None
