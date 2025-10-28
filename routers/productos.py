"""
Rutas para la gestión de productos.
Incluye creación con validaciones de negocio.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from db import get_session
from models import Producto, Categoria
from schemas import ProductoCreate, ProductoRead

router = APIRouter(prefix="/productos", tags=["Productos"])


# ======================
# 🟢 CREAR PRODUCTO
# ======================

@router.post("/", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate, session: Session = Depends(get_session)):
    """
    Crea un nuevo producto validando:
    - Que exista la categoría asociada.
    - Que el stock sea mayor o igual a 0.
    - Que el precio sea positivo.
    """

    # Verificar existencia de categoría
    categoria = session.get(Categoria, producto.categoria_id)
    if not categoria or not categoria.activa:
        raise HTTPException(status_code=404, detail="Categoría no encontrada o inactiva")

    # Validar reglas de negocio
    if producto.stock < 0:
        raise HTTPException(status_code=400, detail="El stock no puede ser negativo")
    if producto.precio <= 0:
        raise HTTPException(status_code=400, detail="El precio debe ser mayor que cero")

    nuevo_producto = Producto(
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio,
        stock=producto.stock,
        categoria_id=producto.categoria_id,
    )

    session.add(nuevo_producto)
    session.commit()
    session.refresh(nuevo_producto)
    return nuevo_producto
