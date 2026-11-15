import argparse
import ssl
import time
import urllib.error
import urllib.request
from urllib.parse import urlsplit

import certifi

REQUEST_COUNT = 10
REQUEST_TIMEOUT = 15

CHUNK_SIZE = 64 * 1024

BYTES_PER_MEGABYTE = 1_000_000
BITS_PER_MEGABIT = 1_000_000
BITS_PER_BYTE = 8

parser = argparse.ArgumentParser(
    description="Измерение скорости скачивания данных по HTTP/HTTPS"
)
parser.add_argument(
    "url",
    help="HTTP- или HTTPS-адрес ресурса для скачивания"
)

args = parser.parse_args()
url_parts = urlsplit(args.url)

if url_parts.scheme not in ("http", "https") or not url_parts.hostname:
    parser.error("Укажите корректный HTTP- или HTTPS-адрес")

try:
    url_parts.port
except ValueError:
    parser.error("Некорректный номер порта в URL")

ssl_context = ssl.create_default_context(cafile=certifi.where())

total_bytes = 0
total_time = 0.0

for i in range(REQUEST_COUNT):
    print(
        f"\rВыполняется запрос {i + 1}/{REQUEST_COUNT}...", end="", flush=True)

    start_time = time.perf_counter()

    try:
        with urllib.request.urlopen(
            args.url,
            context=ssl_context,
            timeout=REQUEST_TIMEOUT
        ) as response:
            bytes_loaded = 0

            while chunk := response.read(CHUNK_SIZE):
                bytes_loaded += len(chunk)

    except urllib.error.HTTPError as error:
        print(f"Ошибка HTTP: {error.code} {error.reason}")
        raise SystemExit(1)

    except urllib.error.URLError as error:
        print(f"Ошибка соединения: {error.reason}")
        raise SystemExit(1)

    except TimeoutError:
        print(f"Превышено время ожидания ({REQUEST_TIMEOUT} секунд)")
        raise SystemExit(1)

    elapsed_time = time.perf_counter() - start_time

    total_bytes += bytes_loaded
    total_time += elapsed_time

print("\r" + " " * 40 + "\r", end="")

total_megabytes = total_bytes / BYTES_PER_MEGABYTE
print(f"Всего скачано: {total_megabytes:.3f} MB")

average_time = total_time / REQUEST_COUNT
print(f"Среднее время запроса: {average_time:.3f} секунд")

if total_time > 0:
    download_speed_mbps = (
        total_bytes * BITS_PER_BYTE
        / (total_time * BITS_PER_MEGABIT)
    )
else:
    download_speed_mbps = 0.0
print(f"Скорость скачивания: {download_speed_mbps:.3f} Мбит/с")
