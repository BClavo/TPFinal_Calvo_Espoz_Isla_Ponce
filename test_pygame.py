# Example file showing a basic pygame "game loop"
import pygame
from classes import Bird, Tuberia
import json
import random

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

# pipe = classes.Tuberia(650,500,False)
# pipe2 = classes.Tuberia(650,-500+PIPE_GAP,True)
grupo_pipes = pygame.sprite.Group()
# grupo_pipes.add(pipe,pipe2)

top_pipe_image = pygame.image.load('sprites/toppipe.png')
top_pipe_image = pygame.transform.scale(top_pipe_image, (PIPE_WIDTH, HEIGHT))  # corregido: altura coherente

# pygame setup
pygame.init() # Inicia todo los modulos de pygame
screen_ancho, screen_alto = GAME_WIDTH,HEIGHT
screen=pygame.display.set_mode((screen_ancho,screen_alto)) # Crea la ventana ancho/alto

bg_image = pygame.image.load('sprites/bg_dia.png')
bg_x = 0
bg_speed = 2  # velocidad del fondo


# Scale the image to fit the screen (if necessary)
bg_image = pygame.transform.scale(bg_image, (screen_ancho, screen_alto))


pygame.display.set_caption("Testeo") # Le pone nombre a la ventana
clock = pygame.time.Clock()
player = pygame.Rect((300,250,50,50))

NUEVA_TUBERIA = pygame.USEREVENT + 1
pygame.time.set_timer(NUEVA_TUBERIA, 950)  # cada 1.5 segundos

run = True
while run:

   
    
    screen.fill("purple") # Llena la pantalla de un color
    screen.blit(bg_image, (0, 0)) # Dibuja una superficie arriba de otra
    pygame.draw.rect(screen,(255,0,0),player) 

    
    # Mover fondo
    bg_x -= bg_speed
    if bg_x <= -GAME_WIDTH:
        bg_x = 0

    # Dibujar fondo dos veces para scroll infinito
    screen.blit(bg_image, (bg_x, 0))
    screen.blit(bg_image, (bg_x + GAME_WIDTH, 0))


    for event in pygame.event.get(): # Event, las distintas cosas que pueden pasar
        if event.type == pygame.QUIT:
            run = False
        elif event.type == NUEVA_TUBERIA:
                        # Centro vertical del hueco (entre tuberías)
            centro_gap = random.randint(150, HEIGHT - 150)

            # Posición de cada tubería
            PIPE_HEIGHT=500
            y_top = centro_gap - PIPE_GAP // 2 - PIPE_HEIGHT
            y_bottom = centro_gap + PIPE_GAP // 2

            tuberia_top = Tuberia(GAME_WIDTH, y_top, True)
            tuberia_bottom = Tuberia(GAME_WIDTH, y_bottom, False)
            grupo_pipes.add(tuberia_top, tuberia_bottom)


        
    grupo_pipes.draw(screen)
    grupo_pipes.update()
    

      # flip() the display pone a ver las cosas
    pygame.display.flip() # Toda la pantalla
    clock.tick(FPS)  # Controla los FPS del juego
    pygame.display.update() # Una parte especifica 
        


pygame.quit() # Finaliza los modulos
