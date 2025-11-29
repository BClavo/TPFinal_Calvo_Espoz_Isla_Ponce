
"""
Archivo de configuración central para el juego Flappy Bird Genético
"""
import os.path

import pygame

# --- CONFIGURACIÓN DE PANTALLA ---
HEIGHT = 600
WIDTH = 1000
PANEL_WIDTH = 280
GAME_WIDTH = 720
FPS = 60
#--- CONFIGURACIÓN DEL GRAFICO ---
GRAPH_X = GAME_WIDTH + 20
GRAPH_Y = 255
GRAPH_WIDTH = PANEL_WIDTH - 40
GRAPH_HEIGHT = 120
GRAPH_RECT = pygame.Rect(GRAPH_X,GRAPH_Y,GRAPH_WIDTH,GRAPH_HEIGHT) #Genera el cuadrado del grafico
GRAPH_RECT_GEN = pygame.Rect(GRAPH_X,GRAPH_Y+GRAPH_HEIGHT+20,GRAPH_WIDTH,GRAPH_HEIGHT)
SPEED_Y = GRAPH_Y+ 2*(GRAPH_HEIGHT+20)
GRAPH_BACKGROUND =  (40,40,50)
GRAPH_BORDER = (80,80,80)
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
ELITE_SIZE = 20
MUTATION_RATE = 0.2
MUTATION_INTENSITY = 0.4
BONUS_POR_TUBERIA = 200

# --- COLORES ---
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (100, 150, 255)
AMARILLO = (255, 255, 0)
NARANJA = (255, 165, 0)
TURQUESA = (64,224,208)

# --- RUTAS DE SPRITES ---
SPRITE_PATHS = {
    'fondo': 'sprites/bg_dia.png',
    'bird': 'sprites/bird1.png',
    'bird_dead': 'sprites/bird2muerto.png',
    'pipe_top': 'sprites/toppipe.png',
    'pipe_bottom': 'sprites/bottompipe.png',
    'titulo': 'sprites/titulo3.png',
    'subtitulo': 'sprites/geneticover.png',
    'jugar': 'sprites/jugar.png',
    'personalizar': 'sprites/personalizar.png',
    'salir': 'sprites/salir.png',
    'game_over': 'sprites/game_over.png'
}

# --- RUTAS DEL MENU ---

# --- FUENTES PERSONALIZADAS ---
FONT_PATHS = {
    'flappyfont': 'sprites/FlappyBirdy.ttf',
}

FONT_SIZES = {
    'titulo': 140,
    'subtitulo': 50,
    'texto': 24,
    'stats': 20
}

# --- CONFIGURACIÓN DE AUDIO ---
MUSIC_VOLUME = 0.4
SFX_VOLUME = 0.5

AUDIO_PATHS = {
    'game_music' : os.path.join("sounds","music.ogg"),
    'menu_music' : os.path.join("sounds","menu_music.wav"),
    'die' :  os.path.join("sounds","sfx_die.wav"),
    'hit' :  os.path.join("sounds","sfx_hit.wav" ),
    'point' : os.path.join("sounds","sfx_point.wav" ),
    'swooshing' : os.path.join("sounds","sfx_swooshing.wav" ),
    'wing' : os.path.join("sounds","sfx_wing.wav" ),
    'click' : os.path.join("sounds","clicksound.wav")
    }