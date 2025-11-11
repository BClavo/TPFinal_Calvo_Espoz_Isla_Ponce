
"""
Archivo de configuración central para el juego Flappy Bird Genético
"""

# --- CONFIGURACIÓN DE PANTALLA ---
HEIGHT = 600
WIDTH = 1000
PANEL_WIDTH = 280
GAME_WIDTH = 720
FPS = 60

# -- CONFIGURACIÓN DE FÍSICA ---
GRAVITY = 0.5
FLAP_STRENGTH = -10

# --- CONFIGURACIÓN DE TUBERÍAS ---
PIPE_WIDTH = 70
PIPE_GAP = 250
MIN_PIPE_GAP = 150
PIPE_SPEED = 6
PIPE_HEIGHT = 500
DISTANCIA_ENTRE_TUBERIAS = 360
MARGEN_VERTICAL = 150

# --- CONFIGURACIÓN DEL PÁJARO ---
BIRD_SIZE = 30

# --- PARÁMETROS GENÉTICOS ---
NUM_PAJAROS = 100
MAX_GENERATIONS = 1000
ELITE_SIZE = 4
MUTATION_RATE = 0.1
MUTATION_INTENSITY = 0.2
BONUS_POR_TUBERIA = 1000

# --- COLORES ---
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (100, 150, 255)

# --- RUTAS DE SPRITES ---
SPRITE_PATHS = {
    'fondo': 'sprites/bg_dia.png',
    'base': 'sprites/base.png',
    'bird': 'sprites/bird1.png',
    'bird_dead': 'sprites/bird2muerto.png',
    'pipe_top': 'sprites/toppipe.png',
    'pipe_bottom': 'sprites/bottompipe.png'
}