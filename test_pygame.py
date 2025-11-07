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
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Genético")
clock = pygame.time.Clock()

panel_juego = pygame.Surface((GAME_WIDTH, HEIGHT))
panel = pygame.Surface((PANEL_WIDTH, HEIGHT))


# Fondo
fondo_juego = pygame.image.load('sprites/bg_dia.png')
fondo_juego= pygame.transform.scale(fondo_juego, (GAME_WIDTH, HEIGHT))
NEGRO = (0, 0, 0)
fondo_x = 0
fondo_velocidad = 2

# Grupos
grupo_pipes = pygame.sprite.Group()
grupo_pajaros = pygame.sprite.Group()

# Crear pájaros

NUM_PAJAROS = 20  # Número total de pájaros que se van a crear
pajaros = []  # Lista para guardar referencias individuales a cada pájaro

for pajaro in range(NUM_PAJAROS):  # Bucle para crear múltiples pájaros
    b = Bird()  # Instancia de un nuevo pájaro 
    # b.rect.y = random.randint(HEIGHT // 3, HEIGHT - 100)  # Posición vertical aleatoria dentro de un rango jugable (para verlos)
    grupo_pajaros.add(b)  # Se agrega el pájaro al grupo de sprites
    pajaros.append(b)  # Se guarda el pájaro en la lista para acceso individual (por ejemplo, en simulaciones genéticas)


# Evento para tuberías
NUEVA_TUBERIA = pygame.USEREVENT + 1
pygame.time.set_timer(NUEVA_TUBERIA, 1000) # 0,95 seg

# Inicializar frame contador
frame = 0

# Loop principal
run = True
while run:

    # Dibujar panel izquierdo con la imagen del juego moviendose
    screen.blit(fondo_juego, (fondo_x, 0))
    screen.blit(fondo_juego, (fondo_x + GAME_WIDTH, 0))
    fondo_x -= fondo_velocidad
    if fondo_x <= -GAME_WIDTH:
        fondo_x = 0
     

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == NUEVA_TUBERIA:  # Evento personalizado para generar nuevas tuberías
            MARGEN_VERTICAL = 150  # Margen para evitar que el hueco esté demasiado cerca de los bordes
            centro_gap = random.randint(MARGEN_VERTICAL, HEIGHT - MARGEN_VERTICAL)  # Posición vertical aleatoria del centro del hueco

            PIPE_HEIGHT = 500  # Altura fija de cada tubería

            y_top = centro_gap - PIPE_GAP // 2 - PIPE_HEIGHT  # Posición Y de la tubería superior (invertida)
            y_bottom = centro_gap + PIPE_GAP // 2  # Posición Y de la tubería inferior (normal)

            tuberia_top = Tuberia(GAME_WIDTH, y_top, True)  # Crea la tubería superior en el borde derecho
            tuberia_bottom = Tuberia(GAME_WIDTH, y_bottom, False)  # Crea la tubería inferior en el borde derecho

            grupo_pipes.add(tuberia_top, tuberia_bottom)  # Agrega ambas tuberías al grupo de sprites

    # --- LÓGICA DEL PÁJARO GENÉTICO ---
    def clave_distancia(pipe):
        return pajaro.distancia_a(pipe)

    pipes_front = [p for p in grupo_pipes if p.rect.x + p.width > pajaro.rect.x]
    pipes_front.sort(key=clave_distancia)
    next_pipe = pipes_front[0] if pipes_front else None

    for pajaro in pajaros:
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

    
    # Dibujar panel derecho en negro
    pygame.draw.rect(screen, NEGRO, (GAME_WIDTH, 0, PANEL_WIDTH, HEIGHT))


    pygame.display.flip()
    # pygame.display.update()
    clock.tick(FPS)
   

pygame.quit()
