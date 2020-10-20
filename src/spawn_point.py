import pygame

from src.enemigo import Enemigo
from src.objeto_juego import ObjetoJuego, QUIETO


class SpawnPoint(ObjetoJuego):
    def __init__(self, pos_x, pos_y, vida_inicial=50, spawn_time=8000, enemigo=Enemigo, base_enemy_health=50,
                 base_enemy_damage=1, spawn_amount=1, base_enemy_speed=1):
        imagenes = {
            QUIETO: [pygame.transform.scale(pygame.image.load("imagenes/grave.png"), (30, 60))]
        }
        super(SpawnPoint, self).__init__(pos_x=pos_x, pos_y=pos_y, imagenes=imagenes, estado=QUIETO, animacion=0,
                                         velocidad=0, vida_inicial=vida_inicial)
        self.spawn_time = spawn_time
        self.enemy = enemigo
        self.last_spawn_time = pygame.time.get_ticks()
        self.enemy_base_health = base_enemy_health
        self.enemy_base_damage = base_enemy_damage
        self.enemy_spawn_amount = spawn_amount
        self.enemy_base_speed = base_enemy_speed

    def dibujar(self, pantalla):
        super(SpawnPoint, self).dibujar(pantalla)
        pygame.draw.rect(pantalla, (255, 0, 0), (self.posicion[0], self.posicion[1] - 10, self.vida_inicial, 5))
        pygame.draw.rect(pantalla, (0, 255, 0), (self.posicion[0], self.posicion[1] - 10, self.vida, 5))

    def spawn_enemy(self, enemy_list):
        for _ in range(self.enemy_spawn_amount):
            enemy_list.append(self.enemy(
                self.posicion.left,
                self.posicion.top,
                vida_inicial=self.enemy_base_health,
                danio=self.enemy_base_damage,
                velocidad=self.enemy_base_speed
            ))
