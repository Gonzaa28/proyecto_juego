import pygame
from src.disparo import Disparo
from src.disparo_bomba import DisparoBomba
from src.disparo_congelante import DisparoCongelante
from src.objeto_juego import ObjetoJuego
from src.configuracion import *


class Jugador(ObjetoJuego):
    def __init__(self, dimensiones=(50, 50)):
        imagenes = {
            UP: [
                pygame.transform.scale(pygame.image.load("imagenes/jugador/up1.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/up2.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/up3.png"), dimensiones)
            ],
            RIGHT: [
                pygame.transform.scale(pygame.image.load("imagenes/jugador/right1.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/right2.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/right3.png"), dimensiones)
            ],
            DOWN: [
                pygame.transform.scale(pygame.image.load("imagenes/jugador/down1.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/down2.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/down3.png"), dimensiones)
            ],
            LEFT: [
                pygame.transform.scale(pygame.image.load("imagenes/jugador/left1.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/left2.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/left3.png"), dimensiones)
            ],
            PUNCH_UP: [
                # pygame.transform.scale(pygame.image.load("imagenes/jugador/punchup1.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/punchup2.png"), dimensiones)
            ],
            PUNCH_RIGHT: [
                # pygame.transform.scale(pygame.image.load("imagenes/jugador/punchright1.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/punchright2.png"), dimensiones)
            ],
            PUNCH_DOWN: [
                # pygame.transform.scale(pygame.image.load("imagenes/jugador/punchdown1.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/punchdown2.png"), dimensiones)
            ],
            PUNCH_LEFT: [
                # pygame.transform.scale(pygame.image.load("imagenes/jugador/punchleft1.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/punchleft2.png"), dimensiones)
            ]
        }
        super(Jugador, self).__init__(imagenes=imagenes, pos_x=int(ANCHO / 2), pos_y=int(ALTO / 2), estado=0,
                                      animacion=0, velocidad=10, vida_inicial=50, poder_ataque=1)
        self.lista_disparos = []
        self.lista_disparos_bomba = []
        self.lista_disparos_stun = []
        self.ultima_curacion = pygame.time.get_ticks()
        self.coins = 0

    def procesar_accion(self, acciones):
        if not acciones['w_bandera'] and not acciones['d_bandera'] and not acciones['s_bandera'] and not \
                acciones['a_bandera']:
            self.quedarse_quieto()
        if acciones['a_bandera']:
            self.mover_izquierda()
        if acciones['d_bandera']:
            self.mover_derecha()
        if acciones['w_bandera']:
            self.mover_arriba()
        if acciones['s_bandera']:
            self.mover_abajo()
        if acciones['space_bandera']:
            self.disparar()
        else:
            self.no_golpear()
        if acciones['f_bandera']:
            self.disparar(infinito=True)
        if acciones['r_bandera']:
            self.disparar_bomba()
        if acciones['v_bandera']:
            self.disparar_congeladores()

    def dibujar(self, pantalla):
        for disparo in reversed(self.lista_disparos):
            try:
                if disparo.posicion.top <= 0 or disparo.posicion.right >= ANCHO or disparo.posicion.bottom >= ALTO or \
                        disparo.posicion.left <= 0:
                    if disparo.infinito:
                        if disparo.posicion.right >= ANCHO:
                            disparo.posicion.left = 0
                        elif disparo.posicion.left <= 0:
                            disparo.posicion.right = ANCHO
                        elif disparo.posicion.top <= 0:
                            disparo.posicion.bottom = ALTO
                        elif disparo.posicion.bottom >= ALTO:
                            disparo.posicion.top = 0
                    else:
                        self.lista_disparos.remove(disparo)
                disparo.movimiento()
                disparo.dibujar(pantalla)
            except:
                pass

        for disparo in reversed(self.lista_disparos_bomba):
            try:
                if disparo.posicion.top <= 0 or disparo.posicion.right >= ANCHO or disparo.posicion.bottom >= ALTO or \
                        disparo.posicion.left <= 0:
                    self.lista_disparos_bomba.remove(disparo)
                disparo.movimiento()
                disparo.dibujar(pantalla)
                if disparo.explotado and disparo.tiempo_detonacion + disparo.duracion_explosion <= pygame.time.get_ticks():
                    self.lista_disparos_bomba.remove(disparo)
            except:
                pass

        for disparo in reversed(self.lista_disparos_stun):
            try:
                if disparo.posicion.top <= 0 or disparo.posicion.right >= ANCHO or disparo.posicion.bottom >= ALTO or \
                        disparo.posicion.left <= 0:
                    self.lista_disparos_stun.remove(disparo)
                disparo.movimiento()
                disparo.dibujar(pantalla)
                # if disparo.explotado and disparo.tiempo_detonacion + disparo.duracion_explosion <= pygame.time.get_ticks():
                    #self.lista_disparos_stun.remove(disparo) MODIFAR PARA ANIMACION
            except:
                pass

        super(Jugador, self).dibujar(pantalla)
        pygame.draw.rect(pantalla, (255, 0, 0), (self.posicion[0], self.posicion[1] - 10, self.vida_inicial, 5))
        pygame.draw.rect(pantalla, (0, 255, 0), (self.posicion[0], self.posicion[1] - 10, self.vida, 5))

    def disparar(self, infinito=False):
        if self.cooldown_ataque + self.tiempo_ataque <= pygame.time.get_ticks():
            self.tiempo_ataque = pygame.time.get_ticks()
            self.lista_disparos.append(Disparo(self.posicion.centerx, self.posicion.centery, self.ultimo_estado, infinito=infinito)) # TODO VALIDACION SI PODES USAR UN DISPARO INFINITO
            self.golpear()

    def curarse(self, val_curacion):
        if self.vida <= self.vida_inicial:
            self.vida = self.vida + val_curacion if self.vida + val_curacion <= self.vida_inicial else self.vida_inicial
            return True
        return False

    def disparar_bomba(self):
        if self.cooldown_ataque + self.tiempo_ataque <= pygame.time.get_ticks():
            self.tiempo_ataque = pygame.time.get_ticks()
            self.lista_disparos_bomba.append(DisparoBomba(self.posicion.centerx, self.posicion.centery, self.ultimo_estado))
            self.golpear()

    def disparar_congeladores(self):
        if self.cooldown_ataque + self.tiempo_ataque <= pygame.time.get_ticks():
            self.tiempo_ataque = pygame.time.get_ticks()
            self.lista_disparos_stun.append(DisparoCongelante(self.posicion.centerx, self.posicion.centery, self.ultimo_estado))
            self.golpear()

    def add_coins(self, cantidad):
        self.coins += cantidad
        return True

    def spend_coins(self, cantidad):
        if self.coins - cantidad > 0:
            self.coins -= cantidad
            return True
        return False

    def vaciar_ataques(self):
        self.lista_disparos = []
        self.lista_disparos_bomba = []
        self.lista_disparos_stun = []
