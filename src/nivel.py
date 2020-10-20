from random import randint
import pygame
from src.funciones import posicion_aleatoria_mapa
from src.enemigo import *
from src.configuracion import *
from src.spawn_point import SpawnPoint


class Nivel:
    def __init__(self, imagen_fondo, jugador, numero, cantidad_enemigos=3, respawn=10000, spawn_point_quantity=1, items=None,
                 velocidad_enemigos=2.0, vida_enemigos=60, danio_enemigos=1, cantidad_enemigos_spawn=1):
        self.numero = numero
        self.fondo = pygame.transform.scale(pygame.image.load(imagen_fondo), (ANCHO, ALTO)).convert()
        self.jugador = jugador
        self.enemigos = [Enemigo(pos_x=randint(1, int(ANCHO)), pos_y=randint(1, 500)) for _ in range(cantidad_enemigos)]
        self.items = items or []
        self.moneda = Moneda(ANCHO / 2, 0)
        self.respawn = respawn
        self.spawn_point_quantity = spawn_point_quantity
        self.ultimo_enemigo = pygame.time.get_ticks()
        self.velocidad_enemigos = velocidad_enemigos
        self.vida_enemigos = vida_enemigos
        self.danio_enemigos = danio_enemigos
        self.cantidad_enemigos_spawn = cantidad_enemigos_spawn
        self.spawn_points = [
            SpawnPoint(
                *posicion_aleatoria_mapa(),
                base_enemy_damage=self.danio_enemigos,
                base_enemy_health=self.vida_enemigos,
                base_enemy_speed=self.velocidad_enemigos,
                spawn_time=self.respawn,
                enemigo=Enemigo,
                spawn_amount=self.cantidad_enemigos_spawn
            )
            for _ in range(spawn_point_quantity)
        ]

    def bucle_principal(self, pantalla, fuente, banderas):
        pantalla.blit(self.fondo, (0, 0))

        if self.ultimo_enemigo + self.respawn <= pygame.time.get_ticks():
            self.spawn_enemies()

        self.moneda.dibujar(pantalla)
        texto_coins = fuente.render(f'{self.jugador.coins}', False, (0, 0, 0))
        pantalla.blit(texto_coins, (self.moneda.posicion.right, self.moneda.posicion.top))
        texto = fuente.render(f'Nivel: {self.numero}', False, (0, 0, 0))
        pantalla.blit(texto, (5, 0))

        self.jugador.procesar_accion(banderas)

        self.jugador.recorrer_imagenes()

        self.jugador.dibujar(pantalla)

        for spawn_point in self.spawn_points:
            spawn_point.dibujar(pantalla)

            for x in spawn_point.detectar_colision(reversed(self.jugador.lista_disparos)):
                self.jugador.lista_disparos.remove(x)
                self.jugador.golpear(spawn_point, x.poder_ataque)
                if spawn_point.vida <= 0:
                    self.spawn_points.remove(spawn_point)
                    # TODO Agregar drop

            for x in spawn_point.detectar_colision(reversed(self.jugador.lista_disparos_stun)):
                if not x.congelado:
                    x.congelar()
                # self.jugador.lista_disparos_stun.remove(x)
                    self.jugador.golpear(spawn_point, x.poder_ataque)
                    if spawn_point.vida <= 0:
                        self.spawn_points.remove(spawn_point)
                    #TODO agregar drop
                    for enemigo_congelacion in x.detectar_colision(reversed(self.enemigos)):
                        enemigo_congelacion.congelar(x.duracion_congelacion)
                        self.jugador.golpear(enemigo_congelacion, x.poder_ataque)
                        if enemigo_congelacion.vida <= 0:
                            self.enemigos.remove(enemigo_congelacion)

            for x in spawn_point.detectar_colision(reversed(self.jugador.lista_disparos_bomba)):
                if not x.explotado:
                    x.detonar()
                    for spawn_point_exposion in x.detectar_colision(reversed(self.spawn_points)):
                        self.jugador.golpear(spawn_point_exposion, x.poder_ataque)
                        if spawn_point_exposion.vida <= 0:
                            self.spawn_points.remove(spawn_point_exposion)
                            # TODO agregar drop

                    for enemigo_explosion in x.detectar_colision(reversed(self.enemigos)):
                        self.jugador.golpear(enemigo_explosion, x.poder_ataque)
                        if enemigo_explosion.vida <= 0:
                            if enemigo_explosion in self.enemigos:
                                self.enemigos.remove(enemigo_explosion)
                                # TODO agregar drop

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
                try:
                    self.jugador.lista_disparos.remove(x)
                except:
                    pass
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

            for x in enemigo.detectar_colision(reversed(self.jugador.lista_disparos_bomba)):
                if not x.explotado:
                    x.detonar()
                    for enemigo_explosion in x.detectar_colision(reversed(self.enemigos)):
                        self.jugador.golpear(enemigo_explosion, x.poder_ataque)
                        if enemigo_explosion.vida <= 0:
                            if enemigo_explosion in self.enemigos:
                                self.enemigos.remove(enemigo_explosion)
                                enemigo.morir(self.items)

                    for spawn_point_exposion in x.detectar_colision(reversed(self.spawn_points)):
                        self.jugador.golpear(spawn_point_exposion, x.poder_ataque)
                        if spawn_point_exposion.vida <= 0:
                            self.spawn_points.remove(spawn_point_exposion)
                            # TODO agregar drop

        for item_recogido in self.jugador.detectar_colision(self.items):
            if item_recogido.recoger(self.jugador):
                self.items.remove(item_recogido)
                pass
                # agregar sonido

        for item in self.items:
            item.dibujar(pantalla)

        return

    def nivel_ganado(self):
        return len(self.enemigos) == 0 and len(self.spawn_points) == 0

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

    def spawn_enemies(self):
        self.ultimo_enemigo = pygame.time.get_ticks()
        for spawn_point in self.spawn_points:
            spawn_point.spawn_enemy(self.enemigos)

    def generar_proximo_nivel(self):
        # TODO meter aleatoriedad, sino esto se vuelve imposible rapido
        proximo_numero = self.numero + 1
        fondo = self.traer_fondo_nivel(proximo_numero)
        cantidad_enemigos_iniciales = randint(1, 5)
        cantidad_puntos_aparicion = self.spawn_point_quantity + 1
        tiempo_respawn = self.respawn - 1000
        cantidad_enemigos_spawn = self.cantidad_enemigos_spawn + 1
        vida_enemigos = self.vida_enemigos + 10
        danio_enemigos = self.danio_enemigos + 1
        velocidad_enemigos = self.velocidad_enemigos + 0.5

        return Nivel(
            jugador=self.jugador,
            respawn=tiempo_respawn,
            numero=proximo_numero,
            spawn_point_quantity=cantidad_puntos_aparicion,
            cantidad_enemigos=cantidad_enemigos_iniciales,
            imagen_fondo=fondo,
            items=self.items,
            cantidad_enemigos_spawn=cantidad_enemigos_spawn,
            vida_enemigos=vida_enemigos,
            danio_enemigos=danio_enemigos,
            velocidad_enemigos=velocidad_enemigos
        )
