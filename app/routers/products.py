from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from app.schemas import ProductCreate, ProductUpdate, ProductResponse
from app.database import db

router = APIRouter(prefix="/products", tags=["Productos"])


@router.get("/", response_model=List[ProductResponse], summary="Obtener lista de productos")
def get_products(
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    min_price: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Precio máximo"),
    search: Optional[str] = Query(None, description="Buscar por nombre o descripción"),
    skip: int = Query(0, ge=0, description="Número de elementos a omitir"),
    limit: int = Query(100, ge=1, le=500, description="Límite de elementos a retornar")
):
    """
    Recupera una lista de productos con soporte para filtrado por categoría, rango de precios,
    búsqueda por texto y paginación.
    """
    return db.get_all(
        category=category,
        min_price=min_price,
        max_price=max_price,
        search=search,
        skip=skip,
        limit=limit
    )


@router.get("/{product_id}", response_model=ProductResponse, summary="Obtener producto por ID")
def get_product(product_id: int):
    """
    Obtiene los detalles de un producto por su ID único.
    """
    product = db.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {product_id} no encontrado"
        )
    return product


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo producto"
)
def create_product(product_in: ProductCreate):
    """
    Crea un nuevo producto en el inventario validando los datos requeridos.
    """
    return db.create(product_in)


@router.put("/{product_id}", response_model=ProductResponse, summary="Actualización completa de producto")
def update_product(product_id: int, product_in: ProductCreate):
    """
    Actualiza completamente un producto existente. Reemplaza todos los campos.
    """
    updated = db.update(product_id, ProductUpdate(**product_in.model_dump()), partial=False)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {product_id} no encontrado"
        )
    return updated


@router.patch("/{product_id}", response_model=ProductResponse, summary="Actualización parcial de producto")
def patch_product(product_id: int, product_in: ProductUpdate):
    """
    Actualiza uno o varios campos de un producto existente.
    """
    updated = db.update(product_id, product_in, partial=True)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {product_id} no encontrado"
        )
    return updated


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar producto")
def delete_product(product_id: int):
    """
    Elimina un producto del inventario por su ID.
    """
    success = db.delete(product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {product_id} no encontrado"
        )
    return None
