import pygame_menu
from pygame_menu.themes import Theme
from src import *
from src.nivel import Nivel


def pausa():

    fuente = pygame.font.SysFont('Bauhaus 93', 35)
    pausado = True

    while pausado:
        texto = fuente.render("Pause", False, (0, 0, 0))
        rectangulo = texto.get_rect()
        pantalla.blit(texto, ((ANCHO/2-rectangulo[2]+40), (ALTO/2-rectangulo[3])))
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_q:
                pausado = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pausado = False
        pygame.display.update()

    reloj.tick(15)


def main_supervivencia(pantalla):

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
    nivel_1 = Nivel(Nivel.traer_fondo_nivel(1), jugador, 1) # @staticmethod es una funcion que podemos llamar desde la clase pero no tiene acceso a ningun atributro de la clase)
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
                pausa()

        if not nivel_1.nivel_ganado() and not nivel_1.nivel_perdido():
            nivel_1.bucle_principal(pantalla, fuente, banderas)
        elif nivel_1.nivel_ganado():
            jugador.vaciar_ataques()
            nivel_1 = nivel_1.generar_proximo_nivel()
            # nivel_1 = Nivel(nivel_1.traer_fondo_nivel(nivel_1.numero+1), jugador, nivel_1.numero+1, items=nivel_1.items)
        # TODO AGREGAR LOGICA CUANDO PIERDA

        pygame.display.update()

        reloj.tick(15)


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    reloj = pygame.time.Clock()

    pantalla = pygame.display.set_mode(RESOLUCION)
    pygame.display.set_caption("Juego")
    icono = pygame.transform.scale(pygame.image.load("imagenes/jugador/down1.png"), (80, 80))
    pygame.display.set_icon(icono)
    fondo = pygame.transform.scale(pygame.image.load("imagenes/fondo.png"), (ANCHO, ALTO)).convert() # SACAR
    fuente = pygame.font.SysFont('Bauhaus 93', 25, False)

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
    menu.add_button('Modo supervivencia', main_supervivencia, pantalla)
    menu.add_button('Exit', pygame_menu.events.EXIT)
    menu.mainloop(pantalla)




