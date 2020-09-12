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
             pygame.transform.scale(pygame.image.load("imagenes/jugador/down5.png"), dimensiones)
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


reloj = pygame.time.Clock()

pantalla = pygame.display.set_mode(RESOLUCION)
pygame.display.set_caption("Juego")
icono = pygame.transform.scale(pygame.image.load("imagenes/jugador/down1.png"), (80, 80))
pygame.display.set_icon(icono)
fondo = pygame.transform.scale(pygame.image.load("imagenes/fondo.png"), (ANCHO, ALTO)).convert()


def funcion():
    pantalla.blit(fondo, (0, 0))

    jugador = Jugador()

    w_bandera = False
    d_bandera = False
    s_bandera = False
    a_bandera = False
    space_bandera = False

    corriendo = True
    contador = 0
    while corriendo:

        contador += 5

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

        if not w_bandera and not d_bandera and not s_bandera and not a_bandera and not space_bandera:
            jugador.animacion = 0
            if jugador.estado == PUNCH_RIGHT or jugador.estado:
                jugador.estado = ultimo_estado

            if jugador.estado == DOWN and (contador % 90) == 0:
                jugador.animacion = 4

        if w_bandera:
            jugador.mover_arriba()
            jugador.estado = UP
            jugador.animacion += 1
            if jugador.animacion == 4:
                jugador.animacion = 0

        if d_bandera:
            jugador.mover_derecha()
            jugador.estado = RIGHT
            if jugador.animacion > 3:
                jugador.animacion = 0
            else:
                jugador.animacion += 1
            if jugador.animacion > 3:
                jugador.animacion = 0

        if s_bandera:
            jugador.mover_abajo()
            jugador.estado = DOWN
            if jugador.animacion > 3:
                jugador.animacion = 0
            else:
                jugador.animacion += 1
            if jugador.animacion > 3:
                jugador.animacion = 0

        if a_bandera:
            jugador.mover_izquierda()
            jugador.estado = LEFT
            if jugador.animacion > 3:
                jugador.animacion = 0
            else:
                jugador.animacion += 1
            if jugador.animacion > 3:
                jugador.animacion = 0

        if jugador.estado is not PUNCH_RIGHT and jugador.estado is not PUNCH_DOWN and jugador.estado is not PUNCH_LEFT:
            ultimo_estado = jugador.estado

        if space_bandera:
            if ultimo_estado == UP:
                jugador.estado = PUNCH_UP
            if ultimo_estado == RIGHT:
                jugador.estado = PUNCH_RIGHT
            if ultimo_estado == DOWN:
                jugador.estado = PUNCH_DOWN
            if ultimo_estado == LEFT:
                jugador.estado = PUNCH_LEFT
            if jugador.animacion > 3:
                jugador.animacion = 0
            else:
                jugador.animacion += 1
            if jugador.animacion > 3:
                jugador.animacion = 0

        if w_bandera and d_bandera:
            jugador.estado = UP
            jugador.animacion += 1
            if jugador.animacion == 4:
                jugador.animacion = 0

        if d_bandera and s_bandera:
            jugador.estado = DOWN
            jugador.animacion += 1
            if jugador.animacion == 4:
                jugador.animacion = 0

        if s_bandera and a_bandera:
            jugador.estado = DOWN
            jugador.animacion += 1
            if jugador.animacion == 4:
                jugador.animacion = 0

        if a_bandera and w_bandera:
            jugador.estado = UP
            jugador.animacion += 1
            if jugador.animacion == 4:
                jugador.animacion = 0

        if w_bandera and space_bandera:
            jugador.estado = PUNCH_UP
            jugador.mover_abajo()
            if jugador.animacion > 3:
                jugador.animacion = 0
            else:
                jugador.animacion += 1
            if jugador.animacion > 3:
                jugador.animacion = 0

        if d_bandera and space_bandera:
            jugador.estado = PUNCH_RIGHT
            jugador.mover_izquierda()
            if jugador.animacion > 3:
                jugador.animacion = 0
            else:
                jugador.animacion += 1
            if jugador.animacion > 3:
                jugador.animacion = 0

        if s_bandera and space_bandera:
            jugador.estado = PUNCH_DOWN
            jugador.mover_arriba()
            if jugador.animacion > 3:
                jugador.animacion = 0
            else:
                jugador.animacion += 1
            if jugador.animacion > 3:
                jugador.animacion = 0

        if a_bandera and space_bandera:
            jugador.estado = PUNCH_LEFT
            jugador.mover_derecha()
            if jugador.animacion > 3:
                jugador.animacion = 0
            else:
                jugador.animacion += 1
            if jugador.animacion > 3:
                jugador.animacion = 0

        if w_bandera and d_bandera and space_bandera:
            jugador.estado = PUNCH_UP
            if jugador.animacion > 3:
                jugador.animacion = 0
            else:
                jugador.animacion += 1
            if jugador.animacion > 3:
                jugador.animacion = 0

        if d_bandera and s_bandera and space_bandera:
            jugador.estado = PUNCH_DOWN
            if jugador.animacion > 3:
                jugador.animacion = 0
            else:
                jugador.animacion += 1
            if jugador.animacion > 3:
                jugador.animacion = 0

        if s_bandera and a_bandera and space_bandera:
            jugador.estado = PUNCH_DOWN
            if jugador.animacion > 3:
                jugador.animacion = 0
            else:
                jugador.animacion += 1
            if jugador.animacion > 3:
                jugador.animacion = 0

        if a_bandera and w_bandera and space_bandera:
            jugador.estado = PUNCH_UP
            if jugador.animacion > 3:
                jugador.animacion = 0
            else:
                jugador.animacion += 1
            if jugador.animacion > 3:
                jugador.animacion = 0

        jugador.dibujar(pantalla)

        pygame.display.update()

        reloj.tick(15)


menu = pygame_menu.Menu(600, 800, 'Bienvenido', theme=pygame_menu.themes.THEME_DARK)
menu.add_text_input('Nombre: ')
menu.add_selector('Dificultad:', [('Difícil', 1), ('Fácil', 2)])
menu.add_button('Jugar', funcion)
menu.add_button('Salir', pygame_menu.events.EXIT)
menu.mainloop(pantalla)
