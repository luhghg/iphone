from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(max_length=255)
    description: str


class ProductCreate(ProductBase):
    category_id: int 
    is_active: bool = True


class ProductResponse(ProductBase):
    id: int
    category_id: int
    is_active: bool

    model_config = ConfigDict(from_attributes = True) 


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = None
    category_id: int | None = None
    is_active: bool | None = None


