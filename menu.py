"""
Módulo de Menú Principal para Flappy Bird Genético.

Este módulo administra toda la interacción inicial del usuario con el juego,
incluyendo navegación entre pantallas, selección de modo de juego, 
personalización visual y confirmaciones de salida. Proporciona botones
interactivos y detección de clicks

Incluye:

- Botones estándar y botones basados en imágenes
- Menú principal con portada y música
- Submenú de selección de modo (Simulador / Clásico)
- Sistema de confirmación de salida
- Menú de personalización de estilo visual

El menú sigue un flujo básico:
    1. Mostrar portada y botones principales
    2. Detectar interacciones del jugador
    3. Cargar modos de juego o submenús
    4. Inicializar la clase Juego cuando corresponde
"""

import pygame
from config import *
from game import Juego
from classes import SoundManager

class Boton:
    """Botón genérico con texto y detección de click.

    Args:
        x (int): Posición horizontal.
        y (int): Posición vertical.
        texto (str): Texto mostrado en el botón.
        ancho (int): Ancho del botón.
        alto (int): Alto del botón.
        color_base (tuple[int,int,int]): Color base del botón.
        color_resaltado (tuple[int,int,int]): Color al resaltar.
    """

    def __init__(
            self,
            x: int,
            y: int,
            texto: str,
            ancho: int = 220,
            alto: int = 60,
            color_base=NARANJA,
            color_resaltado=BLANCO
    ):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_base = color_base
        self.color_resaltado = color_resaltado
        self.color_actual = color_base
        self.fuente = pygame.font.Font(FONT_PATHS['flappyfont'], FONT_SIZES['subtitulo'])

    def dibujar(self, pantalla: pygame.Surface) -> None:
        """Dibuja el botón en pantalla.

        Args:
            pantalla (pygame.Surface): Superficie donde dibujar.
        """
        pygame.draw.rect(pantalla, self.color_actual, self.rect, border_radius=12)
        texto_render = self.fuente.render(self.texto, True, NEGRO)
        texto_rect = texto_render.get_rect(center=self.rect.center)
        pantalla.blit(texto_render, texto_rect)

    def actualizar(self, mouse_pos: tuple[int, int]) -> None:
        """Actualiza el estado de resaltado del botón.

        Args:
            mouse_pos (tuple[int,int]): Posición actual del mouse.
        """
        if self.rect.collidepoint(mouse_pos):
            self.color_actual = self.color_resaltado
        else:
            self.color_actual = self.color_base

    def click(self, mouse_pos: tuple[int, int]) -> bool:
        """Verifica si el botón fue clickeado.

        Args:
            mouse_pos (tuple[int,int]): Posición del click.

        Returns:
            bool: True si se hizo click sobre el botón.
        """
        return self.rect.collidepoint(mouse_pos)


class BotonImagen:
    """Botón basado en imagen con detección de resaltado y click.

    Args:
        x (int): Posición horizontal.
        y (int): Posición vertical.
        imagen_path (str): Ruta de la imagen del botón.
        escala (tuple[int,int]): Tamaño redimensionado.
    """

    def __init__(self, x: int, y: int, imagen_path: str, escala: tuple[int, int] = (210, 80)):
        self.imagen_original = pygame.image.load(imagen_path).convert_alpha()
        self.imagen_original = pygame.transform.scale(self.imagen_original, escala)
        self.imagen_resaltado = self._crear_resaltado(self.imagen_original)
        self.imagen_actual = self.imagen_original
        self.rect = self.imagen_actual.get_rect(topleft=(x, y))
        self.resaltado = False

    def _crear_resaltado(self, imagen: pygame.Surface) -> pygame.Surface:
        """Crea una versión más brillante para mouse encima del botón.

        Args:
            imagen (pygame.Surface): Imagen original.

        Returns:
            pygame.Surface: Imagen resaltada.
        """
        #duplica la imagen y la pinta de blanco para resaltarla
        resaltado_img = imagen.copy()
        resaltado_img.fill((255, 255, 255, 50), None, pygame.BLEND_RGBA_ADD)
        return resaltado_img

    def actualizar(self, mouse_pos: tuple[int, int]) -> None:
        """Actualiza si el botón está resaltado.

        Args:
            mouse_pos (tuple[int,int]): Posición del mouse.
        """
        self.resaltado = self.rect.collidepoint(mouse_pos)
        self.imagen_actual = self.imagen_resaltado if self.resaltado else self.imagen_original

    def dibujar(self, pantalla: pygame.Surface) -> None:
        """Dibuja el botón en pantalla."""
        pantalla.blit(self.imagen_actual, self.rect)

    def click(self, mouse_pos: tuple[int, int]) -> bool:
        """Retorna True si se hizo click encima del botón."""
        return self.rect.collidepoint(mouse_pos)


