from redis import Redis


def save_filepath_to_redis(filepath: str):
    r = Redis('redis', decode_responses=True)
    r.set('parsed:rates:yandex_b2c', filepath)
    print('saved', flush=True)
    r.close()
