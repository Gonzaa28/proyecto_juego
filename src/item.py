from src.objeto_juego import ObjetoJuego
from src.configuracion import *


class Item(ObjetoJuego):
    def __init__(self, pos_x, pos_y, imagenes):
        super(Item, self).__init__( imagenes, pos_x, pos_y, estado=QUIETO, animacion=0, velocidad=0)

    def recoger(self, jugador):
        pass

    def dibujar(self, pantalla):
        super(Item, self).dibujar(pantalla)
        self.recorrer_imagenes()