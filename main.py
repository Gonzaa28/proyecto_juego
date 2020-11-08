import pygame_menu
from pygame_menu.themes import Theme
from src import *
from src.nivel import Nivel


class ItemShop:
    def __init__(self, imagen_item, alto, center_x, top_y, texto, precio, tipo_item, mejora):
        self.imagen_item = pygame.transform.scale(pygame.image.load(imagen_item), (60, alto))
        self.posicion = self.imagen_item.get_rect()
        self.posicion.centerx = center_x
        self.posicion.top = top_y

        self.fuente = pygame.font.SysFont('Bauhaus 93', 35)

        self.texto = fuente.render(texto, False, (0, 0, 0))
        self.texto_posicion = self.texto.get_rect()

        self.precio = fuente.render(str(precio), False, (0, 0, 0))
        self.precio_valor = precio
        self.precio_posicion = self.precio.get_rect()

        self.tipo_item = tipo_item
        self.mejora = mejora

        self.imagen_comprar = pygame.transform.scale(pygame.image.load('imagenes/bagofmoney.png'), (60, alto))
        self.posicion_imagen_comprar = self.imagen_comprar.get_rect()

        self.alinear_imagenes()

        self.rectangulo_x = self.posicion.left
        self.rectangulo_y = self.posicion.top
        self.rectangulo_ancho = self.posicion_imagen_comprar.right - self.posicion.left
        self.rectangulo_alto = self.posicion[3]

        self.rectangulo = pygame.Rect(self.rectangulo_x, self.rectangulo_y, self.rectangulo_ancho, self.rectangulo_alto)

        self.centrar_en_pantalla()

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, (0, 0, 0), (self.rectangulo.left - 5, self.rectangulo.top - 5,
                                               self.rectangulo.width + 10, self.rectangulo.height + 10))
        pygame.draw.rect(pantalla, (94, 184, 104), self.rectangulo)
        pantalla.blit(self.imagen_item, self.posicion)
        pantalla.blit(self.texto, self.texto_posicion)
        pantalla.blit(self.precio, self.precio_posicion)
        pantalla.blit(self.imagen_comprar, self.posicion_imagen_comprar)

    def centrar_en_pantalla(self):
        self.rectangulo.centerx = int(ANCHO / 2)
        self.posicion.left = self.rectangulo.left
        self.alinear_imagenes()

    def alinear_imagenes(self):
        self.texto_posicion.left = self.posicion.right
        self.texto_posicion.centery = self.posicion.centery
        self.precio_posicion.centery = self.posicion.centery
        self.precio_posicion.left = self.texto_posicion.right + 50
        self.posicion_imagen_comprar.centery = self.posicion.centery
        self.posicion_imagen_comprar.left = self.precio_posicion.right

    def comprar(self, jugador):
        if jugador.coins - self.precio_valor >= 0:
            jugador.coins -= self.precio_valor
            if self.tipo_item == ITEM_PODER_ATAQUE:
                jugador.poder_ataque += self.mejora
            if self.tipo_item == ITEM_VELOCIDAD:
                jugador.velocidad += self.mejora
            if self.tipo_item == ITEM_VIDA:
                jugador.vida_inicial += self.mejora
                jugador.vida = jugador.vida_inicial


def pausa(banderas, jugador, nivel, fuente):
    banderas['w_bandera'] = False
    banderas['d_bandera'] = False
    banderas['s_bandera'] = False
    banderas['a_bandera'] = False
    banderas['space_bandera'] = False
    banderas['f_bandera'] = False
    banderas['r_bandera'] = False
    banderas['v_bandera'] = False

    fuente = pygame.font.SysFont('Bauhaus 93', 35)
    pausado = True

    lista_items = [ItemShop('imagenes/sword.png', 60, int(ANCHO / 2), 100, 'Poder ataque', 10, ITEM_PODER_ATAQUE, 5)]
    lista_items.append(
        ItemShop('imagenes/wing.png', 60, int(ANCHO / 2), lista_items[-1].rectangulo.bottom + 15, 'Velocidad      ',
                 10, ITEM_VELOCIDAD, 5))
    lista_items.append(ItemShop('imagenes/items/heart.png', 60, int(ANCHO / 2), lista_items[-1].rectangulo.bottom + 15,
                                'Vida               ',
                                10, ITEM_VIDA, 5))

    while pausado:
        pantalla.blit(nivel.fondo, (0, 0))
        texto = fuente.render("Pausa/Tienda", False, (0, 0, 0))
        rectangulo = texto.get_rect()
        pantalla.blit(texto, (0, 0))
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_q:
                pausado = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pausado = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for item in lista_items:
                    if item.posicion_imagen_comprar.collidepoint(pygame.mouse.get_pos()):
                        item.comprar(jugador)

        for item in lista_items:
            item.dibujar(pantalla)

        nivel.moneda.dibujar(pantalla)
        texto_coins = fuente.render(f'{jugador.coins}', False, (0, 0, 0))
        pantalla.blit(texto_coins, (nivel.moneda.posicion.right, nivel.moneda.posicion.top))

        pygame.display.update()

    for s in nivel.spawn_points:
        s.last_spawn_time = pygame.time.get_ticks()

    nivel.ultimo_enemigo = pygame.time.get_ticks()


