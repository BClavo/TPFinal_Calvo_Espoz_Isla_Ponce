# Example file showing a basic pygame "game loop"
import pygame
import classes


# pygame setup
pygame.init() # Inicia todo los modulos de pygame
screen_ancho, screen_alto = 1000,600 
screen=pygame.display.set_mode((screen_ancho,screen_alto)) # Crea la ventana ancho/alto

bg_image = pygame.image.load('sprites/bg_night.png')
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
    if bg_x <= -WIDTH:
        bg_x = 0

    # Dibujar fondo dos veces para scroll infinito
    screen.blit(bg_image, (bg_x, 0))
    screen.blit(bg_image, (bg_x + WIDTH, 0))


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
