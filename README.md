## Как запустить проект

1. **Клонируйте репозиторий**:

   ```bash
   git clone https://github.com/javoxirone/text-analyzer.git
   cd text-analyzer
   ```

2. **Создайте виртуальное окружение (опционально, но желательно)**:

   ```bash
   python -m venv env
   source env/bin/activate        # для Linux/Mac
   env\Scripts\activate           # для Windows
   ```

3. **Установите зависимости**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Выполните миграции базы данных**:

   ```bash
   python manage.py migrate
   ```

5. **Запустите сервер разработки**:

   ```bash
   python manage.py runserver
   ```

6. **Откройте приложение в браузере**:

   Перейдите по ссылке: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
