from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from Class.Pedidos import Pedidos
from Utils.decorator import http_decorator
from Config.db import get_db

pedidos_router = APIRouter()

@pedidos_router.post('/consultar_pedido', tags=["Pedidos"], response_model=dict)
@http_decorator
def consultar_pedido(request: Request, db: Session = Depends(get_db)):
    data = getattr(request.state, "json_data", {})
    response = Pedidos(db).consultar_pedido(data)
    return response

@pedidos_router.post('/actualizar_masivo', tags=["Pedidos"], response_model=dict)
@http_decorator
def actualizar_masivo(request: Request, db: Session = Depends(get_db)):
    data = getattr(request.state, "json_data", {})
    response = Pedidos(db).actualizar_masivo(data)
    return response

@pedidos_router.post('/actualizar_fecha_individual', tags=["Pedidos"], response_model=dict)
@http_decorator
def actualizar_fecha_individual(request: Request, db: Session = Depends(get_db)):
    data = getattr(request.state, "json_data", {})
    response = Pedidos(db).actualizar_fecha_individual(data)
    return response
