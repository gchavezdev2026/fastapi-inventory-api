from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del producto")
    description: Optional[str] = Field(None, max_length=500, description="Descripción detallada del producto")
    price: float = Field(..., gt=0, description="Precio unitario, debe ser mayor que 0")
    stock: int = Field(..., ge=0, description="Cantidad en stock, debe ser mayor o igual a 0")
    category: str = Field(..., min_length=1, max_length=50, description="Categoría del producto")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Nombre del producto")
    description: Optional[str] = Field(None, max_length=500, description="Descripción del producto")
    price: Optional[float] = Field(None, gt=0, description="Precio unitario (mayor a 0)")
    stock: Optional[int] = Field(None, ge=0, description="Cantidad en stock (mayor o igual a 0)")
    category: Optional[str] = Field(None, min_length=1, max_length=50, description="Categoría del producto")


class ProductResponse(ProductBase):
    id: int = Field(..., description="Identificador único del producto")
    created_at: datetime = Field(..., description="Fecha de creación")
    updated_at: datetime = Field(..., description="Fecha de última actualización")

    model_config = ConfigDict(from_attributes=True)
