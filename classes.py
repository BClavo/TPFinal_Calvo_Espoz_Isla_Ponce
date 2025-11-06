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



# class Pajarito:
#     def __init__ (self,tamaño=30,fuerza_aleteo=-10):
#         self.tamaño=tamaño
#         self.fuerza_aleteo=fuerza_aleteo
    
class Tuberia:
    def __init__(self, x, ancho=70, gap=200, min_gap=150, velocidad=6):
        self.x = x
        self.y=random.randit(100, 400)  # altura del hueco

        self.ancho=ancho
        self.gap=gap
        self.min_gap=min_gap
        self.vel=velocidad
    def mover(self):
        self.x -= self.vel
    def fuera_de_pantalla(self):
        return self.x + self.ancho < 0


# class Fondo:
#     def __init__(self,ancho,alto):

class Juego:
    def __init__(self,ancho,fps,tiempo_max,gravedad):
        self.ancho=ancho
        self.fps=fps
        self.tiempo_max=tiempo_max
        self.gravedad=gravedad




{
	"WIDTH": 1000 ,
	"HEIGHT" : 600 ,
	"PANEL_WIDTH" : 280 ,
	"GAME_WIDTH" : 400 ,
	"FPS" : 60 ,
	"MAX_TIME" : 120 ,
	"GRAVITY" : 0.5 ,

	# "FLAP_STRENGTH" : -10 ,

	# "PIPE_WIDTH" : 70 ,
	# "PIPE_GAP" : 200  ,
	# "MIN_PIPE_GAP" : 150 ,
	# "PIPE_SPEED" : 6 ,

	# "BIRD_SIZE" : 30
}
