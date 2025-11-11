import pygame
import numpy as np
from config import *

class Pajaro(pygame.sprite.Sprite):
    
    def __init__(self, genes=None, imagen_vivo=None, imagen_muerto=None):
        super().__init__()
        # Genética: 6 pesos para la red neuronal
        self.genes = genes if genes is not None else np.random.uniform(-1, 1, 6)
        
        # Imágenes
        self.imagen_vivo = imagen_vivo
        self.imagen_muerto = imagen_muerto
        self.image = self.imagen_vivo.copy() if imagen_vivo else None
        
        # Posición y física
        self.rect = self.image.get_rect() if self.image else pygame.Rect(0, 0, BIRD_SIZE, BIRD_SIZE)
        self.rect.x = WIDTH // 4
        self.rect.y = HEIGHT // 2
        self.vy = 0
        
        # Estado
        self.vivo = True
        
        # Métricas para fitness
        self.distancia = 0
        self.fitness = 0
        self.tiempo_vivo = 0
        self.tuberias_pasadas = 0
        self.ultima_tuberia_pasada = None

    def decision_aleteo(self, tuberia):
        """Decide si el pájaro debe aletear según su red neuronal simple."""
        
        # Normalizar entradas
        delta_x = (tuberia.rect.x - self.rect.right) / GAME_WIDTH
        delta_y = (tuberia.y_gap - self.rect.centery) / HEIGHT
        vy_norm = self.vy / 20
        
        # Desempaquetar genes 
        w0, w1, w2, w3, w4, w5 = self.genes
        
        # Calcular valor de decisión
        valor = (
            w0  
            + w1 * delta_y  
            + w2 * (delta_y ** 2)  
            + w3 * delta_x
            + w4 * (delta_x ** 2)  
            + w5 * vy_norm  
        )
        
        return valor > 0

    def aletear(self, fuerza=FLAP_STRENGTH):
        """Aplica la fuerza de aleteo al pájaro."""
        self.vy = fuerza

    def actualizar_posicion(self):
        """Actualiza la física y posición del pájaro."""
        if not self.vivo:
            return
            
        # Aplicar gravedad
        self.vy += GRAVITY
        self.rect.y += self.vy
        
        # Actualizar métricas
        self.tiempo_vivo += 1
        self.distancia += 1

        # Límite superior
        if self.rect.top <= 0:
            self.rect.top = 0

        # Límite inferior (muerte)
        if self.rect.bottom >= HEIGHT:
            self.vivo = False
            self.muerte()

    def calcular_fitness(self):
        """
        Calcula el fitness del pájaro basado en:
        - Distancia recorrida
        - Tiempo de supervivencia
        - Número de tuberías pasadas (más importante)
        - Bonus por supervivencia prolongada
        """
        # Distancia recorrida
        fitness_distancia = self.distancia * 2
        
        # Tiempo de supervivencia
        fitness_tiempo = self.tiempo_vivo * 1.5

        # Tuberías pasadas (componente más importante)
        fitness_tuberias = self.tuberias_pasadas * BONUS_POR_TUBERIA
        
        # Bonus por supervivencia prolongada
        if self.tiempo_vivo > 300:
            bonus_supervivencia = (self.tiempo_vivo - 300) * 3
        else:
            bonus_supervivencia = 0
        
        # Fitness total
        self.fitness = (fitness_distancia + fitness_tiempo + 
                        bonus_supervivencia + fitness_tuberias)
        
        # Prevenir fitness negativo
        self.fitness = max(0, self.fitness)

    def muerte(self):
        """Cambia imagen y detiene al pájaro."""
        self.vivo = False
        self.vy = 0
        self.image = self.imagen_muerto.copy()
        self.image.set_alpha(51)  # opacidad baja, igual que tu versión original

                
    def verificar_colision_tuberia(self, grupo_tuberias):
        """Detecta colisión con alguna tubería."""
        if pygame.sprite.spritecollideany(self, grupo_tuberias):
            self.alive = False
            self.muerte()

    def verificar_tuberia_pasada(self, tuberia):
        """Detecta si el pájaro ya pasó la tubería."""
        if self.rect.left > tuberia.rect.right:
            if self.last_pipe_passed != id(tuberia):
                self.pipes_passed += 1
                self.last_pipe_passed = id(tuberia)



class Tuberia(pygame.sprite.Sprite):
    """Representa una tubería (superior o inferior)."""

    def __init__(self, x_inicial, y_inicial, superior, imagen_top, imagen_bottom, id_tuberia):
        super().__init__()
        self.superior = superior
        self.velocidad = PIPE_SPEED
        self.ancho = PIPE_WIDTH
        self.image = imagen_top if superior else imagen_bottom
        self.rect = self.image.get_rect()
        self.rect.x = x_inicial
        self.rect.y = y_inicial
        self.id_tuberia = id_tuberia
        self.y_gap = y_inicial + PIPE_HEIGHT + (PIPE_GAP / 2) if superior else y_inicial - (PIPE_GAP / 2)

    def update(self):
        self.rect.x -= self.velocidad
        if self.rect.right < 0:
            self.kill()


def crear_par_tuberias(x_inicial, centro_gap, imagen_top, imagen_bottom):
    """Crea y devuelve un par (superior, inferior) de tuberías."""
    y_top = centro_gap - PIPE_GAP // 2 - PIPE_HEIGHT
    y_bottom = centro_gap + PIPE_GAP // 2
    id_tuberia = pygame.time.get_ticks()
    tuberia_top = Tuberia(x_inicial, y_top, True, imagen_top, imagen_bottom, id_tuberia)
    tuberia_bottom = Tuberia(x_inicial, y_bottom, False, imagen_top, imagen_bottom, id_tuberia)
    return tuberia_top, tuberia_bottom


class Fondo:
    """Crea un efecto de desplazamiento infinito en el fondo."""

    def __init__(self, imagen):
        self.imagen = imagen
        self.x1 = 0
        self.x2 = GAME_WIDTH
        self.velocidad = 2

    def actualizar(self):
        self.x1 -= self.velocidad
        self.x2 -= self.velocidad
        if self.x1 <= -GAME_WIDTH:
            self.x1 = self.x2 + GAME_WIDTH
        if self.x2 <= -GAME_WIDTH:
            self.x2 = self.x1 + GAME_WIDTH

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x1, 0))
        pantalla.blit(self.imagen, (self.x2, 0))
