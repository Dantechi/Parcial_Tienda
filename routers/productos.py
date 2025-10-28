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

# ======================
# 🔍 LISTAR PRODUCTOS CON FILTROS
# ======================

from typing import Optional

@router.get("/", response_model=list[ProductoRead])
def listar_productos(
    session: Session = Depends(get_session),
    categoria_id: Optional[int] = None,
    stock_min: Optional[int] = None,
    precio_max: Optional[float] = None,
    activos: Optional[bool] = True
):
    """
    Lista productos con filtros opcionales:
    - categoria_id → filtra por categoría
    - stock_min → productos con stock mayor o igual
    - precio_max → productos con precio menor o igual
    - activos → True (por defecto) para ver solo los activos
    """
    query = select(Producto)

    # Filtros dinámicos
    if categoria_id:
        query = query.where(Producto.categoria_id == categoria_id)
    if stock_min is not None:
        query = query.where(Producto.stock >= stock_min)
    if precio_max is not None:
        query = query.where(Producto.precio <= precio_max)
    if activos is not None:
        query = query.where(Producto.activo == activos)

    productos = session.exec(query).all()
    return productos

# ======================
# 🔁 OBTENER PRODUCTO CON SU CATEGORÍA
# ======================

@router.get("/{producto_id}", response_model=ProductoRead)
def obtener_producto(producto_id: int, session: Session = Depends(get_session)):
    """
    Retorna un producto por ID junto con su categoría asociada.
    """
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Accede a la categoría para asegurar que se incluya en la respuesta
    producto.categoria
    return producto
