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
