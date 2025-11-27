import pygame
import numpy as np
from config import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt 

def rgb_to_mpl(rgb_tuple):
    """Convierte tuplas RGB (0-255) a Matplotlib (0.0-1.0)"""
    return tuple(c / 255.0 for c in rgb_tuple)

class Pajaro(pygame.sprite.Sprite):
    
    def __init__(self, genes=None, imagen_vivo=None, imagen_muerto=None):
        super().__init__()
        # Genética: 6 pesos para la red neuronal
        self.genes = genes if genes is not None else np.random.uniform(-3, 3, 6)
        
        # Imágenes
        self.imagen_vivo = imagen_vivo
        self.imagen_muerto = imagen_muerto
        self.image = self.imagen_vivo.copy() if imagen_vivo else None
        
        # Posición y física
        self.rect = self.image.get_rect() if self.image else pygame.Rect(0, 0, BIRD_SIZE, BIRD_SIZE)
        self.rect.x = WIDTH // 4
        self.rect.y = HEIGHT // 2
        self.vy = 0
        
        # Estado
        self.vivo = True
        
        # Métricas para fitness
        self.distancia = 0
        self.fitness = 0
        self.tiempo_vivo = 0
        self.tuberias_pasadas = -1
        self.ultima_tuberia_pasada = None

    def decision_aleteo(self, tuberia):
        """Decide si el pájaro debe aletear según su red neuronal simple."""
        
        # Normalizar entradas
        delta_x = (tuberia.rect.x - self.rect.right) / GAME_WIDTH
        delta_y = (tuberia.y_gap - self.rect.centery) / HEIGHT
        vy_norm = self.vy / 20
        
        # Desempaquetar genes 
        w0, w1, w2, w3, w4, w5 = self.genes
        
        # Calcular valor de decisión
        valor = (
            w0  
            + w1 * delta_y  
            + w2 * (delta_y ** 2)  
            + w3 * delta_x
            + w4 * (delta_x ** 2)  
            + w5 * vy_norm  
        )
        
        return valor > 0

    def aletear(self, fuerza=FLAP_STRENGTH):
        """Aplica la fuerza de aleteo al pájaro."""
        self.vy = fuerza

    def actualizar_posicion(self):
        """Actualiza la física y posición del pájaro."""
        if not self.vivo:
            return
            
        # Aplicar gravedad
        self.vy += GRAVITY
        self.rect.y += self.vy
        
        # Actualizar métricas
        self.tiempo_vivo += 1
        self.distancia += 1

        # Límite superior
        if self.rect.top <= 0:
            self.rect.top = 0

        

    def calcular_fitness(self):
        """
        Calcula el fitness del pájaro basado en:
        - Distancia recorrida
        - Tiempo de supervivencia
        - Número de tuberías pasadas (más importante)
        - Bonus por supervivencia prolongada
        """
        # Distancia recorrida
        fitness_distancia = self.distancia * 2
        
        # Tiempo de supervivencia
        fitness_tiempo = self.tiempo_vivo * 1.5

        # Tuberías pasadas (componente más importante)
        fitness_tuberias = self.tuberias_pasadas * BONUS_POR_TUBERIA
        
        # Bonus por supervivencia prolongada
        if self.tiempo_vivo > 300:
            bonus_supervivencia = (self.tiempo_vivo - 300) * 3
        else:
            bonus_supervivencia = 0
        
        # Fitness total
        self.fitness = (fitness_distancia + fitness_tiempo + 
                        bonus_supervivencia + fitness_tuberias)
        
        # Prevenir fitness negativo
        self.fitness = max(0, self.fitness)

    def muerte(self):
        """Cambia imagen y detiene al pájaro."""
        self.vivo = False
        self.vy = 0
        self.image = self.imagen_muerto.copy()
        self.image.set_alpha(51)  # opacidad baja, igual que tu versión original

    def verificar_limite_inferior(self):
    # Límite inferior (muerte)
        if self.rect.bottom >= HEIGHT:
            self.vivo = False
            self.muerte()          
            return True 
        return False  
    
    
    def verificar_colision_tuberia(self, grupo_tuberias):
        """Detecta colisión con alguna tubería."""
        if pygame.sprite.spritecollideany(self, grupo_tuberias):
            self.muerte()
            return True 
        return False

    def verificar_tuberia_pasada(self, tuberia):
        """Detecta si el pájaro ya pasó la tubería."""
        if self.ultima_tuberia_pasada != tuberia.id_tuberia:
            self.tuberias_pasadas += 1
            self.ultima_tuberia_pasada = tuberia.id_tuberia



