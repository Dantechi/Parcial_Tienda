"""
Rutas para gestionar las categorías de productos.
Incluye creación y listado de categorías activas.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from db import get_session
from models import Categoria
from schemas import CategoriaCreate, CategoriaRead

router = APIRouter(prefix="/categorias", tags=["Categorías"])


# ======================
# 🟢 CREAR CATEGORÍA
# ======================

@router.post("/", response_model=CategoriaRead, status_code=status.HTTP_201_CREATED)
def crear_categoria(categoria: CategoriaCreate, session: Session = Depends(get_session)):
    """
    Crea una nueva categoría si el nombre no existe.
    """
    # Verificar unicidad del nombre
    existente = session.exec(select(Categoria).where(Categoria.nombre == categoria.nombre)).first()
    if existente:
        raise HTTPException(status_code=409, detail="Ya existe una categoría con ese nombre.")

    nueva_categoria = Categoria(nombre=categoria.nombre, descripcion=categoria.descripcion)
    session.add(nueva_categoria)
    session.commit()
    session.refresh(nueva_categoria)
    return nueva_categoria


# ======================
# 🟢 LISTAR CATEGORÍAS ACTIVAS
# ======================

@router.get("/", response_model=list[CategoriaRead])
def listar_categorias_activas(session: Session = Depends(get_session)):
    """
    Retorna todas las categorías activas en el sistema.
    """
    categorias = session.exec(select(Categoria).where(Categoria.activa == True)).all()
    return categorias

# ======================
# 🟢 OBTENER CATEGORÍA CON SUS PRODUCTOS
# ======================

@router.get("/{categoria_id}", response_model=CategoriaRead)
def obtener_categoria_con_productos(categoria_id: int, session: Session = Depends(get_session)):
    """
    Retorna una categoría por su ID junto con sus productos relacionados.
    """
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    # Carga los productos (relación 1:N)
    categoria.productos  # Esto carga los productos relacionados
    return categoria

# ======================
# 🟡 ACTUALIZAR CATEGORÍA
# ======================

@router.put("/{categoria_id}", response_model=CategoriaRead)
def actualizar_categoria(categoria_id: int, datos: CategoriaCreate, session: Session = Depends(get_session)):
    """
    Actualiza el nombre o descripción de una categoría existente.
    No permite duplicar nombres.
    """
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    # Verificar nombre único (si se cambia)
    if categoria.nombre != datos.nombre:
        existente = session.exec(select(Categoria).where(Categoria.nombre == datos.nombre)).first()
        if existente:
            raise HTTPException(status_code=409, detail="Ya existe otra categoría con ese nombre.")

    categoria.nombre = datos.nombre
    categoria.descripcion = datos.descripcion

    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


# ======================
# 🔴 DESACTIVAR CATEGORÍA
# ======================

@router.delete("/{categoria_id}", response_model=CategoriaRead)
def desactivar_categoria(categoria_id: int, session: Session = Depends(get_session)):
    """
    Desactiva una categoría en lugar de eliminarla físicamente.
    Si se desactiva, todos sus productos también se desactivan (cascada lógica).
    """
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    categoria.activa = False

    # Desactivar también todos sus productos
    for producto in categoria.productos:
        producto.activo = False
        session.add(producto)

    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria
