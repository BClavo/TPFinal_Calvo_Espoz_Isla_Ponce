
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
MAX_GENERATIONS = 100
ELITE_SIZE = 20
MUTATION_RATE = 0.2
MUTATION_INTENSITY = 0.4
BONUS_POR_TUBERIA = 300

# --- COLORES ---
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (100, 150, 255)
AMARILLO = (255, 255, 0)
NARANJA = (255, 165, 0)
TURQUESA = (64,224,208)
VIOLETA = (200,10,200)

# --- RUTAS DE SPRITES ---
SPRITE_PATHS = {
    "default":{'fondo': 'sprites/temas/default/default_fondo.png',
                'bird': 'sprites/temas/default/default_pj.png',
                'bird_dead': 'sprites/temas/default/default_muerto.png',
                'pipe_top': 'sprites/temas/default/default_toppipe.png',
                'pipe_bottom': 'sprites/temas/default/default_bottompipe.png',
                'portada': 'sprites/temas/default/default_portada.png'},
    "espacio":{'fondo': 'sprites/temas/area51/espacio_fondo.png',
                'bird': 'sprites/temas/area51/espacio_pj.png',
                'bird_dead': 'sprites/temas/area51/espacio_muerto.png',
                'pipe_top': 'sprites/temas/area51/espacio_toppipe.png',
                'pipe_bottom': 'sprites/temas/area51/espacio_bottompipe.png',
                'portada': 'sprites/temas/area51/espacio_portada.png'},
    "agua":{'fondo': 'sprites/temas/bajo_agua/agua_fondo.png',
                'bird': 'sprites/temas/bajo_agua/agua_pj.png',
                'bird_dead': 'sprites/temas/bajo_agua/agua_muerto.png',
                'pipe_top': 'sprites/temas/bajo_agua/agua_toppipe.png',
                'pipe_bottom': 'sprites/temas/bajo_agua/agua_bottompipe.png',
                'portada': 'sprites/temas/bajo_agua/agua_portada.png'},
    "bosque":{'fondo': 'sprites/temas/bosque/bosque_fondo.png',
                'bird': 'sprites/temas/bosque/bosque_pj.png',
                'bird_dead': 'sprites/temas/bosque/bosque_muerto.png',
                'pipe_top': 'sprites/temas/bosque/bosque_toppipe.png',
                'pipe_bottom': 'sprites/temas/bosque/bosque_bottompipe.png',
                'portada': 'sprites/temas/bosque/bosque_portada.png'},
    "mitologia":{'fondo': 'sprites/temas/mitologia/mitologia_fondo.png',
                'bird': 'sprites/temas/mitologia/mitologia_pj.png',
                'bird_dead': 'sprites/temas/mitologia/mitologia_muerto.png',
                'pipe_top': 'sprites/temas/mitologia/mitologia_toppipe.png',
                'pipe_bottom': 'sprites/temas/mitologia/mitologia_bottompipe.png',
                'portada': 'sprites/temas/mitologia/mitologia_portada.png'},
    "stranger":{'fondo': 'sprites/temas/stranger/stranger_fondo.png',
                'bird': 'sprites/temas/stranger/stranger_pj.png',
                'bird_dead': 'sprites/temas/stranger/stranger_muerto.png',
                'pipe_top': 'sprites/temas/stranger/stranger_toppipe.png',
                'pipe_bottom': 'sprites/temas/stranger/stranger_bottompipe.png',
                'portada': 'sprites/temas/stranger/stranger_portada.png'},
    "udesa":{'fondo': 'sprites/temas/udesa/udesa_fondo.png',
                'bird': 'sprites/temas/udesa/udesa_pj.png',
                'bird_dead': 'sprites/temas/udesa/udesa_muerto.png',
                'pipe_top': 'sprites/temas/udesa/udesa_toppipe.png',
                'pipe_bottom': 'sprites/temas/udesa/udesa_bottompipe.png',
                'portada': 'sprites/temas/udesa/udesa_portada.png'},

    'titulo': 'sprites/titulo3.png',
    'subtitulo': 'sprites/geneticover.png',
    'jugar': 'sprites/jugar.png',
    'personalizar': 'sprites/personalizar.png',
    'salir': 'sprites/salir.png',
    'game_over': 'sprites/game_over.png',
    "flechai": 'sprites/flecha_izq.png' ,
    "flechad": 'sprites/flecha_der.png',
    'icono': 'sprites/icono_flappy.png',
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
    'game_over' : os.path.join("sounds","game_over.wav"),
    'die' :  os.path.join("sounds","sfx_die.wav"),
    'hit' :  os.path.join("sounds","sfx_hit.wav" ),
    'point' : os.path.join("sounds","sfx_point.wav" ),
    'swooshing' : os.path.join("sounds","sfx_swooshing.wav" ),
    'wing' : os.path.join("sounds","sfx_wing.wav" ),
    'click' : os.path.join("sounds","clicksound.wav")
    }