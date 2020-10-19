import pygame

from src.item import Item
from src.configuracion import *


class Corazon(Item):
    def __init__(self, pos_x, pos_y):
        imagen = {
            QUIETO: [pygame.transform.scale(pygame.image.load("imagenes/items/heart.png"), (30, 30))],
        }
        super(Corazon, self).__init__(pos_x, pos_y, imagen)
        self.curacion = 10

    def recoger(self, jugador):
        return jugador.curarse(self.curacion)
