from pydantic import BaseModel, ConfigDict


class ProductVariantCreate(BaseModel):
    product_id: int
    price: float
    stock: int = 0
    storage: str | None = None
    color: str | None = None


class ProductVariantResponse(BaseModel):
    id: int
    product_id: int
    price: float
    stock: int
    storage: str | None
    color: str | None

    model_config = ConfigDict(from_attributes = True) 


class ProductVariantUpdate(BaseModel):
    price: float | None = None
    stock: int | None = None
    storage: str | None = None
    color: str | None = None

