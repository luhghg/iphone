# iPhone Store API

REST API для інтернет-магазину смартфонів. Побудовано на FastAPI з асинхронною архітектурою, Redis кешуванням та задеплоєно на Railway.

**Live:** https://iphone-production-4797.up.railway.app/docs

---

## Стек

| Технологія | Призначення |
|---|---|
| FastAPI | Web framework |
| PostgreSQL + asyncpg | База даних |
| SQLAlchemy 2.0 (async) | ORM |
| Alembic | Міграції |
| Redis | Кешування |
| JWT (python-jose) | Аутентифікація |
| Argon2 | Хешування паролів |
| SQLAdmin | Адмін панель |
| Docker | Контейнеризація |
| Railway | Деплой |
| GitHub Actions | CI/CD |
| pytest + httpx | Тестування |

---

## Функціонал

- **Auth** — реєстрація, логін, JWT токени, ролі (user/admin)
- **Продукти** — CRUD, пошук по назві, фільтр по категорії
- **Варіанти продуктів** — різні кольори, обʼєми памʼяті, ціни
- **Корзина** — додавання, оновлення кількості, очищення
- **Замовлення** — оформлення з корзини, відстеження статусу, перевірка stock
- **Redis кеш** — кешування списку продуктів і окремих продуктів по id
- **Адмін панель** — `/admin` з управлінням всіма моделями

---

## Архітектура

```
app/
├── routers/        # HTTP ендпоінти
├── services/       # Бізнес логіка
├── repositories/   # Запити до БД
├── schemas/        # Pydantic моделі
├── models/         # SQLAlchemy моделі
└── core/           # Config, Redis, Auth, Admin
```

Три шари: **Router → Service → Repository**. Кожен відповідає за своє.

---

## Запуск локально

```bash
git clone https://github.com/luhghg/iphone.git
cd iphone

# Запусти через Docker
docker compose up
```

Swagger доступний на `http://localhost:8080/docs`

---

## Тести

```bash
pytest tests/ -v
```

13 тестів покривають auth, cart і orders. CI запускається автоматично при кожному push через GitHub Actions.

---

## Redis кешування

Продукти кешуються з TTL 1 година:
- `products:all` — список всіх продуктів
- `product:{id}` — окремий продукт

При створенні/оновленні/видаленні продукту кеш інвалідується автоматично.
