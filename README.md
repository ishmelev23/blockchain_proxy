# BlockchainProxyService

## Установка
```
git clone https://github.com/ishmelev23/blockchain_proxy
cd blockhain_proxy
virtualenv .venv -p python3
. .venv/bin/activate
pip install -r requirements.pip

touch settings_local.py settings_local_tests.py
```

## Пример локальных настроек
```
import os

DEBUG = True

API_ENDPOINT = '/api/v1/'

DB_URL = 'mysql://trxhandler_admin:changeme@127.0.0.1:3306/trxhandler'
NODE_URL = 'https://ropsten.infura.io/v3/[api_key]'

ADDRESS = 'Your address'
PRIVATE_KEY = 'Your private key'

GAS_PRICE = 4

WATCHER_PROCESS_COUNT = 4
WATCHER_SLEEP_TIME = 5

PUBLISHER_PROCESS_COUNT = 4
PUBLISHER_SLEEP_TIME = 5

LOGGING_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
LOGGING_TYPES = ['console']

```

## Запуск
```
python3 init_db.py # Инициализация базы данных
python3 app.py # Запуск development сервера
python3 worker.py start --name publisher # Запуск сервиса публикации транзакций
python3 worker.py start --name watcher # Запуск сервиса отслеживания статуса транзакций
```

## Запуск тестов
```
TESTING=1 python3 init_db.py # TESTING=1 указывает подтягивать тестовые настройки
TESTING=1 python3 -m unittest tests.api.transactions
```
