import pygame
import pygame_menu
from pygame_menu.themes import Theme
from random import randint
import os
import sys
from pygame.locals import *

pygame.init()
pygame.font.init()

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


class ObjetoJuego:
    def __init__(self, imagenes, pos_x, pos_y, estado, animacion, velocidad, poder_ataque=2,
                 cooldown_ataque=500, vida_inicial=50):
        self.imagenes = imagenes
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

    def recorrer_imagenes(self):
        if self.caminando or self.golpeando:
            if self.ultimo_dibujo_tiempo + 75 <= pygame.time.get_ticks():
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

    def golpear(self, objeto_golpeado=None):
        self.golpeando = True
        if objeto_golpeado:
            objeto_golpeado.vida -= self.modificar_poder_ataque()
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
            if self.posicion.top <= enemigo.posicion.bottom and self.posicion.bottom >= enemigo.posicion.top \
                    and self.posicion.right >= enemigo.posicion.left and self.posicion.left <= enemigo.posicion.right:
                # enemigo.caminando = False
                yield enemigo
            # else:
            #     enemigo.caminando = True
        return

    def modificar_poder_ataque(self):
        return self.poder_ataque


class Jugador(ObjetoJuego):
    def __init__(self, dimensiones=(50, 50)):
        imagenes = {
            UP: [pygame.transform.scale(pygame.image.load("imagenes/jugador/up1.png"), dimensiones),
                 pygame.transform.scale(pygame.image.load("imagenes/jugador/up2.png"), dimensiones),
                 pygame.transform.scale(pygame.image.load("imagenes/jugador/up3.png"), dimensiones)
                 ],
            RIGHT: [pygame.transform.scale(pygame.image.load("imagenes/jugador/right1.png"), dimensiones),
                    pygame.transform.scale(pygame.image.load("imagenes/jugador/right2.png"), dimensiones),
                    pygame.transform.scale(pygame.image.load("imagenes/jugador/right3.png"), dimensiones)
                    ],
            DOWN: [pygame.transform.scale(pygame.image.load("imagenes/jugador/down1.png"), dimensiones),
                   pygame.transform.scale(pygame.image.load("imagenes/jugador/down2.png"), dimensiones),
                   pygame.transform.scale(pygame.image.load("imagenes/jugador/down3.png"), dimensiones)
                   ],
            LEFT: [pygame.transform.scale(pygame.image.load("imagenes/jugador/left1.png"), dimensiones),
                   pygame.transform.scale(pygame.image.load("imagenes/jugador/left2.png"), dimensiones),
                   pygame.transform.scale(pygame.image.load("imagenes/jugador/left3.png"), dimensiones)
                   ],
            PUNCH_UP: [  # pygame.transform.scale(pygame.image.load("imagenes/jugador/punchup1.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/punchup2.png"), dimensiones)
            ],
            PUNCH_RIGHT: [
                # pygame.transform.scale(pygame.image.load("imagenes/jugador/punchright1.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/punchright2.png"), dimensiones)
            ],
            PUNCH_DOWN: [  # pygame.transform.scale(pygame.image.load("imagenes/jugador/punchdown1.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/punchdown2.png"), dimensiones)
            ],
            PUNCH_LEFT: [  # pygame.transform.scale(pygame.image.load("imagenes/jugador/punchleft1.png"), dimensiones),
                pygame.transform.scale(pygame.image.load("imagenes/jugador/punchleft2.png"), dimensiones)
            ]
        }
        super(Jugador, self).__init__(imagenes=imagenes, pos_x=int(ANCHO / 2), pos_y=int(ALTO / 2), estado=0,
                                      animacion=0, velocidad=10, vida_inicial=50, poder_ataque=12)
        self.lista_disparos = []

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
            self.curarse()

    def dibujar(self, pantalla):
        for disparo in reversed(self.lista_disparos):
            try:
                if disparo.posicion.top <= 0 or disparo.posicion.right >= ANCHO or disparo.posicion.bottom >= ALTO or \
                        disparo.posicion.left <= 0:
                    self.lista_disparos.remove(disparo)
                disparo.movimiento()
                disparo.dibujar(pantalla)
            except:
                pass
        super(Jugador, self).dibujar(pantalla)
        # fuente = pygame.font.SysFont('Comic Sans MS', 15)
        # texto = fuente.render(f'{"".join(["-" for _ in range(self.vida)])}', False, (0, 255, 0))
        # rectangulo = texto.get_rect()
        # rectangulo.bottom = self.posicion.top
        # rectangulo.centerx = self.posicion.centerx
        # pantalla.blit(texto, (rectangulo[0], rectangulo[1]))
        pygame.draw.rect(pantalla, (255, 0, 0), (self.posicion[0], self.posicion[1] - 10, self.vida_inicial, 5))
        pygame.draw.rect(pantalla, (0, 255, 0), (self.posicion[0], self.posicion[1] - 10, self.vida, 5))

    def disparar(self):
        if self.cooldown_ataque + self.tiempo_ataque <= pygame.time.get_ticks():
            self.tiempo_ataque = pygame.time.get_ticks()
            self.lista_disparos.append(Disparo(self.posicion.centerx, self.posicion.centery, self.ultimo_estado))
            self.golpear()

    def curarse(self):
        if self.vida < self.vida_inicial:
            self.vida += 5


