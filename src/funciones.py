from random import randint
from src.configuracion import *


def posicion_aleatoria_mapa():
    return randint(0+100, ANCHO-100), randint(0+100, ALTO-100)


def posicion_aleatoria_radio(punto_x, punto_y, radio):
    if punto_x + radio >= ANCHO:
        pos_x = randint(punto_x - radio, ANCHO - 30)
    elif punto_x - radio < 0:
        pos_x = randint(0 + 30, punto_x + radio)
    else:
        pos_x = randint(punto_x - radio, punto_x + radio)

    if punto_y + radio >= ALTO:
        pos_y = randint(punto_y - radio, ALTO - 30)
    elif punto_y - radio < 0:
        pos_y = randint(0 + 30, punto_y + radio)
    else:
        pos_y = randint(punto_y - radio, punto_y + radio)

    return pos_x, pos_y