class MenuPrincipal:
    """Menú principal del juego.

    Args:
        pantalla (pygame.Surface): Pantalla donde se renderiza.
    """

    def __init__(self, pantalla:pygame.Surface, estilo: str="default"):
        self.pantalla = pantalla
        self.clock = pygame.time.Clock()
        self.fuente_titulo = pygame.font.Font(FONT_PATHS['flappyfont'], FONT_SIZES['titulo'])
        self.fuente_pregunta = pygame.font.Font(FONT_PATHS['flappyfont'], FONT_SIZES['subtitulo'])
        self.running = True
        
        self.botones=True

        #creacion y adecuacion al tamaño de botones y texto
        self.boton_play = BotonImagen(WIDTH // 4 - 110 , 440, SPRITE_PATHS['jugar'])
        self.boton_personalizar = BotonImagen(WIDTH // 2 - 110, 440, SPRITE_PATHS['personalizar'])
        self.boton_salir = BotonImagen(WIDTH*3 // 4 - 110, 440, SPRITE_PATHS['salir'])

        self.estilo= estilo
        self.portada = pygame.image.load(SPRITE_PATHS[self.estilo]['fondo']).convert()
        self.portada = pygame.transform.scale(self.portada, (WIDTH, HEIGHT))

        self.titulo_img = pygame.image.load(SPRITE_PATHS['titulo']).convert_alpha()
        self.titulo_img = pygame.transform.scale(self.titulo_img, (600, 150))
        self.titulo_rect = self.titulo_img.get_rect(center=(WIDTH // 2, 140))

        self.subtitulo_img = pygame.image.load(SPRITE_PATHS['subtitulo']).convert_alpha()
        self.subtitulo_img = pygame.transform.scale(self.subtitulo_img, (400, 100))
        self.subtitulo_rect = self.subtitulo_img.get_rect(
            center=(self.titulo_rect.centerx + 80, self.titulo_rect.bottom + 10))

        self.icono_tuerca = pygame.image.load("sprites/gear.png").convert_alpha()
        self.icono_tuerca = pygame.transform.scale(self.icono_tuerca, (60, 60))
        self.rect_tuerca = self.icono_tuerca.get_rect(topright=(WIDTH - 20, 20))

        self.mostrar_confirmacion = False
        self.mostrar_modo_juego = False
        self.mostrar_personalizacion = False

        self.sound_manager = SoundManager() 
        self.sound_manager.play_music('menu_music') # <-- Inicia la música del juego

    def ejecutar(self) -> None:
        """Bucle principal del menú."""
        while self.running:
            self.clock.tick(FPS)
            self.pantalla.fill((20, 20, 30))
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #si se hace click izquierdo
                    #printea mensaje si se presiona la rueda
                    if self.rect_tuerca.collidepoint(mouse_pos):
                        self.sound_manager.play_sfx('click')
                        self.mostrar_configuracion()
                    #muestra el menu de confirmacion de salida si se presiona salir
                    elif self.boton_salir.click(mouse_pos):
                        self.sound_manager.play_sfx('click')
                        self.mostrar_confirmacion = True
                    #gestiona la eleccion de salir o no si el menu está abierto
                    elif self.mostrar_confirmacion:
                        self.gestionar_confirmacion(mouse_pos)
                    #muestra la seleccion de modo de juego si se presiona jugar
                    elif self.boton_play.click(mouse_pos):
                        self.sound_manager.play_sfx('click')
                        self.mostrar_modo_juego = True
                    #gestiona la seleccion del modo de juego si el menu está abierto
                    elif self.mostrar_modo_juego:
                        self.gestionar_modo(mouse_pos)
                    #muestra el menu de personalizacion si se presiona personalizar
                    elif self.boton_personalizar.click(mouse_pos):
                        self.sound_manager.play_sfx('click')
                        self.mostrar_personalizacion=True
                    #gestiona la personalizacion si el menu está abierto
                    elif self.mostrar_personalizacion:
                        self.gestionar_personalizacion(mouse_pos)
                    
                    
                    

            self.boton_play.actualizar(mouse_pos)
            self.boton_personalizar.actualizar(mouse_pos)
            self.boton_salir.actualizar(mouse_pos)

            self.dibujar()

            pygame.display.flip()

    def dibujar(self) -> None:
        """Dibuja todos los elementos del menú."""
        self.pantalla.blit(self.portada, (0, 0))
        self.pantalla.blit(self.titulo_img, self.titulo_rect)
        self.pantalla.blit(self.subtitulo_img, self.subtitulo_rect)

        if self.botones:
            self.boton_play.dibujar(self.pantalla)
            self.boton_personalizar.dibujar(self.pantalla)
            self.boton_salir.dibujar(self.pantalla)
            self.pantalla.blit(self.icono_tuerca, self.rect_tuerca)
        
        #dibuja el menu acorde al boton seleccionado
        if self.mostrar_confirmacion:
            self.dibujar_confirmacion()
        elif self.mostrar_modo_juego:
            self.dibujar_modo()
        elif self.mostrar_personalizacion:
            self.mostrar_estilos()

    def dibujar_confirmacion(self) -> None:
        """Dibuja el cuadro de confirmación de salida."""
        rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 80, 400, 160)
        pygame.draw.rect(self.pantalla, (40, 40, 50), rect, border_radius=12)
        texto = self.fuente_pregunta.render("Desea salir del juego", True, BLANCO)
        self.pantalla.blit(texto, (rect.centerx - texto.get_width() // 2, rect.y + 30))

        self.boton_si = Boton(rect.centerx - 90, rect.y + 90, "Si", 80, 40, color_base=VERDE)
        self.boton_no = Boton(rect.centerx + 10, rect.y + 90, "No", 80, 40, color_base=ROJO)
        self.boton_si.dibujar(self.pantalla)
        self.boton_no.dibujar(self.pantalla)

    def gestionar_confirmacion(self, mouse_pos: tuple[int, int]) -> None:
        """Gestiona la elección del cuadro de confirmación."""
        #corta si se elige salir del juego
        if self.boton_si.click(mouse_pos):
            self.sound_manager.play_sfx('click')
            self.running = False
        #deja de mostrar el menu si se elige que no
        elif self.boton_no.click(mouse_pos):
            self.sound_manager.play_sfx('click')
            self.mostrar_confirmacion = False

    def dibujar_modo(self) -> None:
        """Dibuja el submenú para elegir el modo de juego."""
        rect = pygame.Rect(WIDTH // 2 - 220, HEIGHT // 2 - 100, 440, 200)
        pygame.draw.rect(self.pantalla, (40, 40, 50), rect, border_radius=12)
        texto = self.fuente_pregunta.render("Modo de juego", True, BLANCO)
        self.pantalla.blit(texto, (rect.centerx - texto.get_width() // 2, rect.y + 25))

        self.boton_simulador = Boton(rect.centerx - 100, rect.y + 80, "Simulador", 180, 45, AZUL)
        self.boton_clasico = Boton(rect.centerx - 100, rect.y + 135, "Clasico", 180, 45, VERDE)
        self.boton_simulador.dibujar(self.pantalla)
        self.boton_clasico.dibujar(self.pantalla)

    def gestionar_modo(self, mouse_pos: tuple[int, int]) -> None:
        """Gestiona el click en la selección de modo."""
        #inicia el juego en modo simulador y deja de mostrar el menu
        if self.boton_simulador.click(mouse_pos):
            self.sound_manager.play_sfx('click')
            juego = Juego(self.pantalla,estilo=self.estilo)
            juego.run()
            self.mostrar_modo_juego = False
        #inicia el juego en modo clásico y deja de mostraar el menu
        elif self.boton_clasico.click(mouse_pos):
            self.sound_manager.play_sfx('click')
            juego = Juego(self.pantalla, "clasico",self.estilo)
            juego.run()
            self.mostrar_modo_juego = False

    def mostrar_configuracion(self) -> None:
        """Muestra el menú de configuración (placeholder)."""
        #no implementado
        print('Configuración: sonido, música, controles, etc')

    def mostrar_estilos(self) -> None:
        """Muestra el menú de personalización"""
        #mantiene el fondo pero quita los botones
        self.botones=False

        #genera lista de tematicas para la seleccion
        self.lista_tematicas=["default","espacio","agua","bosque","mitologia","stranger","udesa"]
        self.indice=self.lista_tematicas.index(self.estilo)
        self.ind_medio=self.indice
        self.ind_izq=self.ind_medio-1 if self.ind_medio-1 in range(len(self.lista_tematicas)) else -1
        self.ind_der=self.ind_medio+1 if self.ind_medio+1 in range(len(self.lista_tematicas)) else 0

        #oscurece el fondo
        fondo_negro = pygame.Surface((WIDTH, HEIGHT))   # crea superficie del tamaño de la pantalla
        fondo_negro.set_alpha(210)                      # ajusta transparencia (0=transparente, 255=opaco)
        fondo_negro.fill((0, 0, 0))                     # color negro
        self.pantalla.blit(fondo_negro, (0, 0))         # dibuja sobre la pantalla

        #genera los botones de las portadas, flechas y seleccion
        self.boton_medio= BotonImagen(WIDTH//2-120,90,SPRITE_PATHS[self.lista_tematicas[self.ind_medio]]['portada'],(240,120))
        self.boton_izq= BotonImagen(WIDTH//4-90,105,SPRITE_PATHS[self.lista_tematicas[self.ind_izq]]['portada'],(180,90))
        self.boton_der= BotonImagen(WIDTH*3//4-90,105,SPRITE_PATHS[self.lista_tematicas[self.ind_der]]['portada'],(180,90))
        self.flecha_izq= BotonImagen(50,125,SPRITE_PATHS["flechai"], (50,50))
        self.flecha_der= BotonImagen(WIDTH-100,125,SPRITE_PATHS["flechad"], (50,50))
        self.boton_elegir= Boton(WIDTH//2-110,HEIGHT-80,"Elegir",color_base=NARANJA)
        ###se planeaba dar funcionalidad a las portadas, de ahí que se generen como botones

        #muestra todos los elementos
        self.boton_medio.dibujar(self.pantalla)
        self.boton_izq.dibujar(self.pantalla)
        self.boton_der.dibujar(self.pantalla)
        self.flecha_izq.dibujar(self.pantalla)
        self.flecha_der.dibujar(self.pantalla)
        self.boton_elegir.dibujar(self.pantalla)

        #se muestra el personaje, tuberías y fondo si el estilo no es el de udesa
        if self.estilo!="udesa":
            #se genrra un borde blanco para resaltar el elemento respecto del fondo
            pygame.draw.rect(self.pantalla,BLANCO,((WIDTH//2)-53, (HEIGHT//2-3),106,106),3)
            pygame.draw.rect(self.pantalla,BLANCO,((WIDTH//4)-13, (HEIGHT//2-3),26,126),3)
            pygame.draw.rect(self.pantalla,BLANCO,((WIDTH*3//4)-78, (HEIGHT//2-3),156,81),3)

            #se adecuan los tamaños de las imagenes correspondientes al diccionario de estilos y se los muestra
            self.pj= pygame.image.load(SPRITE_PATHS[self.estilo]['bird']).convert()
            self.pj= pygame.transform.scale(self.pj, (100, 100))
            self.pipe= pygame.image.load(SPRITE_PATHS[self.estilo]['pipe_bottom']).convert()
            self.pipe= pygame.transform.scale(self.pipe, (20,120))
            self.fondo= pygame.image.load(SPRITE_PATHS[self.estilo]['fondo']).convert()
            self.fondo= pygame.transform.scale(self.fondo, (150, 75))

            self.pantalla.blit(self.pj,((WIDTH//2)-50, (HEIGHT//2)))
            self.pantalla.blit(self.pipe,((WIDTH//4)-10, (HEIGHT//2)))
            self.pantalla.blit(self.fondo,((WIDTH*3//4)-75, (HEIGHT//2)))
            
            self.pantalla.blit(self.fuente_pregunta.render("PERSONAJE",True,NARANJA),(WIDTH//2-60,HEIGHT//2+150))
            self.pantalla.blit(self.fuente_pregunta.render("TUBERIA",True,NARANJA),(WIDTH//4-45,HEIGHT//2+150))
            self.pantalla.blit(self.fuente_pregunta.render("FONDO",True,NARANJA),(WIDTH*3//4-40,HEIGHT//2+150))

  
    def gestionar_personalizacion(self, mouse:tuple[int,int]):
        """Gestiona el click en la selección de personalizacion."""

        if self.flecha_izq.click(mouse):
            #se redefine el estilo actual como el estilo de la izquierda
            #esto modifica que estilo aporta el fondo actualmente y es definido como el nuevo medio
            self.sound_manager.play_sfx('click')
            self.estilo = self.lista_tematicas[self.ind_izq]

            # Si es udesa → usar portada, si no → usar fondo
            if self.estilo == "udesa":
                self.portada = pygame.image.load(SPRITE_PATHS[self.estilo]['portada']).convert()
            else:
                self.portada = pygame.image.load(SPRITE_PATHS[self.estilo]['fondo']).convert()

            self.portada = pygame.transform.scale(self.portada, (WIDTH, HEIGHT))

        elif self.flecha_der.click(mouse):
            #se redefine el estilo actual como el estilo de la derecha
            #esto modifica que estilo aporta el fondo actualmente y es definido como el nuevo medio
            self.sound_manager.play_sfx('click')
            self.estilo = self.lista_tematicas[self.ind_der]

            # Si es udesa → usar portada, si no → usar fondo
            if self.estilo == "udesa":
                self.portada = pygame.image.load(SPRITE_PATHS[self.estilo]['portada']).convert()
            else:
                self.portada = pygame.image.load(SPRITE_PATHS[self.estilo]['fondo']).convert()

            self.portada = pygame.transform.scale(self.portada, (WIDTH, HEIGHT))

        #si se elige el estilo se sale del menu de personalizacion y muestra nuevamente los botones del menu principal
        elif self.boton_elegir.click(mouse):
            self.sound_manager.play_sfx('click')
            self.mostrar_personalizacion = False
            self.botones = True