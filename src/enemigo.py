from random import randint
import pygame
from src.objeto_juego import ObjetoJuego
from src.configuracion import *
from src.funciones import posicion_aleatoria_radio
from src.moneda import *
from src.corazon import *


class Enemigo(ObjetoJuego):
    def __init__(self, pos_x=int(ANCHO / 2), pos_y=0, dimensiones=(45, 45)):
        imagenes = {
            UP: [
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/up1.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/up2.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/up3.png"), dimensiones),
                # pygame.transform.scale(pygame.image.load("imagenes/enemigo/up4.png"), dimensiones),
                # pygame.transform.scale(pygame.image.load("imagenes/enemigo/up5.png"), dimensiones)
            ],
            RIGHT: [
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/right1.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/right2.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/right3.png"), dimensiones),
                # pygame.transform.scale(pygame.image.load("imagenes/enemigo/right4.png"), dimensiones)
            ],
            DOWN: [
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/down1.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/down2.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/down3.png"), dimensiones),
                # pygame.transform.scale(pygame.image.load("imagenes/enemigo/down4.png"), dimensiones),
                # pygame.transform.scale(pygame.image.load("imagenes/enemigo/down5.png"), dimensiones)
            ],
            LEFT: [
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/left1.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/left2.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/left3.png"), dimensiones),
                # pygame.transform.scale(pygame.image.load("imagenes/enemigo/left4.png"), dimensiones)
            ],
            PUNCH_RIGHT: [
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/punchright1.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/punchright2.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/punchright3.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/punchright4.png"), dimensiones)
            ],
            PUNCH_UP: [
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/punchup1.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/punchup2.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/punchup3.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/punchup4.png"), dimensiones)
            ],
            PUNCH_DOWN: [
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/punchdown1.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/punchdown2.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/punchdown3.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/punchdown4.png"), dimensiones)
            ],
            PUNCH_LEFT: [
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/punchleft1.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/punchleft2.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/punchleft3.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/enemigo/punchleft4.png"), dimensiones)
            ],
        }
        super(Enemigo, self).__init__(imagenes=imagenes, pos_x=pos_x, pos_y=pos_y, estado=0, animacion=0,
                                      velocidad=2, cooldown_ataque=500, vida_inicial=60)
        self.golpeado = False
        self.ultima_congelacion = pygame.time.get_ticks()
        self.duracion_congelacion = 1000

    def movimiento_trayectoria(self, pos_jugador):
        if self.esta_congelado():
            return
        else:
            self.caminando = True
        diferencia_x = abs(self.posicion[0] - pos_jugador[0])
        diferencia_y = abs(self.posicion[1] - pos_jugador[1])
        if not self.caminando:
            self.quedarse_quieto()
        elif diferencia_x < diferencia_y:
            if self.posicion == pos_jugador:
                self.quedarse_quieto()
            if self.posicion[0] < pos_jugador[0]:
                self.mover_derecha()
            if self.posicion[0] > pos_jugador[0]:
                self.mover_izquierda()
            if self.posicion[1] > pos_jugador[1]:
                self.mover_arriba()
            if self.posicion[1] < pos_jugador[1]:
                self.mover_abajo()
        else:
            if self.posicion == pos_jugador:
                self.quedarse_quieto()
            if self.posicion[1] > pos_jugador[1]:
                self.mover_arriba()
            if self.posicion[1] < pos_jugador[1]:
                self.mover_abajo()
            if self.posicion[0] < pos_jugador[0]:
                self.mover_derecha()
            if self.posicion[0] > pos_jugador[0]:
                self.mover_izquierda()

    def dibujar(self, pantalla):
        super(Enemigo, self).dibujar(pantalla)
        pygame.draw.rect(pantalla, (255, 0, 0), (self.posicion[0], self.posicion[1] - 10, self.vida_inicial, 5))
        pygame.draw.rect(pantalla, (0, 255, 0), (self.posicion[0], self.posicion[1] - 10, self.vida, 5))

    def golpe_enemigo(self, objeto_golpeado=None):
        if self.cooldown_ataque + self.tiempo_ataque <= pygame.time.get_ticks():
            self.tiempo_ataque = pygame.time.get_ticks()
            self.golpear(objeto_golpeado)

    def morir(self, lista_item):
        x = randint(0, 6)
        if x == 1:
            lista_item.append(Corazon(self.posicion[0], self.posicion[1]))
        if 2 <= x <= 4:
            lista_item.extend([Moneda(*posicion_aleatoria_radio(self.posicion[0], self.posicion[1], 30)) for _ in range(randint(1, 6))])

    def congelar(self, duracion):
        self.duracion_congelacion = duracion
        self.ultima_congelacion = pygame.time.get_ticks()
        self.quedarse_quieto()

    def esta_congelado(self):
        return self.ultima_congelacion + self.duracion_congelacion >= pygame.time.get_ticks()

    def movimiento_destino(self):
        if self.esta_congelado():
            self.quedarse_quieto()
        else:
            super(Enemigo, self).movimiento_destino()
