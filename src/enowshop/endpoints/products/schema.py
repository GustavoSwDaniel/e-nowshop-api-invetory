from typing import List, Optional

from pydantic import BaseModel, Field, validator

from enowshop.endpoints.helpers import int_to_float
from datetime import datetime


class CategorySchema(BaseModel):
    name: str
    uuid: str

    class Config:
        orm_mode = True


class CreateProductSchema(BaseModel):
    category: CategorySchema

    class Config:
        orm_mode = True


class ProductsSchema(BaseModel):
    uuid: str
    name: str
    description: str
    price: float
    market: int = 0
    unity: int
    image_url: str
    created_at: datetime
    category: List[CategorySchema]

    @validator('price')
    def price_to_float(cls, v):
        return int_to_float(v)

    class Config:
        orm_mode = True


class PaginateProductsSchema(BaseModel):
    total: int
    offset: int
    count: int
    data: List[ProductsSchema]


class ProductRegisterSchema(BaseModel):
    name: str
    description: str
    price: float
    market: int = 0
    unity: int
    image_url: str
    category_uuid: str


class UpdateProductSchema(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    market: Optional[int]
    unity: Optional[int]
    image_url: Optional[str]


class ProductsWithDiscountSchema(ProductsSchema):
    new_price: int

    class Config:
        orm_mode = True


class PaginateProductsWithPromotionsSchema(PaginateProductsSchema):
    data: List[ProductsWithDiscountSchema]