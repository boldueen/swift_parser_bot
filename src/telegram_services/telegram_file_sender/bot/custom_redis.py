from redis import Redis


class CustomRedis(Redis):
    yandes_b2b_key: str = ''
    yandes_b2c_key: str = ''
    citymobil_key: str = ''

    def __init__(self) -> None:
        print('connecting to redis...', flush=True)
        super().__init__(host='redis', decode_responses=True)
        print('connected to redis!!!', flush=True)

    def get_filepath_by_filetype(self, filetype: str) -> str:
        filepath: str
        if filetype == 'yandex_b2b':
            filepath = super().get('parsed:rates:yandex_b2b')

        if filetype == 'yandex_b2c':
            filepath = super().get('parsed:rates:yandex_b2c')

        if filetype == 'citymobil':
            filepath = super().get('parsed:rates:citymobil')

        if filepath == '' or filepath is None:
            print(f'no available filepath for {filetype}', flush=True)
            return None

        return filepath
