from src.disparo import Disparo


class DisparoCongelante(Disparo):
    def __init__(self, pos_x, pos_y, estado):
        super(DisparoCongelante, self).__init__(pos_x, pos_y, estado)
        self.poder_ataque = 8
        self.duracion_congelacion = 1000
