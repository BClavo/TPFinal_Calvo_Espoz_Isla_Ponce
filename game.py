import pygame
import random
import numpy as np
from classes import Pajaro, Tuberia, crear_par_tuberias, Fondo
from algoritmo_genetico import Poblacion
from config import *

class Juego:
    """Clase principal que maneja toda la lógica del juego Flappy Bird Genético."""

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

        # Cargar imágenes
        self.cargar_imagenes()

        # Fondo
        self.fondo = Fondo(self.fondo_juego)

        # Grupos de sprites
        self.grupo_tuberias = pygame.sprite.Group()
        self.grupo_pajaros = pygame.sprite.Group()

        # Población
        self.pajaros = []
        self.poblacion = None
        self.inicializar_poblacion()

        # Estado del juego
        self.generation = 1
        self.best_fitness_ever = 0
        self.avg_fitness_history = []
        self.distancia_acumulada = 0

        # Inicializar tuberías
        self.generar_tuberias_iniciales()

        # Fuentes 
        self.font_title = pygame.font.Font(None, 36)
        self.font_text = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 22)
        self.font_graph = pygame.font.Font(None,20)


    def cargar_imagenes(self):
        """Carga y escala todas las imágenes del juego"""
        self.fondo_juego = pygame.image.load(SPRITE_PATHS['fondo']).convert_alpha()
        self.fondo_juego = pygame.transform.scale(self.fondo_juego, (GAME_WIDTH, HEIGHT))

        self.imagen_pajarito = pygame.image.load(SPRITE_PATHS['bird']).convert_alpha()
        self.imagen_pajarito = pygame.transform.scale(self.imagen_pajarito, (BIRD_SIZE, BIRD_SIZE))

        self.top_pipe_image = pygame.image.load(SPRITE_PATHS['pipe_top']).convert_alpha()
        self.top_pipe_image = pygame.transform.scale(self.top_pipe_image, (PIPE_WIDTH, HEIGHT))

        self.bottom_pipe_image = pygame.image.load(SPRITE_PATHS['pipe_bottom']).convert_alpha()
        self.bottom_pipe_image = pygame.transform.scale(self.bottom_pipe_image, (PIPE_WIDTH, HEIGHT))

        self.cadaver = pygame.image.load(SPRITE_PATHS['bird_dead']).convert_alpha()
        self.cadaver = pygame.transform.scale(self.cadaver, (BIRD_SIZE, BIRD_SIZE))
        # no le apliques alpha global aquí, se aplica en Pajaro.muerte()

    def inicializar_poblacion(self):
        """Crea la primera generación de pájaros"""
        self.pajaros = [
            Pajaro(imagen_vivo=self.imagen_pajarito, imagen_muerto=self.cadaver)
            for _ in range(NUM_PAJAROS)
        ]
        self.grupo_pajaros.empty()
        for b in self.pajaros:
            self.grupo_pajaros.add(b)
        self.poblacion = Poblacion(self.pajaros)
        self.pajaros_vivos=self.pajaros.copy()

    def generar_nueva_tuberia(self):
        """Genera un nuevo par de tuberías"""
        centro_gap = random.randint(MARGEN_VERTICAL, HEIGHT - MARGEN_VERTICAL)
        tuberia_top, tuberia_bottom = crear_par_tuberias(
            GAME_WIDTH, centro_gap, self.top_pipe_image, self.bottom_pipe_image
        )
        self.grupo_tuberias.add(tuberia_top, tuberia_bottom)

    def generar_tuberias_iniciales(self):
        """Genera el primer par de tuberías"""
        self.grupo_tuberias.empty()
        self.generar_nueva_tuberia()
        self.distancia_acumulada = 0

    def actualizar_tuberias(self):
        """Actualiza tuberías y genera nuevas cuando sea necesario"""
        self.distancia_acumulada += PIPE_SPEED
        if self.distancia_acumulada >= DISTANCIA_ENTRE_TUBERIAS:
            self.generar_nueva_tuberia()
            self.distancia_acumulada = 0

    def obtener_tuberia_cercana(self):
        """Obtiene la tubería más cercana adelante de los pájaros vivos"""
        if not self.pajaros_vivos:
            return None

        promedio_x = sum(b.rect.right for b in self.pajaros_vivos) / len(self.pajaros_vivos)
        pipes_front = [p for p in self.grupo_tuberias if p.rect.x + p.ancho > promedio_x]
        pipes_front.sort(key=lambda p: p.rect.x - promedio_x)

        return pipes_front[0] if pipes_front else None

    def actualizar_pajaros(self):
        """Actualiza la lógica de todos los pájaros vivos"""
        if not self.pajaros_vivos:
            return False
        
        next_pipe = self.obtener_tuberia_cercana()
        for pajaro in self.pajaros_vivos:
            if not pajaro.vivo:
                self.pajaros_vivos.remove(pajaro)
                continue
            if next_pipe and pajaro.decision_aleteo(next_pipe):
                pajaro.aletear()
            pajaro.actualizar_posicion()
            pajaro.verificar_colision_tuberia(self.grupo_tuberias)
            if next_pipe:
                pajaro.verificar_tuberia_pasada(next_pipe)
        return True

    def crear_nueva_generacion(self):
        """Crea una nueva generación mediante algoritmo genético"""
        for b in self.pajaros:
            b.calcular_fitness()

        current_best = max(b.fitness for b in self.pajaros)
        current_avg = sum(b.fitness for b in self.pajaros) / len(self.pajaros)

        if current_best > self.best_fitness_ever:
            self.best_fitness_ever = current_best

        self.avg_fitness_history.append(current_avg)

        self.poblacion = Poblacion(self.pajaros)
        self.pajaros = self.poblacion.crear_nueva_generacion(
            self.imagen_pajarito, self.cadaver
        )
        self.pajaros_vivos=self.pajaros.copy()
        self.grupo_pajaros.empty()
        for b in self.pajaros:
            self.grupo_pajaros.add(b)

        self.generation += 1
        self.generar_tuberias_iniciales()

    def dibujar_estadisticas_texto(self):
        """Dibuja el panel lateral de estadísticas"""
        pygame.draw.rect(self.screen, NEGRO, (GAME_WIDTH, 0, PANEL_WIDTH, HEIGHT))
        y = 20
        self.screen.blit(self.font_title.render("ESTADÍSTICAS", True, BLANCO), (GAME_WIDTH + 40, y))
        y += 60
        vivos = len(self.pajaros_vivos)
        tub_pas= max(b.tuberias_pasadas for b in self.pajaros_vivos) if vivos!=0 else 0
        stats = [
            (f"Generación: {self.generation}", VERDE),
            (f"Vivos: {vivos}/{NUM_PAJAROS}", BLANCO),
            (f"tuberías pasadas: {tub_pas}", BLANCO),
            (f"Mejor Fitness: {int(self.best_fitness_ever)}", AMARILLO)
        ]
        for text, color in stats:
            self.screen.blit(self.font_text.render(text, True, color), (GAME_WIDTH + 20, y))
            y += 40

    def dibujar_grafico_fitness(self):
        """Dibuja el grafico de fitness promedio vs generacion"""
        pygame.draw.rect(self.screen,GRAPH_BACKGROUND,GRAPH_RECT)
        pygame.draw.rect(self.screen, GRAPH_BORDER,GRAPH_RECT,2,border_radius=5)

        titulo = self.font_small.render("Fitness promedio vs generacion", True, VERDE)
        self.screen.blit(titulo, (GRAPH_RECT.x, GRAPH_RECT.y - 25)) #Copia el contenido y lo coloca en la pantalla

        data = self.avg_fitness_history #Uso el promedio previo
        if len(data) < 2:
            return None #Si es menor a 2 generaciones no puede formar un grafico

        #Eje Y:                                      #}
        max_fitness = max(data)                      #}
                                                     #}Normaliza los datos para graficarlos
        if max_fitness == 0: #}Evita dividir por 0   #}
            max_fitness = 1  #}                      #}
                                                     #}
        #Eje X:
        number_generations = len(data) - 1

        dots = []
        for i, fitness in enumerate(data):
            x = GRAPH_RECT.x + (i/ number_generations) * GRAPH_RECT.width #Se calcula la posicion del punto y se le suma al punto donde inicia el grafico
            y = GRAPH_RECT.bottom - (fitness/max_fitness) * GRAPH_RECT.height #Le resta al final del grafico segun que tan alto el fitness, colocando el punto mas alto segun su fitness

            dots.append((int(x), int(y)))

        if len(dots) >= 2:
            pygame.draw.lines(self.screen, AMARILLO, False, dots, 2)

    def dibujar_panel_lateral(self):
        """Coloca el panel lateral, con el texto y grafico"""

        pygame.draw.rect(self.screen, NEGRO, (GAME_WIDTH, 0, PANEL_WIDTH, HEIGHT))
        self.dibujar_estadisticas_texto()
        self.dibujar_grafico_fitness()




    def reiniciar(self):
        self.generation = 1
        self.best_fitness_ever = 0
        self.avg_fitness_history = []
        self.inicializar_poblacion()
        self.generar_tuberias_iniciales()

    def forzar_siguiente_generacion(self):
        for b in self.pajaros:
            b.vivo = False

    def actualizar(self):
        self.fondo.actualizar()
        self.actualizar_tuberias()
        self.grupo_tuberias.update()
        if not self.actualizar_pajaros():
            self.crear_nueva_generacion()

    def draw(self):
        self.fondo.dibujar(self.screen)
    
        self.grupo_tuberias.draw(self.screen)

        # Dibujar pájaros: primero los muertos, luego los vivos
        for pajaro in sorted(self.pajaros, key=lambda b: b.vivo):
            self.screen.blit(pajaro.image, pajaro.rect)

        self.dibujar_panel_lateral()

    def run(self):
        run = True
        while run and self.generation <= MAX_GENERATIONS:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    elif event.key == pygame.K_r:
                        self.reiniciar()
                    elif event.key == pygame.K_SPACE:
                        self.forzar_siguiente_generacion()
            self.actualizar()
            self.draw()
            pygame.display.flip()
        return self.generation, self.best_fitness_ever