def main_supervivencia(pantalla, fuente):
    banderas = {
        'w_bandera': False,
        'd_bandera': False,
        's_bandera': False,
        'a_bandera': False,
        'space_bandera': False,
        'f_bandera': False,
        'r_bandera': False,
        'v_bandera': False
    }

    jugador = Jugador()
    nivel = Nivel(Nivel.traer_fondo_nivel(1), jugador,
                  1)  # @staticmethod es una funcion que podemos llamar desde la clase pero no tiene acceso a ningun atributro de la clase)

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
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                banderas['r_bandera'] = True
            if evento.type == pygame.KEYUP and evento.key == pygame.K_r:
                banderas['r_bandera'] = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_v:
                banderas['v_bandera'] = True
            if evento.type == pygame.KEYUP and evento.key == pygame.K_v:
                banderas['v_bandera'] = False

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_p:
                pausa(banderas, jugador, nivel, fuente)

        if not nivel.nivel_ganado() and not nivel.nivel_perdido():
            nivel.bucle_principal(pantalla, fuente, banderas)
        elif nivel.nivel_ganado():
            jugador.vaciar_ataques()
            nivel = nivel.generar_proximo_nivel()
        # TODO AGREGAR LOGICA CUANDO PIERDA
        elif nivel.nivel_perdido():
            corriendo = False

        pygame.display.update()

        reloj.tick(15)


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    reloj = pygame.time.Clock()

    pantalla = pygame.display.set_mode(RESOLUCION)
    pygame.display.set_caption("Survival")
    icono = pygame.transform.scale(pygame.image.load("imagenes/jugador/down1.png"), (80, 80))
    pygame.display.set_icon(icono)
    fondo = pygame.transform.scale(pygame.image.load("imagenes/fondo.png"), (ANCHO, ALTO)).convert()  # SACAR
    fuente = pygame.font.SysFont('Bauhaus 93', 30, False)

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
                 title_offset=(ANCHO / 2 - 140, 10),
                 widget_background_color=(0, 0, 0, 0),
                 widget_font=pygame_menu.font.FONT_MUNRO,
                 widget_font_antialias=True,
                 widget_font_color=(75, 75, 75),
                 widget_font_size=40,
                 widget_selection_effect=pygame_menu.widgets.selection.LeftArrowSelection(blink_ms=300),
                 widget_shadow=True,
                 widget_shadow_color=(75, 75, 75),
                 widget_shadow_offset=2)

    tema_ayuda = Theme(background_color=imagen,
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
                       title_offset=(ANCHO / 2 - 100, 10),
                       widget_background_color=(0, 0, 0, 0),
                       widget_font=pygame_menu.font.FONT_MUNRO,
                       widget_font_antialias=True,
                       widget_font_color=(75, 75, 75),
                       widget_font_size=40,
                       widget_selection_effect=pygame_menu.widgets.selection.LeftArrowSelection(blink_ms=300),
                       widget_shadow=True,
                       widget_shadow_color=(75, 75, 75),
                       widget_shadow_offset=2)

    menu = pygame_menu.Menu(600, 800, 'Survival', theme=tema)
    help_menu = pygame_menu.Menu(600, 800, 'Ayuda', theme=tema_ayuda)
    AYUDAS = {
        "mov": "Movimientos",
        "w": "Presione W para correr hacia arriba",
        "d": "Presione D para correr hacia la derecha",
        "a": "Presione A para correr hacia la izquierda",
        "s": "Presione S para correr hacia abajo",
        "dis": "Disparos",
        "space": "Presione SPACE para disparo simple",
        "f": "Presione F para disparo infinito",
        "r": "Presione R para disparo explosivo",
        "v": "Presione V para disparo congelador",
    }
    help_menu.add_label(AYUDAS["mov"], max_char=-1, font_size=33, aling=pygame_menu.locals.ALIGN_RIGHT,
                        font_color=(0, 0, 0))
    help_menu.add_label(AYUDAS["w"], max_char=-1, font_size=33, aling=pygame_menu.locals.ALIGN_RIGHT,
                        font_color=(0, 0, 0))
    help_menu.add_label(AYUDAS["d"], max_char=-1, font_size=33, aling=pygame_menu.locals.ALIGN_RIGHT,
                        font_color=(0, 0, 0))
    help_menu.add_label(AYUDAS["a"], max_char=-1, font_size=33, aling=pygame_menu.locals.ALIGN_RIGHT,
                        font_color=(0, 0, 0))
    help_menu.add_label(AYUDAS["s"], max_char=-1, font_size=33, aling=pygame_menu.locals.ALIGN_RIGHT,
                        font_color=(0, 0, 0))
    help_menu.add_label(AYUDAS["dis"], max_char=-1, font_size=33, aling=pygame_menu.locals.ALIGN_RIGHT,
                        font_color=(0, 0, 0))
    help_menu.add_label(AYUDAS["space"], max_char=-1, font_size=33, aling=pygame_menu.locals.ALIGN_RIGHT,
                        font_color=(0, 0, 0))
    help_menu.add_label(AYUDAS["f"], max_char=-1, font_size=33, aling=pygame_menu.locals.ALIGN_RIGHT,
                        font_color=(0, 0, 0))
    help_menu.add_label(AYUDAS["r"], max_char=-1, font_size=33, aling=pygame_menu.locals.ALIGN_RIGHT,
                        font_color=(0, 0, 0))
    help_menu.add_label(AYUDAS["v"], max_char=-1, font_size=33, aling=pygame_menu.locals.ALIGN_RIGHT,
                        font_color=(0, 0, 0))

    help_menu.add_button('Volver', pygame_menu.events.BACK)
    # menu.add_selector('Dificultad: ', [('Dificil', 1), ('Medio', 2), ('Facil', 3)])
    menu.add_text_input('Nombre: ')
    menu.add_button('Jugar', main_supervivencia, pantalla, fuente)
    menu.add_button('Ayuda', help_menu)
    menu.add_button('Salir', pygame_menu.events.EXIT)
    menu.mainloop(pantalla)
