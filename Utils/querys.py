from Utils.tools import Tools, CustomException
from sqlalchemy import text, or_, case
from sqlalchemy.sql import select
from collections import defaultdict
from datetime import datetime

class Querys:

    def __init__(self, db):
        self.db = db
        self.tools = Tools()
        self.query_params = dict()

    # Query para validar el año de la proyección si existe.
    def consultar_pedido(self, numero_pedido: int):

        try:
            result = dict()
            detalles = list()
            sql = """
                SELECT dp.nit, t.nombres as tercero, dp.fecha, dlp.codigo, 
                r.descripcion as nombre_producto, dlp.cantidad, dlp.valor_unitario,
                dlp.adicional as fecha_entrega, dlp.id, dlp.seq
                FROM documentos_ped dp
                INNER JOIN terceros t ON t.nit = dp.nit
                INNER JOIN documentos_lin_ped dlp ON dlp.numero = dp.numero
                INNER JOIN referencias r ON r.codigo = dlp.codigo
                WHERE dp.sw = 1 AND dlp.sw = 1 AND dp.numero = :numero_pedido
            """

            query = self.db.execute(text(sql), {"numero_pedido": numero_pedido}).fetchall()
            
            if not query:
                return []

            nit = query[0][0]
            tercero = query[0][1]
            fecha = query[0][2]
            for key in query:
                detalles.append({
                    "codigo": key[3],
                    "nombre_producto": key[4],
                    "cantidad": key[5],
                    "valor_unitario": self.tools.formatear_pesos_colombianos(key[6]) if key[6] else 0,
                    "fecha_entrega": str(key[7]),
                    "nueva_fecha": str(key[7]),
                    "id": key[8],
                    "seq": key[9]
                })

            result = {
                "nit": nit,
                "tercero": tercero,
                "fecha": self.tools.format_date(str(fecha), "%Y-%m-%d %H:%M:%S", "%Y-%m-%d") if fecha else '',
                "detalles": detalles
            }
            

            return result
  
        except Exception as ex:
            print(str(ex))
            raise CustomException(str(ex))
        finally:
            self.db.close()

    # Query para guardar masivo
    def actualizar_fecha(self, numero_pedido: int, detalle: dict):
        try:
            sql = """
                UPDATE documentos_lin_ped
                SET adicional = :nueva_fecha
                WHERE id = :id AND numero = :numero_pedido AND sw = 1 AND seq = :seq
            """
            self.db.execute(
                text(sql), 
                {
                    "nueva_fecha": datetime.strptime(str(detalle["nueva_fecha"]), "%Y-%m-%d").strftime("%m-%d-%Y") if detalle["nueva_fecha"] else '', 
                    "id": detalle["id"], 
                    "numero_pedido": numero_pedido, 
                    "seq": detalle["seq"]
                }
            )
            self.db.commit()
            return True
        except Exception as ex:
            print(str(ex))
            raise CustomException(str(ex))
        finally:
            self.db.close()

    # Procedure para actualizar fechas y otras tablas cuando indicadores están marcados
    def actualizar_masivo_indicadores(self, numero_pedido: int, nueva_fecha: str):
        try:
            # Convertir la fecha a formato MM-DD-YYYY si viene en YYYY-MM-DD
            fecha_convertida = datetime.strptime(nueva_fecha, "%Y-%m-%d").strftime("%m-%d-%Y")

            sql = text("""
                EXEC dbo.sp_actualizar_fecha_entrega_pedido 
                    @pedido = :pedido, 
                    @nueva_fecha = :nueva_fecha
            """)

            result = self.db.execute(sql, {
                "pedido": numero_pedido,
                "nueva_fecha": fecha_convertida
            })

            # Si quieres capturar lo que devuelve el SP
            resumen = result.fetchall()

            self.db.commit()
            return True  # O True si no te interesa el resumen

        except Exception as ex:
            print(f"Error ejecutando SP: {ex}")
            raise CustomException(str(ex))
        finally:
            self.db.close()

    # Procedure para actualizar la fecha individual de un item de un pedido
    def actualizar_individual_indicadores(self, numero_pedido: int, item_detalle: dict):
        try:
            print(f"item_detalle: {item_detalle}")
            sql = text("""
                EXEC dbo.sp_actualizar_fecha_entrega_pedido_individual 
                @pedido = :pedido, 
                @nueva_fecha = :nueva_fecha, 
                @codigo = :codigo, 
                @seq = :seq
            """)

            result = self.db.execute(sql, {
                "pedido": numero_pedido,
                "nueva_fecha": datetime.strptime(item_detalle['nueva_fecha'], "%Y-%m-%d").strftime("%m-%d-%Y"),
                "codigo": item_detalle['codigo'],
                "seq": item_detalle['seq']
            })

            self.db.commit()
            return True

        except Exception as ex:
            print(f"Error ejecutando SP: {ex}")
            raise CustomException(str(ex))
        finally:
            self.db.close()
