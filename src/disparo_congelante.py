import pygame
from src.disparo import Disparo
from src.configuracion import *


class DisparoCongelante(Disparo):
    def __init__(self, pos_x, pos_y, estado, dimensiones_vertical=(15, 25), dimensiones_horizontal=(25, 15)):
        dimensiones_congelacion = (100, 100)
        imagenes = {
            UP: [pygame.transform.scale(pygame.image.load("imagenes/jugador/violet_arrow_up.png"), dimensiones_vertical)],
            RIGHT: [pygame.transform.scale(pygame.image.load("imagenes/jugador/violet_arrow_right.png"), dimensiones_horizontal)],
            DOWN: [pygame.transform.scale(pygame.image.load("imagenes/jugador/violet_arrow_down.png"), dimensiones_vertical)],
            LEFT: [pygame.transform.scale(pygame.image.load("imagenes/jugador/violet_arrow_left.png"), dimensiones_horizontal)],
            ICE: [
                pygame.transform.scale(pygame.image.load("imagenes/jugador/ice_1.png"), dimensiones_congelacion),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/ice_2.png"), dimensiones_congelacion),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/ice_3.png"), dimensiones_congelacion),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/ice_4.png"), dimensiones_congelacion),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/ice_5.png"), dimensiones_congelacion),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/ice_6.png"), dimensiones_congelacion)
            ]
        }
        super(DisparoCongelante, self).__init__(imagenes=imagenes, pos_x=pos_x, pos_y=pos_y, estado=estado, velocidad=15)
        self.congelado = False
        self.duracion_congelacion = 1000
        self.tiempo_congelacion = 0
        self.poder_ataque = 8

    def dibujar(self, pantalla):
        if self.congelado:
            pantalla.blit(self.imagenes[self.estado][self.animacion], self.posicion)
            self.recorrer_imagenes(int(self.duracion_congelacion / len(self.imagenes[self.estado])))
        else:
            super(DisparoCongelante, self).dibujar(pantalla)

    def congelar(self):
        self.congelado = True
        self.tiempo_congelacion = pygame.time.get_ticks()
        self.estado = ICE
        self.animacion = 0
        px, py = self.posicion.centerx, self.posicion.centery
        self.posicion = self.imagenes[self.estado][self.animacion].get_rect()
        self.posicion.centerx = px
        self.posicion.centery = py

    def movimiento(self):
        if not self.congelado:
            super(DisparoCongelante, self).movimiento()
