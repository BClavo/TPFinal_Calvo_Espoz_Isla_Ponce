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

tiempo = pygame.time.get_ticks()
# Inicializar pygame
pygame.init()
screen = pygame.display.set_mode((GAME_WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Genético")
clock = pygame.time.Clock()

# Fondo
fondo_image = pygame.image.load('sprites/bg_dia.png')
fondo_image = pygame.transform.scale(fondo_image, (GAME_WIDTH, HEIGHT))
fondo_x = 0
fondo_velocidad = 2

# Grupos
grupo_pipes = pygame.sprite.Group()
grupo_pajaros = pygame.sprite.Group()

# Crear pájaro
pajaro = Bird()
grupo_pajaros.add(pajaro)

# Evento para tuberías
NUEVA_TUBERIA = pygame.USEREVENT + 1
pygame.time.set_timer(NUEVA_TUBERIA, 950) # 0,95 seg

# Inicializar frame contador
frame = 0

# Loop principal
run = True
# Loop principal
run = True
while run:
    screen.blit(fondo_image, (fondo_x, 0))
    screen.blit(fondo_image, (fondo_x + GAME_WIDTH, 0))
    fondo_x -= fondo_velocidad
    if fondo_x <= -GAME_WIDTH:
        fondo_x = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == NUEVA_TUBERIA:
            MARGEN_VERTICAL = 150
            centro_gap = random.randint(MARGEN_VERTICAL, HEIGHT - MARGEN_VERTICAL)
            PIPE_HEIGHT = 500
            y_top = centro_gap - PIPE_GAP // 2 - PIPE_HEIGHT
            y_bottom = centro_gap + PIPE_GAP // 2
            tuberia_top = Tuberia(GAME_WIDTH, y_top, True)
            tuberia_bottom = Tuberia(GAME_WIDTH, y_bottom, False)
            grupo_pipes.add(tuberia_top, tuberia_bottom)

    # --- LÓGICA DEL PÁJARO GENÉTICO ---
    def clave_distancia(pipe):
        return pajaro.distancia_a(pipe)

    pipes_front = [p for p in grupo_pipes if p.rect.x + p.width > pajaro.rect.x]
    pipes_front.sort(key=clave_distancia)
    next_pipe = pipes_front[0] if pipes_front else None

    if pajaro.alive:
        if next_pipe and pajaro.decision_aleteo(next_pipe):
            pajaro.fly()
        pajaro.actualizar_posicion()

    # Colisión con tuberías
    if pygame.sprite.spritecollideany(pajaro, grupo_pipes):
        pajaro.alive = False


    # --- DIBUJO ---
    grupo_pipes.update()
    grupo_pipes.draw(screen)
    if pajaro.alive:
        grupo_pajaros.draw(screen)
    else:
        None

    pygame.display.flip()
    clock.tick(FPS)  


    pygame.display.flip()
    # pygame.display.update()
    clock.tick(FPS)
   

pygame.quit()
