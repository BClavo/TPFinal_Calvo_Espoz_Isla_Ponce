import random
import pygame
import numpy as np 
import json

# --- CARGA DE CONFIGURACIÓN ---
with open("config.json") as f:
    config = json.load(f)
    HEIGHT = config["HEIGHT"]
    WIDTH = config["WIDTH"]
    PANEL_WIDTH = config["PANEL_WIDTH"]
    GAME_WIDTH = config["GAME_WIDTH"]
    FPS = config["FPS"]
    MAX_TIME = config["MAX_TIME"]
    GRAVITY = config["GRAVITY"]
    FLAP_STRENGTH = config["FLAP_STRENGTH"]
    PIPE_WIDTH = config["PIPE_WIDTH"]
    PIPE_GAP = config["PIPE_GAP"]
    MIN_PIPE_GAP = config["MIN_PIPE_GAP"]
    PIPE_SPEED = config["PIPE_SPEED"]
    BIRD_SIZE = config["BIRD_SIZE"]

# --- CARGA DE IMÁGENES ---
fondo = pygame.image.load('sprites/bg.png')
base = pygame.image.load('sprites/base.png')  # corregido: faltaba ".png"
imagen_pajarito = pygame.image.load('sprites/bird1.png')
imagen_pajarito = pygame.transform.scale(imagen_pajarito, (BIRD_SIZE, BIRD_SIZE))  # corregido: debía ser tupla
top_pipe_image = pygame.image.load('sprites/toppipe.png')
top_pipe_image = pygame.transform.scale(top_pipe_image, (PIPE_WIDTH, HEIGHT))  # corregido: altura coherente
bottom_pipe_image = pygame.image.load('sprites/bottompipe.png')  # corregido: "sprites" en plural
bottom_pipe_image = pygame.transform.scale(bottom_pipe_image, (PIPE_WIDTH, HEIGHT))

# --- CLASES ---

class Bird:
    def __init__(self, genes=None):
        if genes is None:
            # Genera los genes de forma aleatoria (6 pesos)
            self.genes = [random.uniform(-1, 1) for _ in range(6)]
        else:
            self.genes = genes

        self.y = HEIGHT // 2  # Inicia en el medio de la pantalla
        self.x = WIDTH // 4   # Posición inicial horizontal
        self.vy = 0
        self.alive = True
        self.distance = 0
        self.fitness = 0

    def decision_aleteo(self, delta_y, delta_x):
        w0, w1, w2, w3, w4, w5 = self.genes
        value = w0 + w1 * delta_y + w2 * (delta_y ** 2) + w3 * delta_x + w4 * (delta_x ** 2) + w5 * self.vy
        return value > 0  # Si es positivo, aletea

    def fly(self, fuerza_de_aleteo=FLAP_STRENGTH):
        self.vy = fuerza_de_aleteo

    def actualizar_posicion(self):
        # Actualiza la velocidad y la posición del pájaro
        self.vy += GRAVITY
        self.y += self.vy
        self.distance += 1
    
    def calcular_fitness(self):
        self.fitness = (self.distance/FPS) * PIPE_SPEED

    def verify_collision(self, pipe):
        # Verifica superposición en eje X
        if pipe.x < self.x + BIRD_SIZE and pipe.x + PIPE_WIDTH > self.x:
            # Verifica choque con tuberías superior o inferior
            if self.y < pipe.y_gap - pipe.gap / 2 or self.y + BIRD_SIZE > pipe.y_gap + pipe.gap / 2:
                self.alive = False
        # Verifica 
        elif self.y < 0 or self.y > HEIGHT:
            self.alive = False

birds = [Bird() for _ in range(10)]  
class Poblacion: 
    def __init__(self,poblacion):
        self.poblacion = poblacion 
    fitnesses = np.array([b.fitness for b in birds])
    fit_normalizado = fitnesses / np.sum(fitnesses)


class Tuberia:
    def __init__(self, x_inicial):
        self.x = x_inicial
        self.width = PIPE_WIDTH
        self.speed = PIPE_SPEED
        self.gap = PIPE_GAP
        self.y_gap = random.randint(self.gap, HEIGHT - self.gap)

    def advance(self):
        self.x -= self.speed

    def fuera_de_pantalla(self):
        return self.x + self.width < 0


class Juego:
    def __init__(self):
        self.ancho = GAME_WIDTH
        self.fps = FPS
        self.tiempo_max = MAX_TIME
        self.gravedad = GRAVITY