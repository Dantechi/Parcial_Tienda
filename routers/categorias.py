"""
Rutas para gestionar las categorías de productos.
Ahora incluye la opción de reactivar categorías.
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
    categorias = session.exec(select(Categoria).where(Categoria.activa == True)).all()
    if not categorias:
        raise HTTPException(status_code=404, detail="No hay categorías activas.")
    return categorias

# ======================
# 🟢 OBTENER CATEGORÍA CON SUS PRODUCTOS
# ======================

from schemas import CategoriaConProductos  # ✅ importa el nuevo esquema

@router.get("/{categoria_id}", response_model=CategoriaConProductos)
def obtener_categoria_con_productos(categoria_id: int, session: Session = Depends(get_session)):
    """
    Retorna una categoría por su ID junto con sus productos relacionados.
    Incluye la relación 1:N en la respuesta.
    """
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    # Carga los productos asociados
    categoria.productos
    return categoria


# ======================
# 🟡 ACTUALIZAR CATEGORÍA
# ======================

@router.put("/{categoria_id}", response_model=CategoriaRead)
def actualizar_categoria(categoria_id: int, datos: CategoriaCreate, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
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

@router.patch("/{categoria_id}/desactivar", response_model=CategoriaRead)
def desactivar_categoria(categoria_id: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    categoria.activa = False
    for producto in categoria.productos:
        producto.activo = False
        session.add(producto)
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria

# ======================
# 🟢 REACTIVAR CATEGORÍA
# ======================

@router.patch("/{categoria_id}/reactivar", response_model=CategoriaRead)
def reactivar_categoria(categoria_id: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if categoria.activa:
        raise HTTPException(status_code=409, detail="La categoría ya está activa")
    categoria.activa = True
    for producto in categoria.productos:
        producto.activo = True
        session.add(producto)
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria
