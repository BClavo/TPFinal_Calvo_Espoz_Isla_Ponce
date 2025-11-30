import pygame
import numpy as np
from config import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def rgb_to_mpl(rgb_tuple: tuple[int, int, int]) -> tuple[float, float, float]:
    """Convierte tuplas RGB (0-255) a Matplotlib (0.0-1.0).

    Args:
        rgb_tuple (tuple[int,int,int]): Tupla RGB estándar.

    Returns:
        tuple[float,float,float]: Tupla normalizada para Matplotlib.
    """
    return tuple(c / 255.0 for c in rgb_tuple)


class Pajaro(pygame.sprite.Sprite):
    """
    Representa un pájaro con genes(forma de arreglo), física y métricas para el algoritmo genetico.

    Args:
        genes (np.ndarray | None): Vector de 6 pesos del pájaro.
        imagen_vivo: Imagen cuando el pájaro está vivo.
        imagen_muerto: Imagen cuando el pájaro está muerto.
    """

    def __init__(self, genes=None, imagen_vivo=None, imagen_muerto=None):
        super().__init__()
        self.genes = genes if genes is not None else np.random.uniform(-1.5, 1.5, 6)

        self.imagen_vivo = imagen_vivo
        self.imagen_muerto = imagen_muerto
        self.image = self.imagen_vivo.copy() if imagen_vivo else None

        self.rect = self.image.get_rect() if self.image else pygame.Rect(0, 0, BIRD_SIZE, BIRD_SIZE)
        self.rect.x = WIDTH // 4
        self.rect.y = HEIGHT // 2
        self.vy = 0

        self.vivo = True
        self.distancia = 0
        self.fitness = 0
        self.tiempo_vivo = 0
        self.tuberias_pasadas = -1
        self.ultima_tuberia_pasada = None

    def decision_aleteo(self, tuberia) -> bool:
        """
        Decide si el pájaro debe aletear usando sus genes y una formula.

        Args:
            tuberia (Tuberia): Tubería próxima que sirve como entrada.

        Returns:
            bool: True si debe aletear.
        """

        delta_x = (tuberia.rect.x - self.rect.right) / GAME_WIDTH
        delta_y = (tuberia.y_gap - self.rect.centery) / HEIGHT
        vy_norm = self.vy / 20

        w0, w1, w2, w3, w4, w5 = self.genes

        valor = (
                w0
                + w1 * delta_y
                + w2 * (delta_y ** 2)
                + w3 * delta_x
                + w4 * (delta_x ** 2)
                + w5 * vy_norm
        )

        return valor > 0

    def aletear(self, fuerza: float = FLAP_STRENGTH) -> None:
        """
        Aplica fuerza hacia arriba.

        Args:
            fuerza (float): Impulso vertical.
        """
        self.vy = fuerza

    def actualizar_posicion(self) -> None:
        """Actualiza la posición del pájaro y sus métricas."""
        if not self.vivo:
            return

        self.vy += GRAVITY
        self.rect.y += self.vy

        self.distancia += 1

        if self.rect.top <= 0:
            self.rect.top = 0

    def calcular_fitness(self) -> None:
        """
        Calcula el fitness combinando:
        - Distancia recorrida
        - Tiempo vivo
        - Tuberías pasadas (más importante)
        - Bonus por supervivencia prolongada
        """
        fitness_distancia = self.distancia * 1.5
        fitness_tuberias = self.tuberias_pasadas * BONUS_POR_TUBERIA

        if self.tiempo_vivo > 300:
            bonus_supervivencia = (self.tiempo_vivo - 300) * 3
        else:
            bonus_supervivencia = 0

        self.fitness = (
                fitness_distancia +
                bonus_supervivencia +
                fitness_tuberias
        )

        self.fitness = max(0, self.fitness)

    def muerte(self) -> None:
        """Detiene al pájaro y cambia su imagen a modo muerto."""
        self.vivo = False
        self.vy = 0
        self.image = self.imagen_muerto.copy()
        self.image.set_alpha(51)

    def verificar_limite_inferior(self) -> bool:
        """
        Verifica si el pájaro toca el piso.

        Returns:
            bool: True si el pájaro muere por tocar el límite inferior.
        """
        if self.rect.bottom >= HEIGHT:
            self.vivo = False
            self.muerte()
            return True
        return False

    def verificar_colision_tuberia(self, grupo_tuberias) -> bool:
        """
        Verifica colisión del pájaro con tuberías.

        Args:
            grupo_tuberias (pygame.sprite.Group): Grupo de tuberías.

        Returns:
            bool: True si colisiona.
        """
        if pygame.sprite.spritecollideany(self, grupo_tuberias):
            self.muerte()
            return True
        return False

    def verificar_tuberia_pasada(self, tuberia) -> None:
        """
        Detecta si el pájaro pasó una tubería.

        Args:
            tuberia (Tuberia): La tubería revisada.
        """
        if self.ultima_tuberia_pasada != tuberia.id_tuberia:
            self.tuberias_pasadas += 1
            self.ultima_tuberia_pasada = tuberia.id_tuberia
            return True 
        return False


class Tuberia(pygame.sprite.Sprite):
    """
    Representa una tubería superior o inferior.

    Args:
        x_inicial (int): Posición inicial en X.
        y_inicial (int): Posición inicial en Y.
        superior (bool): Si es la tubería superior.
        imagen_top: Imagen para tubería superior.
        imagen_bottom: Imagen para tubería inferior.
        id_tuberia (int): Identificador único por par.
    """

    def __init__(self, x_inicial: int, y_inicial: int, superior: bool, imagen_top, imagen_bottom, id_tuberia: int):
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

    def update(self) -> None:
        """Desplaza la tubería hacia la izquierda y la elimina si sale de pantalla."""
        self.rect.x -= self.velocidad
        if self.rect.right < 0:
            self.kill()


def crear_par_tuberias(
        x_inicial: int,
        centro_gap: int,
        imagen_top,
        imagen_bottom
) -> tuple['Tuberia', 'Tuberia']:
    """
    Crea un par de tuberías (superior e inferior).

    Args:
        x_inicial (int): Posición horizontal inicial.
        centro_gap (int): Centro vertical del hueco.
        imagen_top: Imagen para tubería superior.
        imagen_bottom: Imagen para tubería inferior.

    Returns:
        tuple[Tuberia,Tuberia]: Par de tuberías.
    """
    y_top = centro_gap - PIPE_GAP // 2 - PIPE_HEIGHT
    y_bottom = centro_gap + PIPE_GAP // 2
    id_tuberia = pygame.time.get_ticks()
    tuberia_top = Tuberia(x_inicial, y_top, True, imagen_top, imagen_bottom, id_tuberia)
    tuberia_bottom = Tuberia(x_inicial, y_bottom, False, imagen_top, imagen_bottom, id_tuberia)
    return tuberia_top, tuberia_bottom


class Fondo:
    """
    Crea un efecto de desplazamiento infinito en el fondo.

    Args:
        imagen (pygame.Surface): Imagen del fondo.
    """

    def __init__(self, imagen):
        self.imagen = imagen
        self.x1 = 0
        self.x2 = GAME_WIDTH
        self.velocidad = 2

    def actualizar(self) -> None:
        """Actualiza posiciones del fondo para efecto infinito."""
        self.x1 -= self.velocidad
        self.x2 -= self.velocidad
        if self.x1 <= -GAME_WIDTH:
            self.x1 = self.x2 + GAME_WIDTH
        if self.x2 <= -GAME_WIDTH:
            self.x2 = self.x1 + GAME_WIDTH

    def dibujar(self, pantalla) -> None:
        """
        Dibuja el fondo desplazado.

        Args:
            pantalla (pygame.Surface): Superficie donde dibujar.
        """
        pantalla.blit(self.imagen, (self.x1, 0))
        pantalla.blit(self.imagen, (self.x2, 0))


class Graph_manager:
    """
    Administra la generación del gráfico del genoma.

    Args:
        size (tuple[int,int]): Tamaño del gráfico.
        labels (list[str]): Etiquetas de cada gen.
        title (str): Título del gráfico.
    """

    def __init__(self, size=(GRAPH_WIDTH, GRAPH_HEIGHT),
                 labels=["w0", "w1(Δy)", "w2(Δy²)", "w3(Δx)", "w4(Δx²)", "w5(vy)"],
                 title="Genome (Avg ± Std)"):
        self.size = size
        self.labels = labels
        self.title = title

        self.surface = None
        self.last_generation = None

        fig_w = size[0] / 100
        fig_h = size[1] / 100
        self.fig, self.ax = plt.subplots(figsize=(fig_w, fig_h), dpi=100)

        self.ax.set_title(self.title, fontsize=10)
        self.ax.axvline(0, color="white", linewidth=1)
        self.ax.grid(axis="x", alpha=0.2)

    def update_graph(self, generation: int, means: np.ndarray, stds: np.ndarray):
        """
        Actualiza el gráfico solo si cambia la generación.

        Args:
            generation (int): Número de generación.
            means (np.ndarray): Vector de medias de genes.
            stds (np.ndarray): Vector de desvíos estándar.

        Returns:
            pygame.Surface | None: Surface del gráfico renderizado.
        """
        if generation == self.last_generation:
            return

        self.last_generation = generation

        self.ax.clear()
        self.fig.patch.set_facecolor(rgb_to_mpl(GRAPH_BACKGROUND))
        self.ax.set_facecolor(rgb_to_mpl(GRAPH_BACKGROUND))

        n = len(means)
        y = np.arange(n)

        for i in range(n):
            mean = means[i]
            std = stds[i]

            total_std_width = 2 * std
            start_pos = mean - std

            mean_color = "green" if mean >= 0 else "red"

            self.ax.barh(i, total_std_width,
                         left=start_pos, color="gray",
                         alpha=0.4
                         )

            self.ax.barh(i, abs(mean), left=min(0, mean),
                         color=mean_color, alpha=0.9)

            self.ax.text(
                -0.9,
                i,
                f"{mean:.2f}",
                va="center",
                fontsize=8,
                color="white"
            )

        self.ax.set_yticks(y)
        self.ax.set_yticklabels(self.labels, fontsize=10)
        self.ax.axvline(0, color="white", linewidth=1)
        self.ax.grid(axis="x", alpha=0.2)
        self.ax.set_xlim(min(self.ax.get_xlim()[0], -1), max(self.ax.get_xlim()[1], 1))

        self.ax.tick_params(axis='y', colors='turquoise')
        self.ax.tick_params(axis='x', colors='turquoise')

        self.fig.subplots_adjust(left=0.3, right=0.95, top=0.95, bottom=0.20)

        self.fig.canvas.draw()
        raw_data = self.fig.canvas.buffer_rgba()

        w, h = self.fig.canvas.get_width_height()

        self.surface = pygame.image.frombuffer(raw_data, (w, h), "RGBA").convert()

        return self.surface


class SoundManager:
    """
    Maneja los efectos de sonido y la música del juego.
    """

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.set_num_channels(15)
        self.sfx = {}

        self.wing_cooldown_ms = 80
        self.hit_cooldown_ms = 150
        self.sfx_cooldowns = {}
        self.cargar_audio()

    def cargar_audio(self) -> None:
        """Carga todos los efectos de sonido y música."""
        try:
            for name, path in AUDIO_PATHS.items():
                path = os.path.normpath(path)
                if name != 'music':
                    sound = pygame.mixer.Sound(path)
                    sound.set_volume(SFX_VOLUME)
                    self.sfx[name] = sound

        except pygame.error as e:
            print(f"Error al cargar el audio en SoundManager: {e}")

        self.music_paths = {
            'game_music': AUDIO_PATHS.get('game_music'),
            'menu_music': AUDIO_PATHS.get('menu_music')
        }
        pygame.mixer.music.set_volume(MUSIC_VOLUME)

    def play_sfx(self, name: str) -> None:
        """
        Reproduce un sonido instantáneamente.

        Args:
            name (str): Nombre del sonido cargado.
        """
        if name in self.sfx:
            self.sfx[name].play()

    def play_sfx_limited(self, name: str, cooldown_ms: int | None = None) -> None:
        """
        Reproduce un SFX con cooldown para evitar saturación.

        Args:
            name (str): Nombre del efecto.
            cooldown_ms (int | None): Cooldown personalizado.

        """
        if name not in self.sfx:
            return

        if name == 'wing':
            cooldown = self.wing_cooldown_ms
        elif name == 'hit':
            cooldown = self.hit_cooldown_ms
        elif cooldown_ms is not None:
            cooldown = cooldown_ms
        else:
            self.play_sfx(name)
            return

        current_time = pygame.time.get_ticks()

        if name not in self.sfx_cooldowns or \
                current_time - self.sfx_cooldowns[name] > cooldown:
            self.play_sfx(name)
            self.sfx_cooldowns[name] = current_time

    def play_music(self, name: str, loop: int = -1) -> None:
        """
        Reproduce música de fondo.

        Args:
            name (str): Nombre de la pista.
            loop (int): Cantidad de repeticiones (-1 = infinito).
        """
        path = self.music_paths[name]
        if path and os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(loop)
        elif path is None:
            print(f"Error: No se encontró la ruta para la música '{name}'")

    def stop_music(self) -> None:
        """Detiene la música."""
        pygame.mixer.music.stop()

    def pause_music(self) -> None:
        """Pausa la música."""
        pygame.mixer.music.pause()

    def unpause_music(self) -> None:
        """Reanuda la música pausada."""
        pygame.mixer.music.unpause()
