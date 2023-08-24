# from .container import redis
from .custom_redis import CustomRedis

redis = CustomRedis()


def is_body_correct(body: dict) -> bool:
    # TODO: check if body correct(has id_to_send and filetype)
    return True


def get_filepath_by_filetype(filetype: str) -> str:
    filepath = redis.get_filepath_by_filetype(filetype)
    return filepath
