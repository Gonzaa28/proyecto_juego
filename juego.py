import pygame
import pygame_menu
import os
import sys
from pygame.locals import *

pygame.init()

ANCHO = 800
ALTO = 600
RESOLUCION = (ANCHO, ALTO)

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
PUNCH_UP = 4
PUNCH_RIGHT = 5
PUNCH_DOWN = 6
PUNCH_LEFT = 7

# pygame.time.get_ticks()


class ObjetoJuego:
    def __init__(self, imagenes, pos_x, pos_y, estado, animacion, velocidad):
        self.imagenes = imagenes
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.estado = estado
        self.animacion = animacion
        self.posicion = self.imagenes[self.estado][self.animacion].get_rect().move(pos_x, pos_y)
        self.velocidad = velocidad

    def dibujar(self, pantalla):
        pantalla.blit(self.imagenes[self.estado][self.animacion], self.posicion)

    def mover_arriba(self):
        self.posicion = self.posicion.move(0, -self.velocidad)
        if self.posicion.top < 0:
            self.posicion.top = 0

    def mover_derecha(self):
        self.posicion = self.posicion.move(self.velocidad, 0)
        if self.posicion.right > ANCHO:
            self.posicion.right = ANCHO

    def mover_abajo(self):
        self.posicion = self.posicion.move(0, self.velocidad)
        if self.posicion.bottom > ALTO:
            self.posicion.bottom = ALTO

    def mover_izquierda(self):
        self.posicion = self.posicion.move(-self.velocidad, 0)
        if self.posicion.left < 0:
            self.posicion.left = 0

    def recorrer_imagenes(self):
        cant_animaciones = len(self.imagenes[self.estado]) - 1
        if self.animacion > cant_animaciones:
            self.animacion = 0
        else:
            self.animacion += 1
        if self.animacion > cant_animaciones:
            self.animacion = 0


class Jugador(ObjetoJuego):
    def __init__(self, dimensiones=(60, 60)):
        imagenes = [
            [pygame.transform.scale(pygame.image.load("imagenes/jugador/up1.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/up2.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/up3.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/up4.png"), dimensiones)
             ],
            [pygame.transform.scale(pygame.image.load("imagenes/jugador/right1.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/right2.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/right3.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/right4.png"), dimensiones)
             ],
            [pygame.transform.scale(pygame.image.load("imagenes/jugador/down1.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/down2.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/down3.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/down4.png"), dimensiones),
             # pygame.transform.scale(pygame.image.load("imagenes/jugador/down5.png"), dimensiones)
             ],
            [pygame.transform.scale(pygame.image.load("imagenes/jugador/left1.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/left2.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/left3.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/left4.png"), dimensiones)
             ],
            [pygame.transform.scale(pygame.image.load("imagenes/jugador/punchup1.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/punchup2.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/punchup3.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/punchup4.png"), dimensiones)
             ],
            [pygame.transform.scale(pygame.image.load("imagenes/jugador/punchright1.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/punchright2.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/punchright3.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/punchright4.png"), dimensiones)
             ],
            [pygame.transform.scale(pygame.image.load("imagenes/jugador/punchdown1.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/punchdown2.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/punchdown3.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/punchdown4.png"), dimensiones)
             ],
            [pygame.transform.scale(pygame.image.load("imagenes/jugador/punchleft1.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/punchleft2.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/punchleft3.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/jugador/punchleft4.png"), dimensiones)
             ]
        ]
        super(Jugador, self).__init__(imagenes=imagenes, pos_x=int(ANCHO / 2), pos_y=int(ALTO / 2), estado=0,
                                      animacion=0, velocidad=5)
        self.ultimo_estado = 0

    def obtener_ultimo_estado(self):
        if self.estado is not PUNCH_UP and self.estado is not PUNCH_RIGHT and self.estado is not PUNCH_DOWN \
                and self.estado is not PUNCH_LEFT:
            self.ultimo_estado = self.estado
        return self.ultimo_estado

    def golpear(self):
        if self.obtener_ultimo_estado() == UP:
            self.estado = PUNCH_UP
        if self.obtener_ultimo_estado() == RIGHT:
            self.estado = PUNCH_RIGHT
        if self.obtener_ultimo_estado() == DOWN:
            self.estado = PUNCH_DOWN
        if self.obtener_ultimo_estado() == LEFT:
            self.estado = PUNCH_LEFT

    def detectar_colision(self,enemigo):

        if self.posicion.top <= enemigo.posicion.bottom and self.posicion.bottom >= enemigo.posicion.top \
                and self.posicion.right >= enemigo.posicion.left and self.posicion.left <= enemigo.posicion.right:
            enemigo.golpeado = True
        else:
            enemigo.golpeado = False

