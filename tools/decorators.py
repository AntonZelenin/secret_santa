import time

MAX_RETRIES = 3


def retry(func):
    def wrapper(*args, **kwargs):
        retries = 0
        delay = 1
        backoff = 2
        while retries < MAX_RETRIES:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Retry {retries + 1}/{MAX_RETRIES}: {e}")
                retries += 1
                if retries < MAX_RETRIES:
                    time.sleep(delay)
                    delay *= backoff
                else:
                    raise

    return wrapper
