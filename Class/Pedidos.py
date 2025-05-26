from Utils.tools import Tools, CustomException
from Utils.querys import Querys

class Pedidos:

    def __init__(self, db):
        self.db = db
        self.tools = Tools()
        self.querys = Querys(self.db)

    # Función para obtener los detalles de un pedido
    def consultar_pedido(self, data: dict):
        """ Api que realiza la consulta de los estados. """
        try:
            numero_pedido = int(data['numero_pedido'])
            
            pedido_detalles = self.querys.consultar_pedido(numero_pedido)

            # Retornamos la información.
            return self.tools.output(200, "Proceso exitoso.", pedido_detalles)

        except CustomException as e:
            print(f"Error al guardar solicitud: {e}")
            raise e
    
    # Función guardar masivo
    def actualizar_masivo(self, data: dict):
        """ Api que realiza la consulta de los estados. """
        try:
            numero_pedido = int(data['numero_pedido'])
            checkIndicadores = data['checkIndicadores']
            detalles = data["detalles"]
            
            if not detalles:
                raise CustomException("No se encontraron detalles para guardar.")
            
            if not checkIndicadores:
                for key in detalles:
                    self.querys.actualizar_fecha(numero_pedido, key)
                    
            if checkIndicadores:
                self.querys.actualizar_masivo_indicadores(numero_pedido, detalles[0]['nueva_fecha'])

            # Retornamos la información.
            return self.tools.output(200, "Proceso exitoso.")

        except CustomException as e:
            print(f"Error al actualizar masivo: {e}")
            raise e

    # Función para actualizar la fecha individual de un item de un pedido
    def actualizar_fecha_individual(self, data: dict):
        """ Api que realiza la consulta de los estados. """
        try:
            numero_pedido = int(data['numero_pedido'])
            checkIndicadores = data['checkIndicadores']
            item_detalle = data["item_detalle"]
            
            if not checkIndicadores:
                self.querys.actualizar_fecha(numero_pedido, item_detalle)
                
            if checkIndicadores:
                self.querys.actualizar_individual_indicadores(numero_pedido, item_detalle)

            # Retornamos la información.
            return self.tools.output(200, "Proceso exitoso.", item_detalle)

        except CustomException as e:
            print(f"Error al actualizar masivo: {e}")
            raise e