class Enemigo(ObjetoJuego):
    def __init__(self, dimensiones =(60, 60)):
        imagenes = [
            [pygame.transform.scale(pygame.image.load("imagenes/enemigo/up1.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/enemigo/up2.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/enemigo/up3.png"), dimensiones)
             ],
            [pygame.transform.scale(pygame.image.load("imagenes/enemigo/right1.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/enemigo/right2.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/enemigo/right3.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/enemigo/right4.png"), dimensiones)
             ],
            [pygame.transform.scale(pygame.image.load("imagenes/enemigo/down1.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/enemigo/down2.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/enemigo/down3.png"), dimensiones)
             ],
            [pygame.transform.scale(pygame.image.load("imagenes/enemigo/left1.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/enemigo/left2.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/enemigo/left3.png"), dimensiones),
             pygame.transform.scale(pygame.image.load("imagenes/enemigo/left4.png"), dimensiones),
             ]
        ]

        super(Enemigo, self).__init__(imagenes=imagenes, pos_x=int(ANCHO/2), pos_y=0, estado=0, animacion=0,
                                      velocidad=3)
        self.destino = (0, 0)
        self.golpeado = False

    def movimiento_trayectoria(self, pos_jugador):
        if self.posicion == pos_jugador:
            pass
        if self.posicion[0] <= pos_jugador[0]:
            self.mover_derecha()
        if self.posicion[0] >= pos_jugador[0]:
            self.mover_izquierda()
        if self.posicion[1] >= pos_jugador[1]:
            self.mover_arriba()
        if self.posicion[1] <= pos_jugador[1]:
            self.mover_abajo()


reloj = pygame.time.Clock()

pantalla = pygame.display.set_mode(RESOLUCION)
pygame.display.set_caption("Juego")
icono = pygame.transform.scale(pygame.image.load("imagenes/jugador/down1.png"), (80, 80))
pygame.display.set_icon(icono)
fondo = pygame.transform.scale(pygame.image.load("imagenes/fondo.png"), (ANCHO, ALTO)).convert()


