import pygame
from config import *
from game import Juego

class Boton:
    """Botón genérico con texto y detección de click."""
    def __init__(self, x, y, texto, ancho=220, alto=60, color_base=NARANJA, color_resaltado=BLANCO):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_base = color_base
        self.color_resaltado = color_resaltado
        self.color_actual = color_base
        self.fuente = pygame.font.Font(FONT_PATHS['flappyfont'], FONT_SIZES['subtitulo'])
    
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color_actual, self.rect, border_radius=12)
        texto_render = self.fuente.render(self.texto, True, NEGRO) # Convierte un texto en una imagen (Surface) que se puede dibujar en pantalla.
        texto_rect = texto_render.get_rect(center=self.rect.center)
        pantalla.blit(texto_render, texto_rect)

    def actualizar(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):   # Si el mouse está sobre el botón
            self.color_actual = self.color_resaltado
        else:
            self.color_actual = self.color_base

    def click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class BotonImagen:
    """Botón basado en imagen con detección de resaltado y click."""
    def __init__(self, x, y, imagen_path, escala=(210, 80)):
        self.imagen_original = pygame.image.load(imagen_path).convert_alpha()
        self.imagen_original = pygame.transform.scale(self.imagen_original, escala)
        self.imagen_resaltado = self._crear_resaltado(self.imagen_original)
        self.imagen_actual = self.imagen_original
        self.rect = self.imagen_actual.get_rect(topleft=(x, y))
        self.resaltado = False 

    def _crear_resaltado(self, imagen):
        """Crea una versión más brillante para mouse encima del boton."""
        resaltado_img = imagen.copy()
        resaltado_img.fill((255, 255, 255, 50), None, pygame.BLEND_RGBA_ADD)
        return resaltado_img

    def actualizar(self, mouse_pos):
        self.resaltado = self.rect.collidepoint(mouse_pos)
        self.imagen_actual = self.imagen_resaltado if self.resaltado else self.imagen_original

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen_actual, self.rect)

    def click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)



