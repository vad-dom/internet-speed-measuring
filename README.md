# Download Speed Measurement

Консольный скрипт на Python для измерения скорости скачивания данных по HTTP/HTTPS.

Выполняется 10 последовательных запросов к указанному URL, полностью скачивается ответ каждого запроса и рассчитывается среднее время запроса, общий объем полученных данных и средняя скорость скачивания.

## Требования

- Python 3.8 или новее (с `pip`).
- Git — для клонирования репозитория.
- Подключение к интернету.

## Установка и запуск

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/vad-dom/internet-speed-measuring.git
   ```

2. Перейдите в папку проекта:

   ```bash
   cd internet-speed-measuring
   ```

3. Установите зависимости:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Запустите скрипт, передав URL ресурса для скачивания:

   ```bash
   python download_speed.py "https://example.com"
   ```

Для просмотра справки используйте:

```bash
python download_speed.py --help
```
