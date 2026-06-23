from pydantic import BaseModel, ConfigDict, UUID4

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    uuid: UUID4
    slug: str

    model_config = ConfigDict(from_attributes=True)