class Disparo(ObjetoJuego):
    def __init__(self, pos_x, pos_y, estado, dimensiones_vertical=(10, 25), dimensiones_horizontal=(25, 10)):
        imagenes = {
            UP: [pygame.transform.scale(pygame.image.load("imagenes/jugador/arrowup.png"), dimensiones_vertical)],
            RIGHT: [
                pygame.transform.scale(pygame.image.load("imagenes/jugador/arrowright.png"), dimensiones_horizontal)],
            DOWN: [pygame.transform.scale(pygame.image.load("imagenes/jugador/arrowdown.png"), dimensiones_vertical)],
            LEFT: [pygame.transform.scale(pygame.image.load("imagenes/jugador/arrowleft.png"), dimensiones_horizontal)]
        }
        super(Disparo, self).__init__(imagenes=imagenes, pos_x=pos_x, pos_y=pos_y, estado=estado, animacion=0,
                                      velocidad=15)
        self.pos_x = pos_x
        self.pos_y = pos_y

    def movimiento(self):
        if self.estado == UP:
            self.mover_arriba()
        if self.estado == RIGHT:
            self.mover_derecha()
        if self.estado == DOWN:
            self.mover_abajo()
        if self.estado == LEFT:
            self.mover_izquierda()


class Enemigo(ObjetoJuego):
    def __init__(self, pos_x=int(ANCHO / 2), pos_y=0, dimensiones=(45, 45)):
        imagenes = {
            UP: [pygame.transform.scale(pygame.image.load("imagenes/enemigo/up1.png"), dimensiones),
                 pygame.transform.scale(pygame.image.load("imagenes/enemigo/up2.png"), dimensiones),
                 pygame.transform.scale(pygame.image.load("imagenes/enemigo/up3.png"), dimensiones),
                 # pygame.transform.scale(pygame.image.load("imagenes/enemigo/up4.png"), dimensiones),
                 # pygame.transform.scale(pygame.image.load("imagenes/enemigo/up5.png"), dimensiones)
                 ],
            RIGHT: [pygame.transform.scale(pygame.image.load("imagenes/enemigo/right1.png"), dimensiones),
                    pygame.transform.scale(pygame.image.load("imagenes/enemigo/right2.png"), dimensiones),
                    pygame.transform.scale(pygame.image.load("imagenes/enemigo/right3.png"), dimensiones),
                    # pygame.transform.scale(pygame.image.load("imagenes/enemigo/right4.png"), dimensiones)
                    ],
            DOWN: [pygame.transform.scale(pygame.image.load("imagenes/enemigo/down1.png"), dimensiones),
                   pygame.transform.scale(pygame.image.load("imagenes/enemigo/down2.png"), dimensiones),
                   pygame.transform.scale(pygame.image.load("imagenes/enemigo/down3.png"), dimensiones),
                   # pygame.transform.scale(pygame.image.load("imagenes/enemigo/down4.png"), dimensiones),
                   # pygame.transform.scale(pygame.image.load("imagenes/enemigo/down5.png"), dimensiones)
                   ],
            LEFT: [pygame.transform.scale(pygame.image.load("imagenes/enemigo/left1.png"), dimensiones),
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
        self.destino = (0, 0)
        self.golpeado = False

    def movimiento_trayectoria(self, pos_jugador):
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

    # def detectar_colision(self, lista):
    #     flag = False
    #     for x in super(Enemigo, self).detectar_colision(lista):
    #         flag = True
    #         yield x
    #     if flag:
    #         self.golpear()
    #     else:
    #         self.no_golpear()
    #     return

    def dibujar(self, pantalla):
        super(Enemigo, self).dibujar(pantalla)
        # fuente = pygame.font.SysFont('Comic Sans MS', 15)
        # texto = fuente.render(f'{"".join(["-" for _ in range(self.vida)])}', False, (255, 0, 0))
        # rectangulo = texto.get_rect()
        # rectangulo.bottom = self.posicion.top
        # rectangulo.centerx = self.posicion.centerx
        # pantalla.blit(texto, (rectangulo[0], rectangulo[1]))
        pygame.draw.rect(pantalla, (255, 0, 0), (self.posicion[0], self.posicion[1] - 10, self.vida_inicial, 5))
        pygame.draw.rect(pantalla, (0, 255, 0), (self.posicion[0], self.posicion[1] - 10, self.vida, 5))

    def golpe_enemigo(self, objeto_golpeado=None):
        if self.cooldown_ataque + self.tiempo_ataque <= pygame.time.get_ticks():
            self.tiempo_ataque = pygame.time.get_ticks()
            self.golpear(objeto_golpeado)


class Nivel:
    pass


reloj = pygame.time.Clock()

pantalla = pygame.display.set_mode(RESOLUCION)
pygame.display.set_caption("Juego")
icono = pygame.transform.scale(pygame.image.load("imagenes/jugador/down1.png"), (80, 80))
pygame.display.set_icon(icono)
fondo = pygame.transform.scale(pygame.image.load("imagenes/fondo.png"), (ANCHO, ALTO)).convert()
fuente = pygame.font.SysFont('Bauhaus 93', 25, False)


def pausa():

    fuente = pygame.font.SysFont('Bauhaus 93', 35)
    pausado = True

    while pausado:
        texto = fuente.render("Pausa", False, (0, 0, 0))
        rectangulo = texto.get_rect()
        pantalla.blit(texto, ((ANCHO/2-rectangulo[2]+25), (ALTO/2-rectangulo[3])))
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_q:
                pausado = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pausado = False
        pygame.display.update()

    reloj.tick(15)


def funcion():
    pantalla.blit(fondo, (0, 0))

    jugador = Jugador()
    lista_enemigos = [Enemigo(pos_x=randint(1, int(ANCHO)), pos_y=randint(1, 500)) for _ in range(3)]

    banderas = {
        'w_bandera': False,
        'd_bandera': False,
        's_bandera': False,
        'a_bandera': False,
        'space_bandera': False,
        'f_bandera': False
    }

    score = 0
    respawn = 5000
    ultimo_enemigo = pygame.time.get_ticks()

    corriendo = True

    while corriendo:

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
                # sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                corriendo = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_w:
                banderas['w_bandera'] = True
            if evento.type == pygame.KEYUP and evento.key == pygame.K_w:
                banderas['w_bandera'] = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_d:
                banderas['d_bandera'] = True
            if evento.type == pygame.KEYUP and evento.key == pygame.K_d:
                banderas['d_bandera'] = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_s:
                banderas['s_bandera'] = True
            if evento.type == pygame.KEYUP and evento.key == pygame.K_s:
                banderas['s_bandera'] = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_a:
                banderas['a_bandera'] = True
            if evento.type == pygame.KEYUP and evento.key == pygame.K_a:
                banderas['a_bandera'] = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                banderas['space_bandera'] = True
            if evento.type == pygame.KEYUP and evento.key == pygame.K_SPACE:
                banderas['space_bandera'] = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_f:
                banderas['f_bandera'] = True
            if evento.type == pygame.KEYUP and evento.key == pygame.K_f:
                banderas['f_bandera'] = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_p:
                banderas = {
                    'w_bandera': False,
                    'd_bandera': False,
                    's_bandera': False,
                    'a_bandera': False,
                    'space_bandera': False,
                    'f_bandera': False
                }
                pausa()

        pantalla.blit(fondo, (0, 0))

        if ultimo_enemigo + respawn <= pygame.time.get_ticks():
            ultimo_enemigo = pygame.time.get_ticks()
            lista_enemigos.append(Enemigo(pos_x=randint(1, int(ANCHO / 2)), pos_y=randint(1, 500)))

        if score % 20 == 0 and score > 0 and respawn > 500:
            respawn -= 10

        texto = fuente.render(f'Score: {score}', False, (0, 0, 0))
        pantalla.blit(texto, (5, 0))

        jugador.procesar_accion(banderas)

        jugador.recorrer_imagenes()

        jugador.dibujar(pantalla)

        for enemigo in lista_enemigos:
            enemigo.movimiento_trayectoria(jugador.posicion)
            enemigo.recorrer_imagenes()
            enemigo.dibujar(pantalla)

        for x in jugador.detectar_colision([enemigo]):
            pass

        for enemigo in reversed(lista_enemigos):
            debe_golpear = False
            for x in enemigo.detectar_colision([jugador]):
                debe_golpear = True
                enemigo.golpe_enemigo(jugador)
                if jugador.vida <= 0:
                    corriendo = False
            if not debe_golpear:
                enemigo.no_golpear()

            for x in enemigo.detectar_colision(reversed(jugador.lista_disparos)):
                jugador.lista_disparos.remove(x)
                jugador.golpear(enemigo)
                if enemigo.vida <= 0:
                    lista_enemigos.remove(enemigo)
                    score += 5

        pygame.display.update()

        reloj.tick(15)


imagen = pygame_menu.baseimage.BaseImage(
    image_path='imagenes/fondo.png',
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY,
    drawing_offset=(0, 0))

tema = Theme(background_color=imagen,
             cursor_color=(0, 0, 0),
             menubar_close_button=False,
             selection_color=(0, 0, 0),
             title_background_color=(255, 255, 255),
             title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
             title_font=pygame_menu.font.FONT_MUNRO,
             title_font_antialias=True,
             title_font_color=(0, 0, 0),
             title_font_size=75,
             title_shadow=True,
             title_shadow_color=(75, 75, 75),
             title_offset=(ANCHO/2-86, 10),
             widget_background_color=(0, 0, 0, 0),
             widget_font=pygame_menu.font.FONT_MUNRO,
             widget_font_antialias=True,
             widget_font_color=(75, 75, 75),
             widget_font_size=40,
             widget_selection_effect=pygame_menu.widgets.selection.LeftArrowSelection(blink_ms=300),
             widget_shadow=True,
             widget_shadow_color=(75, 75, 75),
             widget_shadow_offset=2)

menu = pygame_menu.Menu(600, 800, 'Juego', theme=tema)

menu.add_text_input('Name: ')
menu.add_selector('Difficulty: ', [('Hard', 1), ('Medium', 2), ('Easy', 3)])
menu.add_button('Play', funcion)
menu.add_button('Exit', pygame_menu.events.EXIT)
menu.mainloop(pantalla)
