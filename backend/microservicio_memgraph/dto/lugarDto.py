# ==============================
# Preparamos estructura de los datos del nodo lugar
# ==============================
class LugarDto:
    def __init__(self, id, name, tipo, estado, accesible, media=None, likes=None,
                 agua=None, electricidad=None, comedor=None, juegos=None):

        self.id = id
        self.name = name
        self.tipo = tipo
        self.estado = estado
        self.accesible = accesible
        self.media = media
        self.likes = likes

        # extras parque
        self.agua = agua
        self.electricidad = electricidad
        self.comedor = comedor
        self.juegos = juegos

    def toDict(self):
        return self.__dict__