def funcion():
    pantalla.blit(fondo, (0, 0))

    jugador = Jugador()
    enemigo = Enemigo()

    w_bandera = False
    d_bandera = False
    s_bandera = False
    a_bandera = False
    space_bandera = False

    corriendo = True

    while corriendo:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
                # sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                corriendo = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_w:
                w_bandera = True
            if evento.type == pygame.KEYUP and evento.key == pygame.K_w:
                w_bandera = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_d:
                d_bandera = True
            if evento.type == pygame.KEYUP and evento.key == pygame.K_d:
                d_bandera = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_s:
                s_bandera = True
            if evento.type == pygame.KEYUP and evento.key == pygame.K_s:
                s_bandera = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_a:
                a_bandera = True
            if evento.type == pygame.KEYUP and evento.key == pygame.K_a:
                a_bandera = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                space_bandera = True
            if evento.type == pygame.KEYUP and evento.key == pygame.K_SPACE:
                space_bandera = False

        pantalla.blit(fondo, jugador.posicion, jugador.posicion)
        pantalla.blit(fondo, enemigo.posicion, enemigo.posicion)

        if not w_bandera and not d_bandera and not s_bandera and not a_bandera and not space_bandera:
            jugador.animacion = 0
            if jugador.estado == PUNCH_UP or jugador.estado == PUNCH_RIGHT or jugador.estado == PUNCH_DOWN or\
                    jugador.estado == PUNCH_LEFT:
                jugador.estado = jugador.obtener_ultimo_estado()

        if w_bandera:
            jugador.mover_arriba()
            jugador.estado = UP
            jugador.recorrer_imagenes()

        if d_bandera:
            jugador.mover_derecha()
            jugador.estado = RIGHT
            jugador.recorrer_imagenes()

        if s_bandera:
            jugador.mover_abajo()
            jugador.estado = DOWN
            jugador.recorrer_imagenes()

        if a_bandera:
            jugador.mover_izquierda()
            jugador.estado = LEFT
            jugador.recorrer_imagenes()

        if space_bandera:
            jugador.golpear()
            jugador.recorrer_imagenes()

        if w_bandera and d_bandera:
            jugador.estado = UP
            jugador.recorrer_imagenes()

        if d_bandera and s_bandera:
            jugador.estado = DOWN
            jugador.recorrer_imagenes()

        if s_bandera and a_bandera:
            jugador.estado = DOWN
            jugador.recorrer_imagenes()

        if a_bandera and w_bandera:
            jugador.estado = UP
            jugador.recorrer_imagenes()

        if w_bandera and space_bandera:
            jugador.estado = PUNCH_UP
            jugador.mover_abajo()
            jugador.recorrer_imagenes()

        if d_bandera and space_bandera:
            jugador.estado = PUNCH_RIGHT
            jugador.mover_izquierda()
            jugador.recorrer_imagenes()

        if s_bandera and space_bandera:
            jugador.estado = PUNCH_DOWN
            jugador.mover_arriba()
            jugador.recorrer_imagenes()

        if a_bandera and space_bandera:
            jugador.estado = PUNCH_LEFT
            jugador.mover_derecha()
            jugador.recorrer_imagenes()

        if w_bandera and d_bandera and space_bandera:
            jugador.estado = PUNCH_UP
            jugador.recorrer_imagenes()

        if d_bandera and s_bandera and space_bandera:
            jugador.estado = PUNCH_DOWN
            jugador.recorrer_imagenes()

        if s_bandera and a_bandera and space_bandera:
            jugador.estado = PUNCH_DOWN
            jugador.recorrer_imagenes()

        if a_bandera and w_bandera and space_bandera:
            jugador.estado = PUNCH_UP
            jugador.recorrer_imagenes()

        if enemigo.posicion[1] > jugador.posicion[1] and (jugador.estado == UP or jugador.estado == DOWN):
            enemigo.estado = UP
            enemigo.recorrer_imagenes()

        if enemigo.posicion[0] < jugador.posicion[0] and (jugador.estado == RIGHT or jugador.estado == LEFT):
            enemigo.estado = RIGHT
            enemigo.recorrer_imagenes()

        if enemigo.posicion[1] < jugador.posicion[1] and (jugador.estado == DOWN or jugador.estado == UP):
            enemigo.estado = DOWN
            enemigo.recorrer_imagenes()

        if enemigo.posicion[0] > jugador.posicion[0] and (jugador.estado == LEFT or jugador.estado == RIGHT):
            enemigo.estado = LEFT
            enemigo.recorrer_imagenes()

        jugador.dibujar(pantalla)

        enemigo.movimiento_trayectoria(jugador.posicion)
        jugador.detectar_colision(enemigo)
        enemigo.dibujar(pantalla)

        if enemigo.golpeado:
           enemigo.estado = DOWN
        else:
            enemigo.estado = UP

        pygame.display.update()

        reloj.tick(15)


menu = pygame_menu.Menu(600, 800, 'Bienvenido', theme=pygame_menu.themes.THEME_DARK)
menu.add_text_input('Nombre: ')
menu.add_selector('Dificultad:', [('Difícil', 1), ('Fácil', 2)])
menu.add_button('Jugar', funcion)
menu.add_button('Salir', pygame_menu.events.EXIT)
menu.mainloop(pantalla)
