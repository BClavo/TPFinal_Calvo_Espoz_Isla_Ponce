"""
Módulo de Algoritmo Genético para Flappy Bird.

Este módulo implementa un algoritmo genético completo que evoluciona una
población de pájaros para mejorar su desempeño en el juego. Incluye:

- Métodos de selección (torneo, ruleta, elitista)
- Operadores de crossover (un punto, blend)
- Mutación adaptativa basada en fitness
- Estadísticas de población

El algoritmo sigue el ciclo evolutivo:
    1. Evaluación de fitness
    2. Selección de padres
    3. Reproducción (crossover)
    4. Mutación
    5. Formación de nueva generación

"""

import numpy as np
from numpy import ndarray
from classes import Pajaro
from config import *


class Poblacion:
    """
    Gestiona la evolución genética de una población de pájaros.

    Esta clase encapsula toda la lógica del algoritmo genético, incluyendo
    selección, crossover, mutación y formación de nuevas generaciones.

    Atributos:
        poblacion (list[Pajaro]): Lista de individuos de la población actual.
        fitnesses (ndarray): Array con los valores de fitness de cada individuo.
        genes (ndarray): Matriz (n_individuos x 6) con los genomas.
        promedio_genes (ndarray): Vector con el promedio de cada gen en la población.
        desviacion_genes (ndarray): Vector con la desviación estándar de cada gen.

    """

    def __init__(self, poblacion: list[Pajaro]) -> None:
        """
        Inicializa la población y calcula estadísticas genéticas.

        Args:
            poblacion: Lista de pájaros que conforman la población inicial.
        """
        self.poblacion: list[Pajaro] = poblacion
        
        # Extraer fitness de todos los individuos
        self.fitnesses: ndarray = np.array([b.fitness for b in self.poblacion])
        
        # Extraer genes de todos los individuos (matriz n×6)
        self.genes: ndarray = np.array([b.genes for b in self.poblacion])
        
        # Calcular estadísticas del genoma poblacional
        self.promedio_genes: ndarray = np.mean(self.genes, axis=0)
        self.desviacion_genes: ndarray = np.std(self.genes, axis=0)

    def seleccion_por_torneo(self, k: int = 5) -> Pajaro:
        """
        Selecciona un individuo mediante torneo aleatorio.

        Elige k individuos al azar y retorna el que tenga mejor fitness.
        Este método balancea exploración y explotación.

        Args:
            k: Tamaño del torneo (cantidad de competidores).

        Returns:
            El pájaro ganador del torneo (mejor fitness entre los k).

        Note:
            Un k mayor favorece la convergencia (explotación).
            Un k menor mantiene diversidad (exploración).
        """
        # Seleccionar k índices aleatorios sin reemplazo
        indices: ndarray = np.random.choice(len(self.poblacion), k, replace=False)
        
        # Encontrar el índice con mejor fitness entre los seleccionados
        mejor_idx: int = indices[np.argmax(self.fitnesses[indices])]
        
        return self.poblacion[mejor_idx]

    def seleccion_por_ruleta(self) -> Pajaro:
        """
        Selecciona un individuo con probabilidad proporcional a su fitness.

        Implementa el método de selección por ruleta (roulette wheel selection):
        individuos con mayor fitness tienen mayor probabilidad de ser elegidos,
        pero todos tienen alguna probabilidad de selección.

        Returns:
            Individuo seleccionado según probabilidades proporcionales.

        Note:
            Este método puede dar demasiada ventaja a individuos muy superiores,
            causando convergencia prematura. Se recomienda usar con mutación alta.

        Raises:
            ValueError: Si la suma de fitness es cero (todos muertos instantáneamente).
        """
        # Calcular probabilidades proporcionales al fitness
        suma_fitness: float = np.sum(self.fitnesses)
        
        # Evitar división por cero si todos tienen fitness 0
        if suma_fitness == 0:
            probabilidades: ndarray = np.ones(len(self.poblacion)) / len(self.poblacion)
        else:
            probabilidades: ndarray = self.fitnesses / suma_fitness
        
        # Elegir un índice según las probabilidades calculadas
        idx: int = np.random.choice(len(self.poblacion), p=probabilidades)
        
        return self.poblacion[idx]

    def seleccion_elitista(self, n_elite: int = ELITE_SIZE) -> list[Pajaro]:
        """
        Selecciona los mejores n individuos para elitismo.

        El elitismo garantiza que los mejores individuos pasen intactos
        a la siguiente generación, evitando la pérdida de soluciones óptimas.

        Args:
            n_elite: Cantidad de individuos élite a preservar.

        Returns:
            Lista con los n mejores individuos ordenados por fitness.

        Note:
            El elitismo acelera la convergencia pero puede reducir diversidad.
            Un buen balance es 10-20% de la población.
        """
        # Obtener índices ordenados por fitness (descendente)
        ordenados: ndarray = np.argsort(self.fitnesses)[::-1]
        
        # Retornar los primeros n_elite individuos
        return [self.poblacion[i] for i in ordenados[:n_elite]]

    def crossover_un_punto(self, p1: Pajaro, p2: Pajaro) -> list[Pajaro]:
        """
        Realiza crossover de un punto entre dos padres.

        Elige un punto de corte aleatorio y intercambia los genes:
            Hijo1: genes[0:punto] de p1 + genes[punto:] de p2
            Hijo2: genes[0:punto] de p2 + genes[punto:] de p1

        Args:
            p1: Primer padre.
            p2: Segundo padre.

        Returns:
            Lista con dos hijos generados por el crossover.

        Note:
            Este método es simple pero puede romper grupos de genes
            que funcionen bien juntos (epistasis).
        """
        # Elegir punto de corte aleatorio (evitando extremos)
        punto: int = np.random.randint(1, len(p1.genes) - 1)
        
        # Crear hijos intercambiando segmentos
        h1: ndarray = np.concatenate([p1.genes[:punto], p2.genes[punto:]])
        h2: ndarray = np.concatenate([p2.genes[:punto], p1.genes[punto:]])
        
        return [Pajaro(h1), Pajaro(h2)]

    def crossover_blend(self, p1: Pajaro, p2: Pajaro, alpha: float = 0.8) -> list[Pajaro]:
        """
        Realiza crossover por mezcla (blend crossover).

        Combina los genes de ambos padres mediante promedio ponderado:
            Hijo1 = p1 * α + p2 * (1 - α)
            Hijo2 = p2 * α + p1 * (1 - α)

        Args:
            p1: Primer padre.
            p2: Segundo padre.
            alpha: Factor de mezcla (0.0-1.0). Valores cercanos a 1.0
                   hacen que el hijo se parezca más al primer padre.

        Returns:
            Lista con dos hijos generados por mezcla.

        Note:
            Este método preserva mejor las relaciones entre genes que
            el crossover de un punto, siendo ideal para problemas continuos.
        """
        # Mezclar genes mediante combinación lineal
        h1: ndarray = p1.genes * alpha + p2.genes * (1 - alpha)
        h2: ndarray = p2.genes * alpha + p1.genes * (1 - alpha)
        
        return [Pajaro(h1), Pajaro(h2)]

    def mutacion(self, genes: ndarray, intensity: float) -> ndarray:
        """
        Aplica mutación gaussiana a un vector de genes.

        Cada gen tiene probabilidad MUTATION_RATE de mutar. Si muta,
        se le suma ruido gaussiano de media 0 y desviación intensity.

        Args:
            genes: Vector de genes a mutar (array de 6 elementos).
            intensity: Desviación estándar del ruido gaussiano aplicado.

        Returns:
            Nuevo vector de genes mutados, con valores en [-1.5, 1.5].

        Note:
            La intensidad adaptativa permite reducir mutaciones cuando
            la población se acerca al óptimo, mejorando convergencia fina.
        """
        rate: float = MUTATION_RATE
        
        # Crear máscara booleana: True indica que el gen mutará
        mascara: ndarray = np.random.rand(*genes.shape) < rate
        
        # Generar ruido gaussiano para cada gen
        ruido: ndarray = np.random.normal(0, intensity, genes.shape)
        
        # Aplicar mutación solo donde la máscara es True
        nuevos_genes: ndarray = np.where(mascara, genes + ruido, genes)
        
        # Asegurar que los genes permanezcan en el rango válido
        return np.clip(nuevos_genes, -1.5, 1.5)

    def crear_nueva_generacion(
        self,
        imagen_vivo: pygame.Surface = None,
        imagen_muerto: pygame.Surface = None
    ) -> list[Pajaro]:
        """
        Genera una nueva población mediante el algoritmo genético completo.

        Pasos del algoritmo:
            1. Calcular fitness de todos los individuos
            2. Aplicar elitismo (mejores pasan directamente)
            3. Seleccionar padres mediante ruleta
            4. Generar hijos con crossover blend
            5. Aplicar mutación adaptativa a los hijos
            6. Completar la población hasta NUM_PAJAROS

        Args:
            imagen_vivo: Superficie de Pygame para pájaros vivos.
            imagen_muerto: Superficie de Pygame para pájaros muertos.

        Returns:
            Lista con NUM_PAJAROS nuevos individuos para la siguiente generación.

        Note:
            La mutación adaptativa reduce su intensidad cuando los padres
            tienen alto fitness, permitiendo ajustes finos cerca del óptimo.
        """
        # Paso 1: Actualizar fitness de todos los individuos
        for bird in self.poblacion:
            bird.calcular_fitness()
        
        self.fitnesses = np.array([b.fitness for b in self.poblacion])

        # Paso 2: Seleccionar élite (mejores individuos pasan sin cambios)
        elite: list[Pajaro] = self.seleccion_elitista(ELITE_SIZE)
        
        # Crear copias de la élite para la nueva generación
        nueva_poblacion: list[Pajaro] = [
            Pajaro(
                genes=e.genes.copy(),
                imagen_vivo=imagen_vivo,
                imagen_muerto=imagen_muerto
            )
            for e in elite
        ]

        # Paso 3-6: Generar resto de la población mediante reproducción
        while len(nueva_poblacion) < NUM_PAJAROS:
            # Seleccionar dos padres mediante ruleta
            padre1: Pajaro = self.seleccion_por_ruleta()
            padre2: Pajaro = self.seleccion_por_ruleta()

            # Generar dos hijos mediante crossover blend
            # hijos: list[Pajaro] = self.crossover_blend(padre1, padre2)
            hijos: list[Pajaro] = self.crossover_un_punto(padre1, padre2)

            # Procesar cada hijo
            for hijo in hijos:
                # Calcular intensidad de mutación adaptativa
                # Padres con alto fitness → mutación más suave
                fitness_promedio_padres: float = (padre1.fitness + padre2.fitness) / 2
                factor_reduccion_mutacion: float = 1.0 / (
                    1.0 + (fitness_promedio_padres / 500)
                )
                intensidad_minima: float = 0.01
                intensidad_mutacion: float = max(
                    MUTATION_INTENSITY * factor_reduccion_mutacion,
                    intensidad_minima
                )

                # Aplicar mutación
                hijo.genes = self.mutacion(hijo.genes, intensidad_mutacion)
                
                # Asignar imágenes al hijo
                hijo.imagen_vivo = imagen_vivo
                hijo.imagen_muerto = imagen_muerto
                hijo.image = imagen_vivo.copy() if imagen_vivo else None

                # Configurar rectángulo de colisión
                if hijo.image:
                    hijo.rect = hijo.image.get_rect()
                    hijo.rect.x = WIDTH // 4
                    hijo.rect.y = HEIGHT // 2

                # Agregar hijo a la nueva población
                nueva_poblacion.append(hijo)
                
                # Detener si alcanzamos el tamaño deseado
                if len(nueva_poblacion) >= NUM_PAJAROS:
                    break

        # Retornar exactamente NUM_PAJAROS individuos
        return nueva_poblacion[:NUM_PAJAROS]

    def get_estadisticas(self) -> dict[str, float]:
        """
        Calcula estadísticas descriptivas del fitness de la población.

        Returns:
            Diccionario con las siguientes métricas:
                - mejor_fitness: Máximo fitness de la población.
                - peor_fitness: Mínimo fitness de la población.
                - promedio_fitness: Media aritmética del fitness.
                - mediana_fitness: Mediana del fitness.
                - desviacion_fitness: Desviación estándar del fitness.

        """
        return {
            'mejor_fitness': float(np.max(self.fitnesses)),
            'peor_fitness': float(np.min(self.fitnesses)),
            'promedio_fitness': float(np.mean(self.fitnesses)),
            'mediana_fitness': float(np.median(self.fitnesses)),
            'desviacion_fitness': float(np.std(self.fitnesses))
        }