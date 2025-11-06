import random
# import os
import pygame
# import time
import json

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


fondo = pygame.image.load('sprites/bg.png')
base = pygame.image.load('sprites/base')
imagen_pajarito = pygame.image.load('sprites/bird1.png')
imagen_pajarito = pygame.transform.scale(imagen_pajarito, (30))
top_pipe_image = pygame.image.load('sprites/toppipe.png')
top_pipe_image = pygame.transform.scale(top_pipe_image, (PIPE_WIDTH, 20))
bottom_pipe_image = pygame.image.load('sprite/bottompipe.png')
bottom_pipe_image = pygame.transform.scale(bottom_pipe_image, (PIPE_WIDTH, 20))


class Bird:
    def __init__(self, genes=None):
        if genes == None:
            self.genes = [random.uniform(-1, 1) for _ in range(0,
                                                               6)]  # Genera los genes de forma aleatoria, representados como vectores de 6 elementos.
        else:
            self.genes = genes

        # self.y = altura_de_la pantalla // 2 #El pajaro se inicia en la mitad de la pantalla.
        self.vy = 0  # Velocidad para subir y bajar
        self.x = 0
        self.alive = True

    def decision_aleteo(self, delta_y, delta_x):
        w0, w1, w2, w3, w4, w5 = self.genes
        value = w0 + w1 * delta_y + w2 * (delta_y ** 2) + w3 * delta_x + w4 * (delta_x ** 2) + w5 * self.vy
        return value > 0  # Si es menor a cero no aletea, si es mayor a 0 aletea.

    def fly(self, fuerza_de_aleteo=-10):
        self.vy = fuerza_de_aleteo

    def actualizar_posicion(self, delta_y, delta_x, aleteo):
        self.vy += GRAVITY
        self.y = self.vy

    def verify_collision(self, pipe):
        if pipe.x < self.x + BIRD_SIZE and pipe.x + PIPE_WIDTH > self.x: # Verifica si hay superposicion en X, lo que permite una salida rapida si el pajaro no esta cerca d ela tuberia.
            if self.y < pipe.y_gap - pipe.gap / 2 or self.y + BIRD_SIZE > pipe.y_gap + pipe.gap / 2: #Verifica si hay un choque con la tuberia superior o inferior.
                self.alive = False

class Tuberia:
    def __init__(self, x_incial):  # }
        self.x = x_incial  # } HAy que sacar al x inicial como argumento, y ponerlo como algo fijo
        self.width = WIDTH
        self.speed = PIPE_SPEED

        self.gap = PIPE_GAP
        self.y_gap = random.randint(self.gap, HEIGHT - self.gap)  # El hueco de la tubería se forma dentro de este rango, para respetar siempre el mismo tamaño

    def advance(self):
        self.x -= PIPE_SPEED
    def fuera_de_pantalla(self):
        return self.x + self.ancho < 0


class Juego:
    def __init__(self,ancho,fps,tiempo_max,gravedad):
        self.ancho=ancho
        self.fps=fps
        self.tiempo_max=tiempo_max
        self.gravedad=gravedad

