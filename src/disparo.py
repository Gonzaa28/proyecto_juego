import pygame
from src.objeto_juego import ObjetoJuego
from src.configuracion import *


class Disparo(ObjetoJuego):
    def __init__(self, pos_x, pos_y, estado, dimensiones_vertical=(10, 25), dimensiones_horizontal=(25, 10), imagenes=None, velocidad=15, infinito=False):
        imagenes = imagenes or {
            UP: [pygame.transform.scale(pygame.image.load("imagenes/jugador/arrowup.png"), dimensiones_vertical)],
            RIGHT: [
                pygame.transform.scale(pygame.image.load("imagenes/jugador/arrowright.png"), dimensiones_horizontal)],
            DOWN: [pygame.transform.scale(pygame.image.load("imagenes/jugador/arrowdown.png"), dimensiones_vertical)],
            LEFT: [pygame.transform.scale(pygame.image.load("imagenes/jugador/arrowleft.png"), dimensiones_horizontal)]
        }
        super(Disparo, self).__init__(imagenes=imagenes, pos_x=pos_x, pos_y=pos_y, estado=estado, animacion=0,
                                      velocidad=velocidad, poder_ataque=4)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.infinito = infinito

    def movimiento(self):
        if self.estado == UP:
            self.mover_arriba()
        if self.estado == RIGHT:
            self.mover_derecha()
        if self.estado == DOWN:
            self.mover_abajo()
        if self.estado == LEFT:
            self.mover_izquierda()