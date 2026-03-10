import datetime


def iso8601_now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
