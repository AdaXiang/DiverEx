# ==============================
# DTO Comentario
# ==============================
class ComentarioDto:
    def __init__(self, id, mensaje, ranking, fecha, lugar=None, usuario=None):
        self.id = id
        self.mensaje = mensaje
        self.ranking = ranking
        self.fecha = fecha
        self.lugar = lugar
        self.usuario = usuario

    def toDict(self):
        return {
            "id": self.id,
            "mensaje": self.mensaje,
            "ranking": self.ranking,
            "fecha": self.fecha,
            "lugar": self.lugar,
            "usuario": self.usuario
        }