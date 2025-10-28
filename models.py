"""
Modelos SQLModel para la Tienda Online.
Define las entidades principales: Categoria y Producto.
Relación 1:N → Una categoría tiene muchos productos.
"""

from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# ======================
# 🏷️ MODELO CATEGORÍA
# ======================

class Categoria(SQLModel, table=True):
    """
    Representa una categoría de productos.
    Cada categoría puede tener múltiples productos.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True, nullable=False)
    descripcion: Optional[str] = None
    activa: bool = Field(default=True)

    # Relación 1:N con Producto
    productos: List["Producto"] = Relationship(back_populates="categoria")


# ======================
# 📦 MODELO PRODUCTO
# ======================

class Producto(SQLModel, table=True):
    """
    Representa un producto dentro de la tienda.
    Cada producto pertenece a una categoría.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False)
    descripcion: Optional[str] = None
    precio: float = Field(gt=0, description="Precio del producto, debe ser mayor que 0")
    stock: int = Field(default=0, ge=0, description="Cantidad disponible en inventario")
    activo: bool = Field(default=True)

    # Relación con categoría
    categoria_id: int = Field(foreign_key="categoria.id")
    categoria: Optional[Categoria] = Relationship(back_populates="productos")
