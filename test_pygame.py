# Example file showing a basic pygame "game loop"
import pygame



# pygame setup
pygame.init() # Inicia todo los modulos de pygame
screen_ancho, screen_alto = 576,1024 
screen=pygame.display.set_mode((screen_ancho,screen_alto)) # Crea la ventana ancho/alto

bg_image = pygame.image.load('bg_night.png')
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

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]==True:
        player.move_ip(0,-1)
    elif keys[pygame.K_s]==True:
        player.move_ip(0,1)
    elif keys[pygame.K_a]==True:
        player.move_ip(-1,0)
    elif keys[pygame.K_d]==True:
        player.move_ip(1,0)


    for event in pygame.event.get(): # Event, las distintas cosas que pueden pasar
        if event.type == pygame.QUIT:
            run = False
        if event.type 

      # flip() the display pone a ver las cosas
    pygame.display.flip() # Toda la pantalla
    clock.tick(120)  # Controla los FPS del juego
    pygame.display.update() # Una parte especifica 
        


pygame.quit() # Finaliza los modulos
