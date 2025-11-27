import numpy as np
from classes import Pajaro
from config import *

class Poblacion:
    """Maneja la evolución genética de la población de pájaros."""

    def __init__(self, poblacion):
        self.poblacion = poblacion
        self.fitnesses = np.array([b.fitness for b in self.poblacion])
        self.genes = np.array([b.genes for b in self.poblacion])
        self.promedio_genes= np.mean(self.genes,axis=0)
        self.desviacion_genes = np.std(self.genes,axis=0)

    def seleccion_por_torneo(self, k=3):
        indices = np.random.choice(len(self.poblacion), k, replace=False)
        mejor_idx = indices[np.argmax(self.fitnesses[indices])]
        return self.poblacion[mejor_idx]

    def seleccion_elitista(self, n_elite=ELITE_SIZE):
        ordenados = np.argsort(self.fitnesses)[::-1]
        return [self.poblacion[i] for i in ordenados[:n_elite]]

    def crossover_un_punto(self, p1, p2):
        punto = np.random.randint(1, len(p1.genes) - 1)
        h1 = np.concatenate([p1.genes[:punto], p2.genes[punto:]])
        h2 = np.concatenate([p2.genes[:punto], p1.genes[punto:]])
        return [Pajaro(h1), Pajaro(h2)]

    def crossover_blend(self, p1, p2, alpha=0.8): #Mezcla un porcentaje de uno con un porcentaje de otro
        h1 = p1.genes * alpha + p2.genes * (1 - alpha)
        h2 = p2.genes * alpha + p1.genes * (1 - alpha)
        return [Pajaro(h1), Pajaro(h2)]

    def mutacion(self, genes, intensity):
        rate = MUTATION_RATE

        mascara = np.random.rand(*genes.shape) < rate
        ruido = np.random.uniform(-intensity, intensity, genes.shape)
        nuevos_genes = np.where(mascara, genes + ruido, genes)
        return np.clip(nuevos_genes, -3, 3)
    
    def crear_nueva_generacion(self, imagen_vivo=None, imagen_muerto=None):
        """
        Crea una nueva generación mediante elitismo, selección, crossover y mutación
        
        Args:
            imagen_vivo: Imagen para pájaros vivos
            imagen_muerto: Imagen para pájaros muertos
        
        Returns:
            list: Nueva población de Birds
        """
        # Calcular fitness de todos los individuos
        for bird in self.poblacion:
            bird.calcular_fitness()
        self.fitnesses = np.array([b.fitness for b in self.poblacion])
        
        # Selección elitista: preservar los mejores
        elite = self.seleccion_elitista(ELITE_SIZE)
        nueva_poblacion = [
            Pajaro(genes=e.genes.copy(), imagen_vivo=imagen_vivo, imagen_muerto=imagen_muerto) 
            for e in elite
        ]
        
        # Generar el resto mediante selección, crossover y mutación
        while len(nueva_poblacion) < NUM_PAJAROS:
            # Seleccionar padres por torneo
            padre1 = self.seleccion_por_torneo()
            padre2 = self.seleccion_por_torneo()
            # Crossover
            hijos = self.crossover_blend(padre1, padre2)
            
            # Mutación y agregar a la nueva población
            for hijo in hijos:

                fitness_promedio_padres = (padre1.fitness + padre2.fitness) / 2
                factor_reduccion_mutacion = 1.0 / (1.0 + (fitness_promedio_padres / 500))
                intensidad_minima = 0.01
                intensidad_mutacion = max(MUTATION_INTENSITY * factor_reduccion_mutacion, intensidad_minima)  # Centila de intensidad minima

                hijo.genes = self.mutacion(hijo.genes, intensidad_mutacion)
                # Asignar imágenes a los hijos
                hijo.imagen_vivo = imagen_vivo
                hijo.imagen_muerto = imagen_muerto
                hijo.image = imagen_vivo.copy() if imagen_vivo else None
                if hijo.image:
                    hijo.rect = hijo.image.get_rect()
                    hijo.rect.x = WIDTH // 4
                    hijo.rect.y = HEIGHT // 2
                
                nueva_poblacion.append(hijo)
                if len(nueva_poblacion) >= NUM_PAJAROS:
                    break
        
        return nueva_poblacion[:NUM_PAJAROS]

    def get_estadisticas(self):
        """
        Obtiene estadísticas de la población actual
        
        Returns:
            dict: Diccionario con estadísticas
        """
        return {
            'mejor_fitness': max(self.fitnesses),
            'peor_fitness': min(self.fitnesses),
            'promedio_fitness': np.mean(self.fitnesses),
            'mediana_fitness': np.median(self.fitnesses),
            'desviacion_fitness': np.std(self.fitnesses)
        }
