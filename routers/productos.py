"""
Rutas para la gestión de productos.
Incluye creación con validaciones de negocio.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from db import get_session
from models import Producto, Categoria
from schemas import ProductoCreate, ProductoRead
from typing import List, Optional  # ✅ IMPORTACIÓN CORREGIDA
from pydantic import BaseModel

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


# ==============================
# 🔍 LISTAR PRODUCTOS CON FILTROS
# ==============================

@router.get("/", response_model=List[ProductoRead])
def listar_productos(
    stock_min: Optional[int] = None,
    stock_max: Optional[int] = None,
    precio_min: Optional[float] = None,
    precio_max: Optional[float] = None,
    categoria_id: Optional[int] = None,
    session: Session = Depends(get_session)
):
    """
    Retorna una lista de productos activos con filtros opcionales:
    - stock_min, stock_max → rango de stock
    - precio_min, precio_max → rango de precio
    - categoria_id → filtrar por categoría específica
    """
    query = select(Producto).where(Producto.activo == True)

    if stock_min is not None:
        query = query.where(Producto.stock >= stock_min)
    if stock_max is not None:
        query = query.where(Producto.stock <= stock_max)
    if precio_min is not None:
        query = query.where(Producto.precio >= precio_min)
    if precio_max is not None:
        query = query.where(Producto.precio <= precio_max)
    if categoria_id is not None:
        query = query.where(Producto.categoria_id == categoria_id)

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


# ======================
# ⚙️ ACTUALIZAR PRODUCTO
# ======================

@router.put("/{producto_id}", response_model=ProductoRead)
def actualizar_producto(producto_id: int, datos: ProductoCreate, session: Session = Depends(get_session)):
    """
    Actualiza un producto existente validando:
    - Que el nuevo stock no sea negativo.
    - Que el precio sea positivo.
    - Que la categoría exista y esté activa.
    """
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Validar categoría
    categoria = session.get(Categoria, datos.categoria_id)
    if not categoria or not categoria.activa:
        raise HTTPException(status_code=404, detail="Categoría no encontrada o inactiva")

    # Validaciones de negocio
    if datos.stock < 0:
        raise HTTPException(status_code=400, detail="El stock no puede ser negativo")
    if datos.precio <= 0:
        raise HTTPException(status_code=400, detail="El precio debe ser mayor que cero")

    # Actualizar campos
    producto.nombre = datos.nombre
    producto.descripcion = datos.descripcion
    producto.precio = datos.precio
    producto.stock = datos.stock
    producto.categoria_id = datos.categoria_id

    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


# ==========================
# 🧹 DESACTIVAR UN PRODUCTO
# ==========================

@router.patch("/{producto_id}/desactivar", response_model=ProductoRead)
def desactivar_producto(producto_id: int, session: Session = Depends(get_session)):
    """
    Desactiva un producto (DELETE lógico).
    No se elimina de la base de datos, solo se marca como inactivo.
    """
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if not producto.activo:
        raise HTTPException(status_code=409, detail="El producto ya está inactivo")

    producto.activo = False
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


# =======================================
# 📦 RESTAR STOCK (GESTIONAR COMPRA)
# =======================================

class CompraRequest(BaseModel):
    cantidad: int


@router.patch("/{producto_id}/comprar", response_model=ProductoRead)
def comprar_producto(producto_id: int, data: CompraRequest, session: Session = Depends(get_session)):
    """
    Permite comprar un producto, restando del stock la cantidad indicada.
    Valida que el stock no quede en negativo.
    """
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if not producto.activo:
        raise HTTPException(status_code=400, detail="No se puede comprar un producto inactivo")

    if data.cantidad <= 0:
        raise HTTPException(status_code=400, detail="La cantidad debe ser mayor que cero")

    if producto.stock < data.cantidad:
        raise HTTPException(status_code=400, detail="Stock insuficiente para la compra")

    producto.stock -= data.cantidad
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto
