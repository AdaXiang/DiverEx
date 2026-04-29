# ==============================
# Preparamos estructura de los datos del nodo usuario
# ==============================
class UsuarioDto:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def toDict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }