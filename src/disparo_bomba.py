import pygame

from src.disparo import Disparo
from src.configuracion import *


class DisparoBomba(Disparo):
    def __init__(self, pos_x, pos_y, estado, dimensiones_vertical=(15, 25), dimensiones_horizontal=(25, 15)):
        dimensiones_explosion = (120, 120)
        imagenes = {
            UP: [pygame.transform.scale(pygame.image.load("imagenes/jugador/arribaFlechaRoja.png"), dimensiones_vertical)],
            RIGHT: [
                pygame.transform.scale(pygame.image.load("imagenes/jugador/derechaFlechaRoja.png"), dimensiones_horizontal)],
            DOWN: [pygame.transform.scale(pygame.image.load("imagenes/jugador/abajoFlechaRoja.png"), dimensiones_vertical)],
            LEFT: [pygame.transform.scale(pygame.image.load("imagenes/jugador/izquierdaFlechaRoja.png"), dimensiones_horizontal)],
            BOOM: [
                pygame.transform.scale(pygame.image.load("imagenes/jugador/boom_1.png"), dimensiones_explosion),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/boom_2.png"), dimensiones_explosion),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/boom_3.png"), dimensiones_explosion),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/boom_4.png"), dimensiones_explosion),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/boom_5.png"), dimensiones_explosion),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/boom_6.png"), dimensiones_explosion),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/boom_7.png"), dimensiones_explosion)
            ]
        }
        super(DisparoBomba, self).__init__(imagenes=imagenes, pos_x=pos_x, pos_y=pos_y, estado=estado, velocidad=15)

        self.explotado = False
        self.duracion_explosion = 1500
        self.tiempo_detonacion = 0
        self.poder_ataque = 15

    def dibujar(self, pantalla):
        if self.explotado:
            pantalla.blit(self.imagenes[self.estado][self.animacion], self.posicion)
            self.recorrer_imagenes(int(self.duracion_explosion/len(self.imagenes[self.estado])))
        else:
            super(DisparoBomba, self).dibujar(pantalla)

    def detonar(self):
        self.explotado = True
        self.tiempo_detonacion = pygame.time.get_ticks()
        self.estado = BOOM
        self.animacion = 0
        px, py = self.posicion.centerx, self.posicion.centery
        self.posicion = self.imagenes[self.estado][self.animacion].get_rect()
        self.posicion.centerx = px
        self.posicion.centery = py

    def movimiento(self):
        if not self.explotado:
            super(DisparoBomba, self).movimiento()