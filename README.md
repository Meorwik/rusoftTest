## Установка

1. **Клонируем репозиторий**

```bash
git clone <repo_url>
cd <repo_folder>
```

2. **Создаем и активируем виртуальное окружение**

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. **Устанавливаем зависимости из pyproject.toml**

```bash
pip install .
# или если используете poetry
poetry install

# Если используем uv:

pip install uv
uv pip install . 
```

4. **Настройка подключения к базе**

⚠️ Убедитесь, что база уже создана на вашей машине.

Данные для подключения к БД хранятся в properties.yaml:
Создайте этот файл в директории проекта и пропишите данные

вот в таком формате:

```yaml
postgres:
  host: localhost
  port: 5432
  user: meorwik
  password: 123
  database: rusofttest
```

---

# Инициализация базы данных

1. **Применяем миграции Alembic для создания таблиц**

```bash
alembic upgrade head
```

2. **Опционально: если появляются ошибки прав для схемы public:**

```sql
ALTER SCHEMA public OWNER TO vash_uzer_bd;
```


---

# Запуск проекта

**Запуск FastAPI сервера:**

```bash
uv pip install . && uvicorn rusoft.main:app --reload
```

# [Swagger](http://localhost:8000/docs)
