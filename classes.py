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
            self.morir()

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

    def morir(self):
        """Cambia la imagen al sprite del pájaro muerto."""
        if self.imagen_muerto:
            self.image = self.imagen_muerto

    def verificar_colision_tuberia(self, grupo_tuberias):
        """Verifica si el pájaro colisiona con alguna tubería."""
        if pygame.sprite.spritecollideany(self, grupo_tuberias):
            self.vivo = False
            self.morir()
            return True
        return False

    def verificar_tuberia_pasada(self, siguiente_tuberia):
        """
        Verifica si el pájaro pasó completamente una tubería
        y actualiza el contador de tuberías pasadas.
        """
        if siguiente_tuberia and self.rect.left > siguiente_tuberia.rect.right:
            if self.ultima_tuberia_pasada != siguiente_tuberia.pipe_id:
                self.tuberias_pasadas += 1
                self.ultima_tuberia_pasada = siguiente_tuberia.pipe_id
                return True
        return False



class Tuberia(pygame.sprite.Sprite):
    """
    Representa una tubería (superior o inferior)
    """
    def __init__(self, x_inicial, y_inicial, top, imagen_top=None, imagen_bottom=None):
        super().__init__()
        
        # Configuración básica
        self.top = top
        self.y = y_inicial
        self.x = x_inicial
        self.width = PIPE_WIDTH
        self.speed = PIPE_SPEED
        self.gap = PIPE_GAP
        
        # ID único para identificar pares de tuberías
        self.pipe_id = None
        
        # Calcular el centro del hueco
        if top:
            # Tubería superior: hueco está DEBAJO
            self.y_gap = y_inicial + PIPE_HEIGHT + (PIPE_GAP // 2)
            self.image = imagen_top
        else:
            # Tubería inferior: hueco está ARRIBA
            self.y_gap = y_inicial - (PIPE_GAP // 2)
            self.image = imagen_bottom   
        
        # Rectángulo de colisión
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def advance(self):
        """Mueve la tubería hacia la izquierda"""
        self.rect.x -= self.speed

    def fuera_de_pantalla(self):
        """Verifica si la tubería salió de la pantalla"""
        return self.rect.x + self.width < 0
    
    def update(self):
        """Actualiza la posición y elimina si está fuera de pantalla"""
        self.advance()
        if self.fuera_de_pantalla():
            self.kill()


def crear_par_tuberias(x_inicial, centro_gap, imagen_top=None, imagen_bottom=None):
    """
    Crea un par de tuberías (superior e inferior) con el mismo ID
    
    Args:
        x_inicial: Posición X inicial
        centro_gap: Posición Y del centro del hueco
        imagen_top: Imagen para tubería superior
        imagen_bottom: Imagen para tubería inferior
    
    Returns:
        tuple: (tuberia_superior, tuberia_inferior)
    """
    y_top = centro_gap - PIPE_GAP // 2 - PIPE_HEIGHT
    y_bottom = centro_gap + PIPE_GAP // 2
    
    tuberia_top = Tuberia(x_inicial, y_top, True, imagen_top, imagen_bottom)
    tuberia_bottom = Tuberia(x_inicial, y_bottom, False, imagen_top, imagen_bottom)
    
    # Asignar el mismo ID a ambas tuberías del par
    shared_id = id(tuberia_top)
    tuberia_top.pipe_id = shared_id
    tuberia_bottom.pipe_id = shared_id
    
    return tuberia_top, tuberia_bottom

# background.py
"""
Clase Background para manejar el fondo con scroll infinito
"""
import pygame
from config import *


class Background:
    """
    Maneja el fondo con scroll infinito
    """
    def __init__(self, imagen_fondo):
        self.imagen = imagen_fondo
        self.x1 = 0
        self.x2 = GAME_WIDTH
        self.velocidad = 2
        self.width = GAME_WIDTH

    def update(self):
        """Actualiza la posición del fondo para crear efecto de scroll"""
        self.x1 -= self.velocidad
        self.x2 -= self.velocidad

        # Resetear posición cuando sale de pantalla
        if self.x1 <= -self.width:
            self.x1 = self.x2 + self.width
        
        if self.x2 <= -self.width:
            self.x2 = self.x1 + self.width

    def draw(self, screen):
        """Dibuja el fondo en la pantalla"""
        screen.blit(self.imagen, (self.x1, 0))
        screen.blit(self.imagen, (self.x2, 0))

    def set_velocidad(self, velocidad):
        """Cambia la velocidad del scroll"""
        self.velocidad = velocidad