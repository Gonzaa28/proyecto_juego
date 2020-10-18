import pygame

from src.item import Item
from src.configuracion import *


class Moneda(Item):
    def __init__(self, pos_x, pos_y, valor=1):
        imagenes = {
            QUIETO: [
                pygame.transform.scale(pygame.image.load("imagenes/items/coins_1.png"), (30, 30)),
                pygame.transform.scale(pygame.image.load("imagenes/items/coins_2.png"), (30, 30)),
                pygame.transform.scale(pygame.image.load("imagenes/items/coins_3.png"), (30, 30)),
                pygame.transform.scale(pygame.image.load("imagenes/items/coins_4.png"), (30, 30)),
                pygame.transform.scale(pygame.image.load("imagenes/items/coins_5.png"), (30, 30)),
                pygame.transform.scale(pygame.image.load("imagenes/items/coins_6.png"), (30, 30)),
                pygame.transform.scale(pygame.image.load("imagenes/items/coins_7.png"), (30, 30)),
                pygame.transform.scale(pygame.image.load("imagenes/items/coins_8.png"), (30, 30))
            ]
        }
        super(Moneda, self).__init__(pos_x, pos_y, imagenes)
        self.valor = valor

    def recoger(self, jugador):
        return jugador.add_coins(self.valor)