class MenuPrincipal:
    """Menú principal del juego."""
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.clock = pygame.time.Clock()
        self.fuente_titulo = pygame.font.Font(FONT_PATHS['flappyfont'], FONT_SIZES['titulo'])
        self.fuente_pregunta = pygame.font.Font(FONT_PATHS['flappyfont'], FONT_SIZES['subtitulo'])
        self.running = True

        # Botones principales con imágenes
        self.boton_play = BotonImagen(WIDTH // 2 - 110, 320, SPRITE_PATHS['jugar'])
        self.boton_personalizar = BotonImagen(WIDTH // 2 - 110, 410, SPRITE_PATHS['personalizar'])
        self.boton_salir = BotonImagen(WIDTH // 2 - 110, 500, SPRITE_PATHS['salir'])

        # Fondo
        self.fondo = pygame.image.load(SPRITE_PATHS['fondo']).convert()
        self.fondo = pygame.transform.scale(self.fondo, (WIDTH, HEIGHT))

        # Título y subtítulo como imágenes
        self.titulo_img = pygame.image.load(SPRITE_PATHS['titulo']).convert_alpha()
        self.titulo_img = pygame.transform.scale(self.titulo_img, (600, 150))
        self.titulo_rect = self.titulo_img.get_rect(center=(WIDTH // 2, 140))

        self.subtitulo_img = pygame.image.load(SPRITE_PATHS['subtitulo']).convert_alpha()
        self.subtitulo_img = pygame.transform.scale(self.subtitulo_img, (400, 100))
        self.subtitulo_rect = self.subtitulo_img.get_rect(
            center=(self.titulo_rect.centerx + 80, self.titulo_rect.bottom + 10)
        )

        # # Botones principales
        # centro_x = WIDTH // 2 - 110
        # self.boton_play = Boton(centro_x, 320, "Jugar")
        # self.boton_personalizar = Boton(centro_x, 410, "Personalizar", color_base=NARANJA)
        # self.boton_salir = Boton(centro_x, 500, "Salir", color_base=NARANJA)

        # Icono tuerca (configuración)
        self.icono_tuerca = pygame.image.load("sprites/gear.png").convert_alpha()
        self.icono_tuerca = pygame.transform.scale(self.icono_tuerca, (60, 60))
        self.rect_tuerca = self.icono_tuerca.get_rect(topright=(WIDTH - 20, 20))

        # Estado del menú
        self.mostrar_confirmacion = False
        self.mostrar_modo_juego = False


    def ejecutar(self):
        """Bucle principal del menú."""
        while self.running:
            self.clock.tick(FPS)
            self.pantalla.fill((20, 20, 30))
            mouse_pos = pygame.mouse.get_pos()

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Click en tuerca (configuración)
                    if self.rect_tuerca.collidepoint(mouse_pos):
                        self.mostrar_configuracion()
                    elif self.mostrar_confirmacion:
                        self.gestionar_confirmacion(mouse_pos)
                    elif self.mostrar_modo_juego:
                        self.gestionar_modo(mouse_pos)
                    elif self.boton_play.click(mouse_pos):
                        self.mostrar_modo_juego = True
                    elif self.boton_personalizar.click(mouse_pos):
                        self.mostrar_personalizar()
                    elif self.boton_salir.click(mouse_pos):
                        self.mostrar_confirmacion = True

            # Actualizar resaltado
            self.boton_play.actualizar(mouse_pos)
            self.boton_personalizar.actualizar(mouse_pos)
            self.boton_salir.actualizar(mouse_pos)

            # Dibujar interfaz
            self.dibujar()

            pygame.display.flip()


    def dibujar(self):
        """Dibuja la pantalla principal."""
        self.pantalla.blit(self.fondo, (0, 0))
        self.pantalla.blit(self.titulo_img, self.titulo_rect)
        self.pantalla.blit(self.subtitulo_img, self.subtitulo_rect)

        self.boton_play.dibujar(self.pantalla)
        self.boton_personalizar.dibujar(self.pantalla)
        self.boton_salir.dibujar(self.pantalla)
        self.pantalla.blit(self.icono_tuerca, self.rect_tuerca)

        # Cuadro de confirmación
        if self.mostrar_confirmacion:
            self.dibujar_confirmacion()
        elif self.mostrar_modo_juego:
            self.dibujar_modo()


    def dibujar_confirmacion(self):
        """Cuadro que pregunta si desea salir."""
        rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 80, 400, 160)
        pygame.draw.rect(self.pantalla, (40, 40, 50), rect, border_radius=12)
        texto = self.fuente_pregunta.render("¿Desea salir del juego?", True, BLANCO)
        self.pantalla.blit(texto, (rect.centerx - texto.get_width() // 2, rect.y + 30))

        self.boton_si = Boton(rect.centerx - 90, rect.y + 90, "Sí", 80, 40, color_base=VERDE)
        self.boton_no = Boton(rect.centerx + 10, rect.y + 90, "No", 80, 40, color_base=ROJO)
        self.boton_si.dibujar(self.pantalla)
        self.boton_no.dibujar(self.pantalla)


    def gestionar_confirmacion(self, mouse_pos):
        """Acciones al hacer clic en la confirmación de salida."""
        if self.boton_si.click(mouse_pos):
            self.running = False
        elif self.boton_no.click(mouse_pos):
            self.mostrar_confirmacion = False


    def dibujar_modo(self):
        """Submenú para elegir modo de juego."""
        rect = pygame.Rect(WIDTH // 2 - 220, HEIGHT // 2 - 100, 440, 200)
        pygame.draw.rect(self.pantalla, (40, 40, 50), rect, border_radius=12)
        texto = self.fuente_pregunta.render("Elegir modo de juego:", True, BLANCO)
        self.pantalla.blit(texto, (rect.centerx - texto.get_width() // 2, rect.y + 25))

        self.boton_simulador = Boton(rect.centerx - 100, rect.y + 80, "Simulador", 180, 45, AZUL)
        self.boton_clasico = Boton(rect.centerx - 100, rect.y + 135, "Clásico", 180, 45, VERDE)
        self.boton_simulador.dibujar(self.pantalla)
        self.boton_clasico.dibujar(self.pantalla)


    def gestionar_modo(self, mouse_pos):
        """Acciones al elegir modo de juego."""
        if self.boton_simulador.click(mouse_pos):
            juego = Juego(self.pantalla)
            juego.run()
            self.mostrar_modo_juego = False
        elif self.boton_clasico.click(mouse_pos):
            print("Modo clásico aún no implementado.")
            self.mostrar_modo_juego = False


    def mostrar_configuracion(self):
        """Muestra configuración (placeholder)."""
        print('Configuración: sonido, música, controles, etc')

    def mostrar_personalizar(self):
        """Muestra menú de personalización (placeholder)."""
        print('Personalización: temas y elementos visuales, etc')
