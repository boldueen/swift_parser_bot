import requests
from schemas import LogBody
from schemas import LogLevel
from config import settings


def is_body_correct(body: dict) -> bool:

    # TODO: validate if body is correct
    return True


def get_log_body(body: dict) -> LogBody:
    print(body)
    user_id = body.get('user_id')
    if user_id is None:
        user_id = settings.TG_ADMIN
    message = body.get('message')
    level = get_log_level(body.get('level'))
    log_body = LogBody(user_id=user_id, message=message, level=level)
    return log_body


def get_log_level(level: str | None) -> LogLevel:
    if level is None:
        return LogLevel.INFO

    if level.upper() == 'ERROR':
        return LogLevel.ERROR
    return LogLevel.INFO


def send_log(log_body: LogBody):
    print(
        f'log has been sent, {log_body.level} {log_body.user_id} {log_body.message}', flush=True)

    pretty_log = get_pretty_log_message(log_body)

    print('pretty_log =', pretty_log, flush=True)

    url = f"https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage"
    response = requests.post(url,
                             json={'chat_id': log_body.user_id,
                                   'text': pretty_log}
                             )

    print(response)


def get_pretty_log_message(log_body: LogBody) -> str:
    print('getting pretty msg...', flush=True)

    print('log_level:', log_body.level, flush=True)
    print('user_id:', log_body.user_id, flush=True)
    print('message:', log_body.message, flush=True)

    if log_body.level == LogLevel.ERROR:
        pretty_log = f'❌ ERROR ❌\n{log_body.message}'
        return pretty_log

    if log_body.level == LogLevel.INFO:
        pretty_log = f'⚙️ INFO ⚙️\n{log_body.message}'
        return pretty_log

    return log_body.message
