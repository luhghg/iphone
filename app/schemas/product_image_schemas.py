from pydantic import BaseModel


class ProductImageCreate(BaseModel):
    product_id : int
    image_url: str
    is_main: bool = False


class ProductImageResponse(BaseModel):
    id: int
    product_id: int
    image_url: str
    is_main: bool

    model_config = {
        "from_attributes": True
        }
    

class ProductImageUpdate(BaseModel):
    image_url:  str | None = None
    is_main: bool | None = None
