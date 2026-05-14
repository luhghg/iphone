from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_engine as engine  
from app.models.bd_models import Product, ProductVariant, User, ProductImage
from app.services.auth_services import verify_password
from app.core.config import settings 
from app.models.bd_models import Category

# 1. Логіка захисту адмінки
class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form.get("username"), form.get("password")

        async with AsyncSession(engine) as session:
            # Шукаємо юзера за іменем
            result = await session.execute(select(User).filter(User.username == username))
            user = result.scalar_one_or_none()

            # Перевірка: чи є юзер, чи він адмін і чи правильний пароль
            if user and user.role == "admin":
                if verify_password(password, user.hashed_password):
                    # Записуємо в сесію, що ми пройшли перевірку
                    request.session.update({"admin_user": username})
                    return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        # Перевірка при кожному переході по сторінках адмінки
        return "admin_user" in request.session

# 2. Налаштування відображення моделей
class UserAdmin(ModelView, model=User):
    name = "Користувач"
    name_plural = "Користувачі"
    icon = "fa-solid fa-user"
    
    # Використовуємо ТІЛЬКИ column_list. 
    # Все, що сюди не вписав (наприклад, hashed_password), і так не буде видно в таблиці.
    column_list = [User.id, User.username, User.email, User.role, User.is_active]
    
    column_searchable_list = [User.username, User.email]
    column_sortable_list = [User.id]

    # А ось для ФОРМИ редагування/створення треба окремо приховати пароль, 
    # щоб адмін випадково не затер хеш пустим рядком.
    form_excluded_columns = [User.hashed_password]


class CategoryAdmin(ModelView, model=Category):
    name = "Категорія"
    name_plural = "Категорії"
    icon = "fa-solid fa-list"
    
    column_list = [Category.id, Category.name, Category.slug, Category.created_at]
    column_searchable_list = [Category.name, Category.slug]
    column_sortable_list = [Category.id]


class ProductAdmin(ModelView, model=Product):
    name = "Продукт"
    name_plural = "Продукти"
    icon = "fa-solid fa-box"
    
    column_list = [Product.id, Product.name, Product.description, Product.is_active, Product.category_id, Product.created_at]
    form_columns = ["name", "description", "is_active", "category"]
    column_searchable_list = [Product.name, Product.description]
    column_sortable_list = [Product.id]


class ProductVariantAdmin(ModelView, model=ProductVariant):
    name = "Варіант продукту"
    name_plural = "Варіанти продуктів"
    icon = "fa-solid fa-boxes-stacked"
    
    column_list = [ProductVariant.id, ProductVariant.product_id, ProductVariant.price, ProductVariant.stock, ProductVariant.storage, ProductVariant.color]
    form_columns = ["product", "price", "stock", "storage", "color"]
    column_searchable_list = [ProductVariant.storage, ProductVariant.color]
    column_sortable_list = [ProductVariant.id]


class ProductImageAdmin(ModelView, model=ProductImage):
    name = "Фото продукту"
    name_plural = "Фото продуктів"
    icon = "fa-solid fa-images"

    column_list = [ProductImage.id, ProductImage.product_id, ProductImage.image_url, ProductImage.is_main, ProductImage.created_at]
    form_columns = ["product", "image_url", "is_main"]
    column_searchable_list = [ProductImage.product_id, ProductImage.image_url]
    column_sortable_list = [ProductImage.id]


# 3. Головна функція для підключення
def setup_admin(app, engine):
    # Створюємо бекенд авторизації (secret_key може бути будь-який рядок)
    auth_backend = AdminAuth(secret_key=settings.ADMIN_SECRET_KEY)
    
    # Створюємо адмінку з захистом
    admin = Admin(app, engine, authentication_backend=auth_backend)
    
    # Додаємо наші в’юхи
    admin.add_view(UserAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(ProductVariantAdmin)
    admin.add_view(ProductImageAdmin)

# Реєструємо їх
# admin.add_view(UserAdmin)