class Tuberia(pygame.sprite.Sprite):
    """Representa una tubería (superior o inferior)."""

    def __init__(self, x_inicial, y_inicial, superior, imagen_top, imagen_bottom, id_tuberia):
        super().__init__()
        self.superior = superior
        self.velocidad = PIPE_SPEED
        self.ancho = PIPE_WIDTH
        self.image = imagen_top if superior else imagen_bottom
        self.rect = self.image.get_rect()
        self.rect.x = x_inicial
        self.rect.y = y_inicial
        self.id_tuberia = id_tuberia
        self.y_gap = y_inicial + PIPE_HEIGHT + (PIPE_GAP / 2) if superior else y_inicial - (PIPE_GAP / 2)

    def update(self):
        self.rect.x -= self.velocidad
        if self.rect.right < 0:
            self.kill()


def crear_par_tuberias(x_inicial, centro_gap, imagen_top, imagen_bottom):
    """Crea y devuelve un par (superior, inferior) de tuberías."""
    y_top = centro_gap - PIPE_GAP // 2 - PIPE_HEIGHT
    y_bottom = centro_gap + PIPE_GAP // 2
    id_tuberia = pygame.time.get_ticks()
    tuberia_top = Tuberia(x_inicial, y_top, True, imagen_top, imagen_bottom, id_tuberia)
    tuberia_bottom = Tuberia(x_inicial, y_bottom, False, imagen_top, imagen_bottom, id_tuberia)
    return tuberia_top, tuberia_bottom


class Fondo:
    """Crea un efecto de desplazamiento infinito en el fondo."""

    def __init__(self, imagen):
        self.imagen = imagen
        self.x1 = 0
        self.x2 = GAME_WIDTH
        self.velocidad = 2

    def actualizar(self):
        self.x1 -= self.velocidad
        self.x2 -= self.velocidad
        if self.x1 <= -GAME_WIDTH:
            self.x1 = self.x2 + GAME_WIDTH
        if self.x2 <= -GAME_WIDTH:
            self.x2 = self.x1 + GAME_WIDTH

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x1, 0))
        pantalla.blit(self.imagen, (self.x2, 0))


class Graph_manager():
    def __init__(self, size=(GRAPH_WIDTH,GRAPH_HEIGHT), labels=["w0", "w1(Δy)", "w2(Δy²)", "w3(Δx)", "w4(Δx²)", "w5(vy)"], 
                 title="Genome (Avg ± Std)"):
        self.size = size
        self.labels = labels
        self.title = title

        self.surface = None
        self.last_generation = None

        # Crear figura y eje una sola vez (optimización grande)
        fig_w = size[0] / 100
        fig_h = size[1] / 100
        self.fig, self.ax = plt.subplots(figsize=(fig_w, fig_h), dpi=100)

        # Estética base (no se repite cada vez)
        self.ax.set_title(self.title, fontsize=10)
        self.ax.axvline(0, color="white", linewidth=1)
        self.ax.grid(axis="x", alpha=0.2)
    

    def update_graph(self, generation, means, stds):
        """
        Genera la Surface SOLO si cambia de generación.
        """
        if generation == self.last_generation:
            return  # nada que actualizar

        self.last_generation = generation

        self.ax.clear()  # limpiar gráfico anterior
        self.fig.patch.set_facecolor(rgb_to_mpl(GRAPH_BACKGROUND)) 
        self.ax.set_facecolor(rgb_to_mpl(GRAPH_BACKGROUND)) #  color de fondo definido en config

        n = len(means)
        y = np.arange(n)

        for i in range(n):
            mean = means[i]
            std = stds[i]

            total_std_width = 2 * std
            start_pos = mean - std
            
            # Determinar el color de la media (para superponer)
            mean_color = "green" if mean >= 0 else "red"

            self.ax.barh(i, total_std_width, 
                left=start_pos, color="gray", 
                alpha=0.4
            )
            
            # Dibujar media sobre la barra gris (Barra Verde/Roja)
            self.ax.barh(i, abs(mean), left=min(0, mean), 
                color=mean_color, alpha=0.9)

            # texto numérico
            self.ax.text(
                -0.9,
                i,
                f"{mean:.2f}",
                va="center",
                fontsize=8,
                color="white"
            )

        # Etiquetas y estética
        self.ax.set_yticks(y)
        self.ax.set_yticklabels(self.labels,fontsize=10)
        # self.ax.set_title(self.title, fontsize=10)
        self.ax.axvline(0, color="white", linewidth=1)
        self.ax.grid(axis="x", alpha=0.2)
        # Margen vertical para separar barras de bordes up/down
        self.ax.set_xlim(min(self.ax.get_xlim()[0], -1), max(self.ax.get_xlim()[1], 1))

        # --- CONFIGURAR EL COLOR DE LAS ETIQUETAS DE LOS EJES ---
        self.ax.tick_params(axis='y', colors='turquoise') 
        self.ax.tick_params(axis='x', colors='turquoise')

        # Ajustar para que no se corte nada
        self.fig.subplots_adjust(left=0.3, right=0.95, top=0.95, bottom=0.20)

        # Renderizado en memoria
        self.fig.canvas.draw()
        raw_data = self.fig.canvas.buffer_rgba()

        w, h = self.fig.canvas.get_width_height()

        # Crear Surface de pygame (rápido)
        self.surface = pygame.image.frombuffer(raw_data, (w, h), "RGBA").convert()

        return self.surface 


