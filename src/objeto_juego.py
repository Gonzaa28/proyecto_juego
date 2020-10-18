import pygame
from src.funciones import *


class ObjetoJuego:
    def __init__(self, imagenes, pos_x, pos_y, estado, animacion, velocidad, poder_ataque=2,
                 cooldown_ataque=500, vida_inicial=50):
        self.imagenes = imagenes
        self.destino = None
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.estado = estado
        self.animacion = animacion
        self.posicion = self.imagenes[self.estado][self.animacion].get_rect().move(pos_x, pos_y)
        self.velocidad = velocidad
        self.golpeando = False
        self.caminando = True
        self.ultimo_estado = self.estado
        self.vida_inicial = vida_inicial
        self.vida = vida_inicial
        self.poder_ataque = poder_ataque
        self.ultimo_dibujo_tiempo = pygame.time.get_ticks()
        self.cooldown_ataque = cooldown_ataque
        self.tiempo_ataque = pygame.time.get_ticks()


    def dibujar(self, pantalla):
        try:
            pantalla.blit(self.imagenes[self.estado][self.animacion], self.posicion)
        except:
            pass

    def mover_arriba(self):
        if self.golpeando:
            self.estado = PUNCH_UP
        else:
            self.estado = UP
            self.posicion = self.posicion.move(0, -self.velocidad)
            if self.posicion.top < 0:
                self.posicion.top = 0
        self.caminando = True
        self.ultimo_estado = UP

    def mover_derecha(self):
        if self.golpeando:
            self.estado = PUNCH_RIGHT
        else:
            self.estado = RIGHT
            self.posicion = self.posicion.move(self.velocidad, 0)
            if self.posicion.right > ANCHO:
                self.posicion.right = ANCHO
        self.caminando = True
        self.ultimo_estado = RIGHT

    def mover_abajo(self):
        if self.golpeando:
            self.estado = PUNCH_DOWN
        else:
            self.estado = DOWN
            self.posicion = self.posicion.move(0, self.velocidad)
            if self.posicion.bottom > ALTO:
                self.posicion.bottom = ALTO
        self.caminando = True
        self.ultimo_estado = DOWN

    def mover_izquierda(self):
        if self.golpeando:
            self.estado = PUNCH_LEFT
        else:
            self.estado = LEFT
            self.posicion = self.posicion.move(-self.velocidad, 0)
            if self.posicion.left < 0:
                self.posicion.left = 0
        self.caminando = True
        self.ultimo_estado = LEFT

    def recorrer_imagenes(self, duracion = 75):
        if self.caminando or self.golpeando:
            if self.ultimo_dibujo_tiempo + duracion <= pygame.time.get_ticks():
                self.ultimo_dibujo_tiempo = pygame.time.get_ticks()
                cant_animaciones = len(self.imagenes[self.estado]) - 1
                if self.animacion > cant_animaciones:
                    self.animacion = 0
                else:
                    self.animacion += 1
                if self.animacion > cant_animaciones:
                    self.animacion = 0
        else:
            self.animacion = 0

    def quedarse_quieto(self):
        self.caminando = False

    def golpear(self, objeto_golpeado=None, danio=1):
        self.golpeando = True
        if objeto_golpeado:
            objeto_golpeado.vida -= self.modificar_poder_ataque(danio)
        if self.ultimo_estado == UP:
            self.estado = PUNCH_UP
        if self.ultimo_estado == RIGHT:
            self.estado = PUNCH_RIGHT
        if self.ultimo_estado == DOWN:
            self.estado = PUNCH_DOWN
        if self.ultimo_estado == LEFT:
            self.estado = PUNCH_LEFT

    def no_golpear(self):
        self.golpeando = False
        self.estado = self.ultimo_estado

    def detectar_colision(self, lista):
        for enemigo in lista:
            if self is not enemigo:
                if self.posicion.top <= enemigo.posicion.bottom and self.posicion.bottom >= enemigo.posicion.top \
                        and self.posicion.right >= enemigo.posicion.left and self.posicion.left <= enemigo.posicion.right:
                    # enemigo.caminando = False
                    yield enemigo
            # else:
            #     enemigo.caminando = True
        return

    def modificar_poder_ataque(self, danio=1):
        return self.poder_ataque * danio

    def movimiento_destino(self):
        if not self.destino:
            self.destino = posicion_aleatoria_mapa()
        if self.posicion.collidepoint(self.destino):
            self.destino = None
        else:
            if self.posicion.centerx < self.destino[0]:
                self.mover_derecha()
            elif self.posicion.centerx > self.destino[0]:
                self.mover_izquierda()
            if self.posicion.centery < self.destino[1]:
                self.mover_abajo()
            elif self.posicion.centery > self.destino[1]:
                self.mover_arriba()