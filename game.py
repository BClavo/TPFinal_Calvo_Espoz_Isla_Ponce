"""
Módulo Principal de Lógica del Juego Flappy Bird Genético.

Aquí se gestiona el ciclo completo del juego, tanto en modo simulador 
(controlado mediante algoritmo genético) como en modo clásico 
(controlado por el jugador). Este módulo coordina la física, generación 
de tuberías, actualización de entidades, interfaz visual y transiciones 
entre generaciones.

Incluye:

- Clase Juego: controlador global del gameplay
- Generación y actualización de tuberías, pájaros y fondo
- Inicialización y control del algoritmo genético mediante Poblacion
- Panel lateral con estadísticas en tiempo real
- Gráficos de fitness y de evolución del genoma
- Lógica de Game Over, reinicio y velocidad dinámica
- Soporte para sonidos y música del juego

El ciclo del juego sigue los pasos:
    1. Actualizar estado (pájaros, tuberías, fondo)
    2. Detectar colisiones y calcular métricas
    3. Crear nueva generación (modo simulador)
    4. Dibujar escena completa y panel lateral
    5. Manejar entrada del jugador o algoritmo
"""
import pygame
import random
from classes import Pajaro, Tuberia, crear_par_tuberias, Fondo, Graph_manager, SoundManager
from algoritmo_genetico import Poblacion
from config import *

