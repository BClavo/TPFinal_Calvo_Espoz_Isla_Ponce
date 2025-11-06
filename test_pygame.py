# Example file showing a basic pygame "game loop"
import pygame
import classes
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



# pygame setup
pygame.init() # Inicia todo los modulos de pygame
screen_ancho, screen_alto = GAME_WIDTH,600
screen=pygame.display.set_mode((screen_ancho,screen_alto)) # Crea la ventana ancho/alto

bg_image = pygame.image.load('sprites/bg.png')
bg_x = 0
bg_speed = 2  # velocidad del fondo


# Scale the image to fit the screen (if necessary)
bg_image = pygame.transform.scale(bg_image, (screen_ancho, screen_alto))


pygame.display.set_caption("Testeo") # Le pone nombre a la ventana
clock = pygame.time.Clock()
player = pygame.Rect((300,250,50,50))


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


    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_w]==True:
    #     player.move_ip(0,-1)
    # elif keys[pygame.K_s]==True:
    #     player.move_ip(0,1)
    # elif keys[pygame.K_a]==True:
    #     player.move_ip(-1,0)
    # elif keys[pygame.K_d]==True:
    #     player.move_ip(1,0)


    for event in pygame.event.get(): # Event, las distintas cosas que pueden pasar
        if event.type == pygame.QUIT:
            run = False
    

      # flip() the display pone a ver las cosas
    pygame.display.flip() # Toda la pantalla
    clock.tick(120)  # Controla los FPS del juego
    pygame.display.update() # Una parte especifica 
        


pygame.quit() # Finaliza los modulos
