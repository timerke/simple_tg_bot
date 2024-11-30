# simple_tg_bot
Простой Telegram bot для сотрудников компании.

## Запуск

1. Установите необходимые зависимости:

   ```bash
   python -m venv venv
   venv\Scripts\python -m pip install --upgrade pip
   venv\Scripts\python -m pip install -r requirements.txt
   ```

2. Запишите API токен Вашего Telegram бота в конфигурационный файл **config.ini**:

   ```
   [GENERAL]
   TOKEN = 
   ```

3. Запустите бота:

   ```bash
   venv\Scripts\python run.py
   ```

   