class Juego:
    """Clase principal que maneja toda la lógica del juego Flappy Bird Genético."""

    def __init__(self, screen:pygame.Surface,modo:str="simulador", estilo:str="default"):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps= FPS
        self.modo = modo
        self.estilo=estilo
        self.game_over = False

        # Contador de tiempo 
        self.start_time = pygame.time.get_ticks()

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
        self.max_pipes_ever= 0
        self.avg_fitness_history = []
        self.max_pipes_history= []
        self.distancia_acumulada = 0
        
        # Nuevas estadísticas
        self.distancia_actual = 0
        self.mejor_distancia = 0
        self.promedio_distancia_history = []

        # Inicializar tuberías
        self.generar_tuberias_iniciales()

        # Fuentes 
        self.font_title = pygame.font.Font(FONT_PATHS['flappyfont'], FONT_SIZES['subtitulo'])
        self.font_text = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)
        self.font_graph = pygame.font.Font(None,20)

        # Grafico de genoma 
        self.graph_gen = Graph_manager()

        # Musicalizacion 
        self.sound_manager = SoundManager() 
        self.sound_manager.play_music('game_music')

        #tecla de espacio para modo clasico
        self.espacio=False

        
    def cargar_imagenes(self):
        """Carga y escala todas las imágenes del juego"""
        self.fondo_juego = pygame.image.load(SPRITE_PATHS[self.estilo]['fondo']).convert_alpha()
        self.fondo_juego = pygame.transform.scale(self.fondo_juego, (GAME_WIDTH, HEIGHT))

        self.imagen_pajarito = pygame.image.load(SPRITE_PATHS[self.estilo]['bird']).convert_alpha()
        self.imagen_pajarito = pygame.transform.scale(self.imagen_pajarito, (BIRD_SIZE, BIRD_SIZE))

        self.top_pipe_image = pygame.image.load(SPRITE_PATHS[self.estilo]['pipe_top']).convert_alpha()
        self.top_pipe_image = pygame.transform.scale(self.top_pipe_image, (PIPE_WIDTH, HEIGHT))

        self.bottom_pipe_image = pygame.image.load(SPRITE_PATHS[self.estilo]['pipe_bottom']).convert_alpha()
        self.bottom_pipe_image = pygame.transform.scale(self.bottom_pipe_image, (PIPE_WIDTH, HEIGHT))

        self.cadaver = pygame.image.load(SPRITE_PATHS[self.estilo]['bird_dead']).convert_alpha()
        self.cadaver = pygame.transform.scale(self.cadaver, (BIRD_SIZE, BIRD_SIZE))
        
        # Cargar imagen específica de Game Over
        self.game_over_image = pygame.image.load(SPRITE_PATHS['game_over']).convert_alpha()
        # Escalar la imagen a un tamaño apropiado
        original_width = self.game_over_image.get_width()
        original_height = self.game_over_image.get_height()
        scale_factor = min(600 / original_width, 250 / original_height)
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        self.game_over_image = pygame.transform.scale(self.game_over_image, (new_width, new_height))
    

    def inicializar_poblacion(self):
        """Crea la primera generación de pájaros"""
        if self.modo=="simulador":
            self.pajaros = [
            Pajaro(imagen_vivo=self.imagen_pajarito, imagen_muerto=self.cadaver)
            for _ in range(NUM_PAJAROS)
        ]
        else: #si el modo es modo clasico, genera un solo pajaro
            self.pajaros = [
            Pajaro(imagen_vivo=self.imagen_pajarito, imagen_muerto=self.cadaver)
            ]
        #vacia la lista de pajaros de la generacion termianda
        self.grupo_pajaros.empty()
        for b in self.pajaros:
            self.grupo_pajaros.add(b)
        self.poblacion = Poblacion(self.pajaros)
        self.pajaros_vivos=self.pajaros.copy()
        self.genes_promedio = self.poblacion.promedio_genes
        self.desviacion = self.poblacion.desviacion_genes

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

    def obtener_tuberia_cercana(self)->Tuberia|None:
        """Obtiene la tubería más cercana adelante de los pájaros vivos"""
        if not self.pajaros_vivos:
            return None
        #toma la posicion en x de los pajaros
        promedio_x = sum(b.rect.right for b in self.pajaros_vivos) / len(self.pajaros_vivos)
        #toma las tuberias que estén a la derechas de los pajaros
        pipes_front = [p for p in self.grupo_tuberias if p.rect.x + p.ancho > promedio_x]
        #ordena las tuberias de mas cercana a mas lejana
        pipes_front.sort(key=lambda p: p.rect.x - promedio_x)
        #retorna la primer tuberia de la lista, la mas cercana
        return pipes_front[0] if pipes_front else None

    def actualizar_pajaros(self)-> bool:
        """Actualiza la lógica de todos los pájaros vivos"""
        if not self.pajaros_vivos:
            return False
        
        # Flag para controlar la reproducción de efectos de sonido una sola vez 
        sonido_muerte_reproducido = False
        sonido_tuberia_pasada = False 

        next_pipe = self.obtener_tuberia_cercana()
        for pajaro in self.pajaros_vivos:  
        # --- Capturar el estado antes de la actualización ---
            pajaro_estaba_vivo = pajaro.vivo
            #decide bajo que condiciones aletear en cada modo
            if self.modo=="simulador" :
                if next_pipe and pajaro.decision_aleteo(next_pipe):
                    pajaro.aletear()
                    self.sound_manager.play_sfx_limited('wing')
            elif self.modo=="clasico":
                if self.espacio:
                    pajaro.aletear()
                    self.espacio=False
                    self.sound_manager.play_sfx_limited('wing')
            pajaro.actualizar_posicion()
            muerte_caida = pajaro.verificar_limite_inferior()
            colision_tuberia = pajaro.verificar_colision_tuberia(self.grupo_tuberias)
            
            if next_pipe:
                tuberia_pasada = pajaro.verificar_tuberia_pasada(next_pipe)
                if not sonido_tuberia_pasada:
                    if tuberia_pasada and pajaro.tuberias_pasadas!=0:
                        self.sound_manager.play_sfx('point')
                        sonido_tuberia_pasada = True 

            if pajaro_estaba_vivo and not pajaro.vivo:
                    pajaro.tiempo_vivo = self.tiempo_transcurrido
                    if not sonido_muerte_reproducido:
                            if colision_tuberia:
                                self.sound_manager.play_sfx_limited('hit')
                            elif muerte_caida:
                                self.sound_manager.play_sfx('die')
                            sonido_muerte_reproducido = True
            
        self.pajaros_vivos = [p for p in self.pajaros_vivos if p.vivo]
        return True

    def crear_nueva_generacion(self):
        """Crea una nueva generación mediante algoritmo genético"""
        self.start_time = pygame.time.get_ticks() # Reiniciar tiempo de generación

        # Verificar si llegamos a MAX_GENERATIONS
        if self.generation >= MAX_GENERATIONS and self.modo == "simulador":
            self.game_over = True
            self.sound_manager.stop_music()
            self.sound_manager.play_music('game_over')
            return #corta la creacion de nuevas generaciones
        
        for b in self.pajaros:
            b.calcular_fitness()

        current_best = max(b.fitness for b in self.pajaros)
        current_avg = sum(b.fitness for b in self.pajaros) / len(self.pajaros)
        current_pipes= max(b.tuberias_pasadas for b in self.pajaros)
        
        # Actualizar estadísticas de distancia
        current_distancia = max(b.distancia for b in self.pajaros)
        promedio_distancia = sum(b.distancia for b in self.pajaros) / len(self.pajaros)
        
        self.distancia_actual = current_distancia
        if current_distancia > self.mejor_distancia:
            self.mejor_distancia = current_distancia
        
        self.promedio_distancia_history.append(promedio_distancia)

        if current_best > self.best_fitness_ever:
            self.best_fitness_ever = current_best
        
        if current_pipes > self.max_pipes_ever:
            self.max_pipes_ever = current_pipes

        self.avg_fitness_history.append(current_avg)
        self.max_pipes_history.append(current_pipes)

        #genera siguiente ronda
        if self.modo=="simulador":
            self.poblacion = Poblacion(self.pajaros)
            self.pajaros = self.poblacion.crear_nueva_generacion(
                self.imagen_pajarito, self.cadaver
            )
            poblacion_hijos_stats = Poblacion(self.pajaros)
            self.genes_promedio = poblacion_hijos_stats.promedio_genes
            self.desviacion = poblacion_hijos_stats.desviacion_genes
            self.pajaros_vivos=self.pajaros.copy()
            self.grupo_pajaros.empty()
        elif self.modo=="clasico":
            self.pajaros= [Pajaro(imagen_vivo=self.imagen_pajarito, imagen_muerto=self.cadaver)]
            self.pajaros_vivos=self.pajaros.copy()
            self.grupo_pajaros.empty()

            
        for b in self.pajaros:
            self.grupo_pajaros.add(b)

        self.generation += 1
        self.generar_tuberias_iniciales()

    def dibujar_estadisticas_texto(self):
        """Dibuja el panel lateral de estadísticas mejorado"""
        pygame.draw.rect(self.screen, NEGRO, (GAME_WIDTH, 0, PANEL_WIDTH, HEIGHT))
        y = 15
        
        # Título
        titulo = self.font_title.render("GA Estadisticas", True, TURQUESA)
        titulo_rect = titulo.get_rect(centerx=GAME_WIDTH + PANEL_WIDTH // 2)
        titulo_rect.y = y
        self.screen.blit(titulo, titulo_rect)
        y += 45
        
        # Línea separadora
        pygame.draw.line(self.screen,TURQUESA, 
                        (GAME_WIDTH + 10, y), 
                        (GAME_WIDTH + PANEL_WIDTH - 10, y), 2)
        y += 15
        
        vivos = len(self.pajaros_vivos)
        tub_pas= max(b.tuberias_pasadas for b in self.pajaros_vivos) if vivos!=0 else 0
        
        # Calcular distancia actual (máxima de los pájaros vivos)
        if vivos > 0:
            distancia_actual = max(b.distancia for b in self.pajaros_vivos)
        else:
            distancia_actual = 0
        
        # Calcular velocidad
        multiplicador = "X1" if self.clock.get_fps() < 90 else "X2"
        
        # Estadísticas en formato más compacto
        stats = [
            (f"Generación: {self.generation}", BLANCO),
            (f"Vivos: {vivos}/{NUM_PAJAROS}", VERDE if vivos > 0 else ROJO),

            (f"Tiempo Gen: {round(self.tiempo_transcurrido,2)}s", BLANCO),
            (f"Tuberias pasadas: {tub_pas}", BLANCO),
            (f"Velocidad: {multiplicador}", AMARILLO),
            "",  # Espaciador
            (f"Distancia actual: {distancia_actual}", BLANCO),
            (f"Distancia promedio: {int(self.promedio_distancia_history[-1]) if self.promedio_distancia_history else 0}", BLANCO),
            (f"Mejor distancia: {self.mejor_distancia}", AMARILLO),
            (f"Mejor fitness: {self.best_fitness_ever}", AMARILLO),

        ]
        
        for item in stats:
            if item == "":
                y += 10  # Espaciador
                continue
            text, color = item
            rendered = self.font_text.render(text, True, color)
            self.screen.blit(rendered, (GAME_WIDTH + 15, y))
            y += 22  # Reducido de 32 a 28 para dar más espacio abajo

    def dibujar_grafico_fitness(self):
        """Dibuja el grafico de fitness promedio vs generacion"""
        # Ajustar posición más abajo
        graph_rect_adjusted = pygame.Rect(GRAPH_RECT.x, GRAPH_RECT.y + 65, GRAPH_RECT.width, GRAPH_RECT.height)
        
        pygame.draw.rect(self.screen, GRAPH_BACKGROUND, graph_rect_adjusted)
        pygame.draw.rect(self.screen, GRAPH_BORDER, graph_rect_adjusted, 2, border_radius=5)
        #cambia el nombre segun el modo
        if self.modo=="simulador":
            titulo = self.font_small.render("Fitness promedio vs generación", True, TURQUESA)
        elif self.modo=="clasico":
            titulo = self.font_small.render("Tuberias vs ronda jugada", True, TURQUESA)

        self.screen.blit(titulo, (graph_rect_adjusted.x + 5, graph_rect_adjusted.y - 22)) # Copia el contenido y lo coloca en la pantalla

        data = self.avg_fitness_history if self.modo=="simulador" else self.max_pipes_history #Uso el promedio previo

        #dibuja el grafico solo si tiene suficientes puntos para hacer una linea
        if len(data) < 2:
            return None

        # Normalizar datos
        max_fitness = max(data)
        if max_fitness == 0:
            max_fitness = 1
                                                     
        number_generations = len(data) - 1

        #generacion del grafico acorde a la cntidad de generaciones hasta el momento
        dots = []
        for i, fitness in enumerate(data):
            x = graph_rect_adjusted.x + (i/ number_generations) * graph_rect_adjusted.width
            y = graph_rect_adjusted.bottom - (fitness/max_fitness) * graph_rect_adjusted.height
            dots.append((int(x), int(y)))

        if len(dots) >= 2:
            pygame.draw.lines(self.screen, AMARILLO, False, dots, 2)

    def dibujar_grafico_genes(self):
        """Dibuja el grafico de promedio y varianza de genes por generación"""
        self.graph_gen.update_graph(self.generation,self.genes_promedio,self.desviacion)
        graph_surface = self.graph_gen.surface 
        
        # reajusta el grafico al tamaño definido en la configuracion
        graph_rect_gen_adjusted = pygame.Rect(GRAPH_RECT_GEN.x, GRAPH_RECT_GEN.y + 70, GRAPH_RECT_GEN.width, GRAPH_RECT_GEN.height)
        
        #dibuja el grafico
        pygame.draw.rect(self.screen, (16,121,187), graph_rect_gen_adjusted)
        titulo = self.font_small.render("Genome (Avg ± Std)", True, TURQUESA)
        self.screen.blit(titulo, (graph_rect_gen_adjusted.x + 5, graph_rect_gen_adjusted.y - 18))

        self.screen.blit(graph_surface, (graph_rect_gen_adjusted.x, graph_rect_gen_adjusted.y))

    def dibujar_panel_lateral(self):
        """Coloca el panel lateral, con el texto y grafico"""
        pygame.draw.rect(self.screen, NEGRO, (GAME_WIDTH, 0, PANEL_WIDTH, HEIGHT))
        
        self.dibujar_estadisticas_texto()
        self.dibujar_grafico_fitness()
        if self.modo=="simulador":
            self.dibujar_grafico_genes()
    
    def dibujar_game_over(self):
        """Dibuja la pantalla de Game Over con estadísticas finales"""
        # Fondo negro
        self.screen.fill(NEGRO)
        
        # Imagen de Game Over (título)
        img_rect = self.game_over_image.get_rect(center=(WIDTH // 2, 150))
        self.screen.blit(self.game_over_image, img_rect)
        
        # Cuadro de estadísticas finales
        box_width = 400
        box_height = 300
        box_x = (WIDTH - box_width) // 2
        box_y = 250
        
        # Fondo del cuadro
        pygame.draw.rect(self.screen, (40, 40, 40), (box_x, box_y, box_width, box_height), border_radius=10)
        pygame.draw.rect(self.screen, NARANJA, (box_x, box_y, box_width, box_height), 3, border_radius=10)
        
        # Título del cuadro
        stats_title = self.font_title.render("ESTADISTICAS FINALES", True, TURQUESA)
        stats_title_rect = stats_title.get_rect(centerx=WIDTH // 2)
        stats_title_rect.y = box_y + 20
        self.screen.blit(stats_title, stats_title_rect)
        
        # Línea separadora
        pygame.draw.line(self.screen, TURQUESA, 
                        (box_x + 20, box_y + 60), 
                        (box_x + box_width - 20, box_y + 60), 2)
        
        # Estadísticas finales
        y_offset = box_y + 80
        promedio_final = int(self.promedio_distancia_history[-1]) if self.promedio_distancia_history else 0
        
        final_stats = [
            ("Generaciones completadas:", f"{self.generation}", BLANCO),
            ("Mejor fitness alcanzado:", f"{int(self.best_fitness_ever)}", BLANCO),
            ("Mejor distancia:", f"{self.mejor_distancia}", BLANCO),
            ("Promedio de distancia final:", f"{promedio_final}", BLANCO),
            ("Máximo de tuberías pasadas:", f"{self.max_pipes_ever}", BLANCO),
        ]
        
        for label, value, color in final_stats:
            # Label
            label_text = self.font_text.render(label, True, BLANCO)
            self.screen.blit(label_text, (box_x + 30, y_offset))
            
            # Value
            value_text = self.font_text.render(value, True, color)
            value_rect = value_text.get_rect(right=box_x + box_width - 30)
            value_rect.y = y_offset
            self.screen.blit(value_text, value_rect)
            
            y_offset += 45
        
        # Instrucciones
        y_offset += 20
        instructions = [
            "Presiona R para reiniciar",
            "Presiona ESC para volver al menú"
        ]
        
        for instruction in instructions:
            instr_text = self.font_small.render(instruction, True, (150, 150, 150))
            instr_rect = instr_text.get_rect(centerx=WIDTH // 2)
            instr_rect.y = y_offset
            self.screen.blit(instr_text, instr_rect)
            y_offset += 30

    def reiniciar(self):
        "devuelve todos los atributos a su estado inicial para comenzar de nuevo la simulacion"
        self.generation = 1
        self.best_fitness_ever = 0
        self.avg_fitness_history = []
        self.max_pipes_history=[]
        self.start_time = pygame.time.get_ticks()
        self.distancia_actual = 0
        self.mejor_distancia = 0
        self.promedio_distancia_history = []
        self.game_over = False
        self.sound_manager.stop_music()
        self.sound_manager.play_music('game_music')
        self.inicializar_poblacion()
        self.generar_tuberias_iniciales()

    def forzar_siguiente_generacion(self):
        "mata a todos los pajaros de la simulacion para ejecutar la siguiente generacion"
        for b in self.pajaros:
            b.vivo = False

    def actualizar(self):
        "actualiza el estado de todos los elementos de la simulacion si el juego no terminó aún"
        if self.game_over:
            return  # No actualizar si el juego terminó
        
        self.fondo.actualizar()
        self.actualizar_tuberias()
        self.grupo_tuberias.update()
        if not self.actualizar_pajaros():
            self.crear_nueva_generacion()

    def draw(self):
        "presenta en pantalla las imagenes, graficos, pajaros o mensajes necesarios para la simulacion"
        if self.game_over:
            self.dibujar_game_over()
            return #retorna unicamente el mensaje si el juego terminó
        
        self.fondo.dibujar(self.screen)
    
        self.grupo_tuberias.draw(self.screen)

        # Dibujar pájaros: primero los muertos, luego los vivos
        for pajaro in sorted(self.pajaros, key=lambda b: b.vivo):
            self.screen.blit(pajaro.image, pajaro.rect)

        self.dibujar_panel_lateral()

    def run(self):
        "corre el juego y maneja la interaccion con el usuario"
        run = True
        while run and self.generation <= MAX_GENERATIONS:
            self.clock.tick(self.fps)
            self.tiempo_transcurrido = (pygame.time.get_ticks() - self.start_time) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #corta el juego al tocar el bton de cerrar
                    run = False
                    self.sound_manager.stop_music()
                    self.sound_manager.play_music('menu_music', loop=-1)
                if event.type == pygame.KEYDOWN:
                    #regresa al menú con el escape
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        self.sound_manager.stop_music()
                        self.sound_manager.play_music('menu_music', loop=-1)
                    #reinicia la partida con la r
                    elif event.key == pygame.K_r:
                        self.reiniciar()
                    #usa el espacio para forzar la siguiente generación o saltar segun el modo
                    elif event.key == pygame.K_SPACE:
                        if self.modo=="simulador":
                            self.forzar_siguiente_generacion()
                        elif self.modo=="clasico":
                            self.espacio=True
                    #usa la tecla control para alterar la velocidad entre x1 y x2
                    elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        if self.modo=="simulador":
                            if self.clock.get_fps()<90:
                                self.fps*=2
                            elif self.clock.get_fps()>90:
                                self.fps=FPS
            #corta la generacion si supera los dos minutos
            if self.modo=="simulador" and self.tiempo_transcurrido>=MAX_TIME:
                self.forzar_siguiente_generacion()
            self.actualizar()
            self.draw()
            pygame.display.flip()
        #return self.generation, self.best_fitness_ever