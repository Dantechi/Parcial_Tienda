"""
Esquemas Pydantic para validación de datos en la Tienda Online.
Definen la estructura de entrada y salida de los endpoints.
"""

from typing import Optional, List
from pydantic import BaseModel, Field

# ======================
# 🏷️ CATEGORÍA
# ======================

class CategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=2, description="Nombre único de la categoría")
    descripcion: Optional[str] = Field(None, description="Descripción breve de la categoría")


class CategoriaCreate(CategoriaBase):
    """Esquema usado para crear una categoría"""
    pass


class CategoriaRead(CategoriaBase):
    """Esquema usado para leer información de una categoría"""
    id: int
    activa: bool

    class Config:
        orm_mode = True


class CategoriaUpdate(BaseModel):
    """Esquema para actualizar una categoría existente"""
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activa: Optional[bool] = None


# ======================
# 📦 PRODUCTO
# ======================

class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=2)
    descripcion: Optional[str] = None
    precio: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)
    activo: bool = Field(default=True)


class ProductoCreate(ProductoBase):
    """Esquema para crear producto"""
    categoria_id: int


class ProductoRead(ProductoBase):
    """Esquema para leer producto con su categoría"""
    id: int
    categoria_id: int

    class Config:
        orm_mode = True


class ProductoUpdate(BaseModel):
    """Esquema para actualizar producto"""
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    activo: Optional[bool] = None
    categoria_id: Optional[int] = None
