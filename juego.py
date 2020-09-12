import pygame
import pygame_menu  #Importamos el pygame y el menu del pygame. Que nos permiten hacen el juego.
import os
import sys
from pygame.locals import *

pygame.init()

ANCHO = 800
ALTO = 600  # Definimos las variables globales de alto y ancho de la pantalla del videojuego
RESOLUCION = (ANCHO, ALTO)  # Definimos la resolucion con una tupla del alto y el ancho.

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
PUNCH_UP = 4
PUNCH_RIGHT = 5
PUNCH_DOWN = 6
PUNCH_LEFT = 7  # Las distintas acciones que permite el videojuego. Moverse y golpear en 4 direcciones.


# pygame.time.get_ticks()


class ObjetoJuego:
    def __init__(self, imagenes, pos_x, pos_y, estado, animacion, velocidad):
        self.imagenes = imagenes
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.estado = estado
        self.animacion = animacion
        self.posicion = self.imagenes[self.estado][self.animacion].get_rect().move(pos_x, pos_y)
        self.velocidad = velocidad  # Creamos los atributos de la clase objetojuego.

    def dibujar(self, pantalla):
        pantalla.blit(self.imagenes[self.estado][self.animacion], self.posicion)  # Dibujamos la pantalla

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
            self.posicion.left = 0   # Marcamos los limites donde nos podemos mover, para los 4 lados.


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
        # Creamos la clase jugador, a partir de la clase
        #  A partir de la superclase objetojuego. Con las imagenes, e instanciando la clase
        # Con los atributos de la superclase


reloj = pygame.time.Clock()  # Declaramos el reloj, muy util para esto.

pantalla = pygame.display.set_mode(RESOLUCION)  # Declaramos la pantalla usando la funcion del pygame y la resolucion
pygame.display.set_caption("Juego")  # Mostramos el juego.
icono = pygame.transform.scale(pygame.image.load("imagenes/jugador/down1.png"), (80, 80))  # miniatura  icono del juego
pygame.display.set_icon(icono) # Mostramos la miniatura del mismo en la pantalla
fondo = pygame.transform.scale(pygame.image.load("imagenes/fondo.png"), (ANCHO, ALTO)).convert()
# Convertimos la miniatura por medio del comando convert.


def funcion():
    pantalla.blit(fondo, (0, 0))  # Llamamos a "fondo" como la imagen de fondo

    jugador = Jugador()  # Comandos del jugador.

    w_bandera = False
    d_bandera = False
    s_bandera = False
    a_bandera = False
    space_bandera = False  # Estos son los comandos que se usan en el juego. Se marcan como banderas.

    corriendo = True
    contador = 0
    while corriendo:  # Mientras este corriendo, Hace este while

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
                # Mientras se presione alguna tecla, hace la accion especifica.
                # Y Mientras corre se añade un contador, usando el reloj.

        pantalla.blit(fondo, jugador.posicion, jugador.posicion)
        #  Se actualiza la posicion de acorde a lo que esta hecho.

        if not w_bandera and not d_bandera and not s_bandera and not a_bandera and not space_bandera:
            jugador.animacion = 0
            # Aca esta en estado "idle" sin hacer nada.
            if jugador.estado == PUNCH_RIGHT or jugador.estado:
                jugador.estado = ultimo_estado
            # Aca guarda el ultimo estado del jugador, si no se movio, el goku apuntando a la derecha.

            if jugador.estado == DOWN and (contador % 90) == 0:
                jugador.animacion = 4


        if w_bandera:
            jugador.mover_arriba()
            jugador.estado = UP
            jugador.animacion += 1
            if jugador.animacion == 4:
                jugador.animacion = 0
            # Aca si se presiona la w, el jugador va hacia arriba.

        if d_bandera:
            jugador.mover_derecha()
            jugador.estado = RIGHT
            if jugador.animacion > 3:
                jugador.animacion = 0
            else:
                jugador.animacion += 1
            if jugador.animacion > 3:
                jugador.animacion = 0
        # Aca si se presiona la d, el jugador va hacia la derecha.

        if s_bandera:
            jugador.mover_abajo()
            jugador.estado = DOWN
            if jugador.animacion > 3:
                jugador.animacion = 0
            else:
                jugador.animacion += 1
            if jugador.animacion > 3:
                jugador.animacion = 0
                # Aca si se presiona la s, el jugador va hacia abajo.

        if a_bandera:
            jugador.mover_izquierda()
            jugador.estado = LEFT
            if jugador.animacion > 3:
                jugador.animacion = 0
            else:
                jugador.animacion += 1
            if jugador.animacion > 3:
                jugador.animacion = 0
                # Aca si se presiona la a, el jugador va hacia la izquierda.

        if jugador.estado is not PUNCH_RIGHT and jugador.estado is not PUNCH_DOWN and jugador.estado is not PUNCH_LEFT:
            ultimo_estado = jugador.estado
            # Aca guarda el ultimo estado del personaje golpeando.

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
                # Aca dependiendo la bandera que se use la animacion del golpe ira a partir de donde movamos el goku.

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
            # Aca haciamos el movimiento diagonal.

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
            # Aca hacemos el golpe para cada direccion.

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
            # Golpe en diagonal por cada direccion

        jugador.dibujar(pantalla)  # Dibuja en la pantalla lo que hace el personaje.

        pygame.display.update()  # Actualiza la pantalla.

        reloj.tick(15)  # Cambia cada 15 milisegundos la accion del personaje.


menu = pygame_menu.Menu(600, 800, 'Bienvenido', theme=pygame_menu.themes.THEME_DARK)  # Crea el menu
menu.add_text_input('Nombre: ')   # Con esto añadis el nombre
menu.add_selector('Dificultad:', [('Difícil', 1), ('Fácil', 2)])  # Dificultades
menu.add_button('Jugar', funcion)  # Entramos al juego
menu.add_button('Salir', pygame_menu.events.EXIT)  # Salir
menu.mainloop(pantalla)  # El menu va haciendo un loop hasta que hagamos una accion.