class SoundManager:
    """Maneja la carga, reproducción y control de efectos de sonido."""

    def __init__(self):
        pygame.mixer.init()
        # Inicializa un número de canales (de config.py)
        pygame.mixer.set_num_channels(15) 
        self.sfx = {}

        # Cooldown para el sonido 'wing' para evitar saturación (en milisegundos)
        # 80ms limita el sonido a ~12 veces por segundo, lo que es mucho más limpio.
        self.wing_cooldown_ms = 80 
        self.hit_cooldown_ms = 150
        self.sfx_cooldowns = {}
        self.cargar_audio()

    def cargar_audio(self):
        try:
            #cargar efectos de sonido
            for name, path in AUDIO_PATHS.items():
                path = os.path.normpath(path)
                if name != 'music':
                    sound = pygame.mixer.Sound(path)
                    sound.set_volume(SFX_VOLUME)
                    self.sfx[name] = sound
        
        except pygame.error as e:
            print(f"Error al cargar el audio en SoundManager: {e}")
            print("Asegurate de que los archivos de audio estén en las rutas correctas.")
        
        # Guardar Paths de Música (para usar con pygame.mixer.music)
        self.music_paths = {
            'game_music': AUDIO_PATHS.get('game_music')
            # 'menu_music': AUDIO_PATHS.get('menu_music'),
        }
        pygame.mixer.music.set_volume(MUSIC_VOLUME)

    def play_sfx(self, name):
        """Reproduce un SFX inmediatamente."""
        if name in self.sfx:
            self.sfx[name].play()
            
    def play_sfx_limited(self, name, cooldown_ms=None):
        """
        Reproduce un SFX limitado por un cooldown. 
        Si no se especifica cooldown, usa el default (wing o hit).
        """
        if name not in self.sfx:
            return
        
        # Asigna el cooldown según el nombre del SFX
        if name == 'wing':
            cooldown = self.wing_cooldown_ms
        elif name == 'hit':
            cooldown = self.hit_cooldown_ms
        elif cooldown_ms is not None:
            cooldown = cooldown_ms
        else:
            # Si no tiene cooldown configurado, lo reproduce inmediatamente
            self.play_sfx(name) 
            return
        current_time = pygame.time.get_ticks()
        
        # Comprueba si ha pasado el tiempo de espera desde el último play
        if name not in self.sfx_cooldowns or \
           current_time - self.sfx_cooldowns[name] > cooldown:
            
            self.play_sfx(name)
            self.sfx_cooldowns[name] = current_time # Actualiza el tiempo  
    
    def play_music(self, name, loop=-1):
        """Carga y reproduce música. loop=-1 para repetición infinita."""
        path = self.music_paths[name]
        if path and os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(loop)
        elif path is None:
             print(f"Error: No se encontró la ruta para la música '{name}'")
    
    def stop_music(self):
        """Detiene la reproducción de la música."""
        pygame.mixer.music.stop()
        
    def pause_music(self):
        """Pausa la reproducción de la música."""
        pygame.mixer.music.pause()
        
    def unpause_music(self):
        """Reanuda la reproducción de la música."""
        pygame.mixer.music.unpause()