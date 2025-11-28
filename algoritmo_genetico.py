import numpy as np
from classes import Pajaro
from config import *

class Poblacion:
    """Maneja la evolución genética de la población de pájaros.

    Args:
        poblacion (list[Pajaro]): Lista inicial de pájaros.
    """

    def __init__(self, poblacion: list):
        self.poblacion = poblacion
        self.fitnesses = np.array([b.fitness for b in self.poblacion])
        self.genes = np.array([b.genes for b in self.poblacion])
        self.promedio_genes = np.mean(self.genes, axis=0)
        self.desviacion_genes = np.std(self.genes, axis=0)

    def seleccion_por_torneo(self, k: int = 3):
        """Selecciona el mejor pájaro dentro de un torneo aleatorio de tamaño ``k``.

        Args:
            k (int): Cantidad de pájaros por torneo.

        Returns:
            Pajaro: Pájaro con mejor fitness dentro del torneo.
        """
        indices = np.random.choice(len(self.poblacion), k, replace=False)
        mejor_idx = indices[np.argmax(self.fitnesses[indices])]
        return self.poblacion[mejor_idx]

    def seleccion_elitista(self, n_elite: int = ELITE_SIZE):
        """Selecciona los mejores individuos y los pasa directamente a la siguiente generación.

        Args:
            n_elite (int): Cantidad de pájaros que se preservan como élite.

        Returns:
            list[Pajaro]: Lista con los mejores pájaros.
        """
        ordenados = np.argsort(self.fitnesses)[::-1]
        return [self.poblacion[i] for i in ordenados[:n_elite]]

    def crossover_un_punto(self, p1, p2):
        """Realiza un crossover de un punto entre dos padres.

        Args:
            p1 (Pajaro): Primer padre.
            p2 (Pajaro): Segundo padre.

        Returns:
            list[Pajaro]: Hijos generados por el crossover.
        """
        punto = np.random.randint(1, len(p1.genes) - 1)
        h1 = np.concatenate([p1.genes[:punto], p2.genes[punto:]])
        h2 = np.concatenate([p2.genes[:punto], p1.genes[punto:]])
        return [Pajaro(h1), Pajaro(h2)]

    def crossover_blend(self, p1, p2, alpha: float = 0.8):
        """Mezcla los genes de dos padres según un factor ``alpha``.

        Args:
            p1 (Pajaro): Primer padre.
            p2 (Pajaro): Segundo padre.
            alpha (float): Porcentaje de mezcla.

        Returns:
            list[Pajaro]: Hijos resultantes de la mezcla.
        """
        h1 = p1.genes * alpha + p2.genes * (1 - alpha)
        h2 = p2.genes * alpha + p1.genes * (1 - alpha)
        return [Pajaro(h1), Pajaro(h2)]

    def mutacion(self, genes, intensity: float):
        """Aplica mutación a un vector de genes.

        Args:
            genes (np.ndarray): Vector de genes a mutar.
            intensity (float): Intensidad máxima de la mutación.

        Returns:
            np.ndarray: Nuevos genes mutados.
        """
        rate = MUTATION_RATE
        mascara = np.random.rand(*genes.shape) < rate
        ruido = np.random.uniform(-intensity, intensity, genes.shape)
        nuevos_genes = np.where(mascara, genes + ruido, genes)
        return np.clip(nuevos_genes, -3, 3)

    def crear_nueva_generacion(self, imagen_vivo=None, imagen_muerto=None):
        """Crea una nueva generación aplicando elitismo, selección, crossover y mutación.

        Args:
            imagen_vivo: Imagen asignada a los pájaros vivos.
            imagen_muerto: Imagen asignada a los pájaros muertos.

        Returns:
            list[Pajaro]: Nueva población generada.
        """
        for bird in self.poblacion:
            bird.calcular_fitness()
        self.fitnesses = np.array([b.fitness for b in self.poblacion])

        elite = self.seleccion_elitista(ELITE_SIZE)
        nueva_poblacion = [
            Pajaro(genes=e.genes.copy(), imagen_vivo=imagen_vivo, imagen_muerto=imagen_muerto)
            for e in elite
        ]

        while len(nueva_poblacion) < NUM_PAJAROS:
            padre1 = self.seleccion_por_torneo()
            padre2 = self.seleccion_por_torneo()

            hijos = self.crossover_blend(padre1, padre2)

            for hijo in hijos:
                fitness_promedio_padres = (padre1.fitness + padre2.fitness) / 2
                factor_reduccion_mutacion = 1.0 / (1.0 + (fitness_promedio_padres / 500))
                intensidad_minima = 0.01
                intensidad_mutacion = max(MUTATION_INTENSITY * factor_reduccion_mutacion, intensidad_minima)

                hijo.genes = self.mutacion(hijo.genes, intensidad_mutacion)
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

    def get_estadisticas(self) -> dict:
        """Devuelve estadísticas descriptivas del fitness de la población.

        Returns:
            dict: Diccionario con estadísticas clave del fitness.
        """
        return {
            'mejor_fitness': max(self.fitnesses),
            'peor_fitness': min(self.fitnesses),
            'promedio_fitness': np.mean(self.fitnesses),
            'mediana_fitness': np.median(self.fitnesses),
            'desviacion_fitness': np.std(self.fitnesses)
        }
