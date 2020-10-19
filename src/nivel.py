from random import randint
import pygame
from src.funciones import posicion_aleatoria_mapa
from src.enemigo import *
from src.configuracion import *


class Nivel:
    def __init__(self, imagen_fondo, jugador, numero, cantidad_enemigos=3, respawn=10000):
        self.numero = numero
        self.fondo = pygame.transform.scale(pygame.image.load(imagen_fondo), (ANCHO, ALTO)).convert()
        self.jugador = jugador
        self.enemigos = [Enemigo(pos_x=randint(1, int(ANCHO)), pos_y=randint(1, 500)) for _ in range(cantidad_enemigos)]
        self.items = []
        self.moneda = Moneda(ANCHO / 2, 0)
        self.respawn = respawn
        self.ultimo_enemigo = pygame.time.get_ticks()

    def bucle_principal(self, pantalla, fuente, banderas):
        pantalla.blit(self.fondo, (0, 0))

        if self.ultimo_enemigo + self.respawn <= pygame.time.get_ticks():
            self.ultimo_enemigo = pygame.time.get_ticks()
            self.enemigos.append(Enemigo(pos_x=randint(1, int(ANCHO / 2)), pos_y=randint(1, 500)))

        self.moneda.dibujar(pantalla)
        texto_coins = fuente.render(f'{self.jugador.coins}', False, (0, 0, 0))
        rec = texto_coins.get_rect()
        pantalla.blit(texto_coins, (self.moneda.posicion.right, self.moneda.posicion.top))
        texto = fuente.render(f'Nivel: {self.numero}', False, (0, 0, 0))
        pantalla.blit(texto, (5, 0))

        self.jugador.procesar_accion(banderas)

        self.jugador.recorrer_imagenes()

        self.jugador.dibujar(pantalla)

        for enemigo in self.enemigos:
            if not enemigo.destino:
                enemigo.movimiento_trayectoria(self.jugador.posicion)
                for otro_enemigo in enemigo.detectar_colision(self.enemigos):
                    otro_enemigo.destino = posicion_aleatoria_mapa()
            else:
                enemigo.movimiento_destino()
            enemigo.recorrer_imagenes()
            enemigo.dibujar(pantalla)

        for enemigo in reversed(self.enemigos):
            debe_golpear = False
            for x in enemigo.detectar_colision([self.jugador]):
                debe_golpear = True
                enemigo.golpe_enemigo(self.jugador)
                if self.jugador.vida <= 0:
                    return
            if not debe_golpear:
                enemigo.no_golpear()

            for x in enemigo.detectar_colision(reversed(self.jugador.lista_disparos)):
                self.jugador.lista_disparos.remove(x)
                self.jugador.golpear(enemigo, x.poder_ataque)
                if enemigo.vida <= 0:
                    self.enemigos.remove(enemigo)
                    enemigo.morir(self.items)

            for x in enemigo.detectar_colision(reversed(self.jugador.lista_disparos_stun)):
                if not x.congelado:
                    x.congelar()
                    enemigo.congelar(x.duracion_congelacion)
                    for enemigo_congelacion in x.detectar_colision(reversed(self.enemigos)):
                        enemigo_congelacion.congelar(x.duracion_congelacion)
                        self.jugador.golpear(enemigo_congelacion, x.poder_ataque)
                        if enemigo_congelacion.vida <= 0:
                            if enemigo_congelacion in self.enemigos:
                                self.enemigos.remove(enemigo_congelacion)
                                enemigo.morir(self.items)

                # self.jugador.lista_disparos_stun.remove(x)
                # self.jugador.golpear(enemigo, x.poder_ataque)
                # enemigo.congelar(x.duracion_congelacion)
                # if enemigo.vida <= 0:
                #     self.enemigos.remove(enemigo)
                #     enemigo.morir(self.items)

            for x in enemigo.detectar_colision(reversed(self.jugador.lista_disparos_bomba)):
                if not x.explotado:
                    x.detonar()
                    for enemigo_explosion in x.detectar_colision(reversed(self.enemigos)):
                        self.jugador.golpear(enemigo_explosion, x.poder_ataque)
                        if enemigo_explosion.vida <= 0:
                            if enemigo_explosion in self.enemigos:
                                self.enemigos.remove(enemigo_explosion)
                                enemigo.morir(self.items)

        for item_recogido in self.jugador.detectar_colision(self.items):
            if item_recogido.recoger(self.jugador):
                self.items.remove(item_recogido)
                pass
                # agregar sonido

        for item in self.items:
            item.dibujar(pantalla)

        return

    def nivel_ganado(self):
        return len(self.enemigos) == 0

    def nivel_perdido(self):
        return self.jugador.vida <= 0

    @staticmethod
    def traer_fondo_nivel(numero):
        if numero % 5 == 1:
            return "imagenes/fondo.png"
        if numero % 5 == 2:
            return "imagenes/fondoAmarillo.png"
        if numero % 5 == 3:
            return "imagenes/fondoNevado.png"
        if numero % 5 == 4:
            return "imagenes/FondoNoche.png"
        if numero % 5 == 0:
            return "imagenes/fondoAlfombravieja.png"
