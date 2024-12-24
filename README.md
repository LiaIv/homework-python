# To-Do API Server

## Инструкции по запуску

### 1. Установите зависимости
Создайте и активируйте виртуальное окружение, затем установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

### 2. Запустите сервер
Выполните команду:
```bash
python server.py
```
Сервер будет доступен по адресу [http://127.0.0.1:8000/tasks](http://127.0.0.1:8000/tasks).

**Примечание:** файл `tasks.txt` будет автоматически создан при добавлении первой задачи.

## Команды для проверки API

### 1. Добавление задачи
```bash
curl -X POST http://127.0.0.1:8000/tasks \
     -H "Content-Type: application/json" \
     -d '{"title": "Test Task", "priority": "high"}'
```

### 2. Получение списка задач
```bash
curl http://127.0.0.1:8000/tasks
```

### 3. Отметка задачи как выполненной
```bash
curl -X POST http://127.0.0.1:8000/tasks/1/complete
```

### 4. Проверка на 404 (задача не найдена)
Если задача с указанным ID не существует, сервер вернёт код 404.

**Пример:**
```bash
curl -X POST http://127.0.0.1:8000/tasks/999/complete
```