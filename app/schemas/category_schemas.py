from pydantic import BaseModel, ConfigDict, model_validator
from slugify import slugify


class CategoryCreate(BaseModel):
    name: str | None = None  # Додав None, бо логіка передбачає створення name зі slug
    slug: str | None = None

    @model_validator(mode='after')
    def generate_slug(self) -> 'CategoryCreate':
        # В mode='after' працюємо безпосередньо з атрибутами self
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        
        elif not self.name and not self.slug:
            raise ValueError("Either name or slug must be provided")
        
        elif self.slug and not self.name:
            self.name = self.slug.replace('-', ' ').title()
        
        elif self.slug and self.name:
            expected_slug = slugify(self.name)
            if self.slug != expected_slug:
                # В Pydantic краще викидати ValueError/AssertionError всередині валідатора
                raise ValueError(f"Slug must be a valid slugified version of the name. Expected: {expected_slug}")
        
        return self

class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str

    model_config = ConfigDict(from_attributes = True)

class CategoryUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
