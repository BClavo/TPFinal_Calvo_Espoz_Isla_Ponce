# 🧬 FLAPPY BIRD GENÉTICO - TP3_Calvo_Espoz_Isla_Ponce
## Simulador de Algoritmos Genéticos con Pygame
---

# 🧠 ÍNDICE COMPLETO

1. **Descripción general**
2. **Características principales**
3. **Estructura del proyecto**
4. **Requisitos previos**
5. **Instrucciones de uso**
6. **Algoritmo Genético — Detalles técnicos**
7. **Visualización de datos con Matplotlib**
8. **Sistema de temas**
9. **Configuración avanzada**
10. **Librerías utilizadas**
    * 10.1 Pygame (TODAS las funciones importantes explicadas)
    * 10.2 NumPy (TODAS las funciones relevantes explicadas)
    * 10.3 Matplotlib (TODAS las funciones utilizadas y explicación profunda)
11. **Por qué usamos NumPy y Matplotlib**
12. **Guía completa: Cómo utilizar el juego con videos demostrativos**
13. **Estrategias de optimización implementadas**
14. **Resultados esperados**
15. **Créditos y licencia**

---

## 📋 1. Descripción general


Este proyecto implementa una versión evolutiva del clásico juego **Flappy Bird**, donde una población de pájaros aprende a jugar mediante **algoritmos genéticos**. El sistema simula la evolución natural: los pájaros con mejor desempeño transmiten sus genes a la siguiente generación, mejorando progresivamente su capacidad para superar obstáculos.

El proyecto incluye dos modos de juego:

🤖 **Modo Simulador**: Observa cómo 100 pájaros evolucionan automáticamente generación tras generación, utilizando redes neuronales simples para tomar decisiones.

🎮 **Modo Clásico**: Juega manualmente al estilo tradicional de Flappy Bird, controlando un solo pájaro con la barra espaciadora.

---

## 🎯 2.Características principales

- **Algoritmo genético completo**: Selección por torneo/ruleta, crossover blend, mutación adaptativa y elitismo
- **Visualización en tiempo real**: Gráficos de fitness, genoma promedio y estadísticas detalladas
- **7 temas visuales personalizables**: Default, Espacio, Agua, Bosque, Mitología, Stranger Things y UdeSA
- **Sistema de audio completo**: Música de fondo y efectos de sonido (aleteo, colisión, puntos)
- **Control de velocidad**: Acelera la simulación 2x para evolucionar más rápido
- **Métricas avanzadas**: Fitness, distancia recorrida, tuberías pasadas, tiempo de supervivencia

---

## 📁 3. Estructura del proyecto

```
flappy-bird-genetico/
│
├── main.py                      # Punto de entrada del programa
├── menu.py                      # Sistema de menús y navegación
├── game.py                      # Lógica principal del juego
├── classes.py                   # Clases de sprites y componentes
├── algoritmo_genetico.py        # Implementación del algoritmo genético
├── config.py                    # Configuración y constantes
│
├── sprites/                     # Recursos visuales
│   ├── temas/                   # 7 temas diferentes
│   │   ├── default/
│   │   ├── espacio/
│   │   ├── agua/
│   │   ├── bosque/
│   │   ├── mitologia/
│   │   ├── stranger/
│   │   └── udesa/
│   └── [imágenes de menú]
│
└── sounds/                      # Efectos de sonido y música
    ├── music.ogg
    ├── menu_music.wav
    └── [efectos sfx]
```

---

## 🚀 4. Requisitos previos

- **Python 3.9 o superior**
- **Instalación de dependencias**:
   ```bash
   pip install pygame numpy matplotlib
   ```

---

## 🎮 5. Instrucciones de uso

### Ejecutar el juego

```bash
python main.py
```

### Controles

**En el Menú:**
- **Click izquierdo**: Seleccionar opciones

**Modo Simulador:**
- **ESPACIO**: Forzar nueva generación
- **CTRL**: Acelerar simulación 2x
- **R**: Reiniciar desde generación 1
- **ESC**: Volver al menú

**Modo Clásico:**
- **ESPACIO**: Aletear
- **R**: Reiniciar
- **ESC**: Volver al menú

---

## 🧬 6. Algoritmo Genético

### Representación de los genes

Cada pájaro tiene un **genoma de 6 pesos** que determina su comportamiento:

```python
genes = [w0, w1, w2, w3, w4, w5]
```

**Función de decisión de aleteo:**
```python
valor = w0 + w1*Δy + w2*Δy² + w3*Δx + w4*Δx² + w5*vy
aletear = (valor > 0)
```

Donde:
- `Δy`: Diferencia vertical entre el pájaro y el centro del hueco
- `Δx`: Distancia horizontal hasta la próxima tubería
- `vy`: Velocidad vertical actual

### Pipeline evolutivo

1. **Evaluación de fitness**:
   ```python
   fitness = distancia * 1.5 + tuberías_pasadas * 300 + bonus_supervivencia
   ```

2. **Selección**:
   - **Elitismo**: Los mejores 20 individuos pasan directamente
   - **Selección por ruleta**: Probabilidad proporcional al fitness

3. **Crossover Blend**:
   ```python
   hijo1 = padre1 * α + padre2 * (1 - α)
   hijo2 = padre2 * α + padre1 * (1 - α)
   ```

4. **Mutación adaptativa**:
   - Intensidad reducida para individuos con alto fitness
   - Tasa de mutación: 20% (configurable)
   - Rango de genes: [-1.5, 1.5]

---

## 📊 7. Visualización de datos

### Panel lateral en tiempo real

**Estadísticas mostradas:**
- Generación actual
- Pájaros vivos / total
- Tiempo de la generación
- Tuberías pasadas (actual)
- Velocidad de simulación
- Distancia actual/promedio/mejor
- Mejor fitness histórico

### Gráficos interactivos

1. **Gráfico de fitness promedio vs generación**
   - Muestra la evolución del fitness a lo largo de las generaciones

2. **Gráfico del genoma (Promedio ± Desviación estándar)**
   - Visualiza cada peso genético
   - Barras verdes (positivas) y rojas (negativas)
   - Área gris muestra la desviación estándar

---

## 🎨 8. Sistema de temas

### Temas disponibles

| Tema | Descripción |
|------|-------------|
| **Default** | Tema clásico de Flappy Bird |
| **Espacio** | Temática espacial futurista |
| **Agua** | Ambiente submarino |
| **Bosque** | Entorno natural con árboles |
| **Mitología** | Inspirado en mitología griega |
| **Stranger** | Estética de Stranger Things |
| **UdeSA** | Tema personalizado universitario |

### Personalización

1. Seleccionar **"Personalizar"** en el menú principal
2. Usar flechas laterales para navegar entre temas
3. Vista previa de personaje, tubería y fondo
4. Confirmar con el botón **"Elegir"**

---

## 🔧 9. Configuración avanzada

### Parámetros genéticos (en `config.py`)

```python
NUM_PAJAROS = 100           # Tamaño de la población
MAX_GENERATIONS = 100       # Generaciones máximas
ELITE_SIZE = 20             # Individuos élite preservados
MUTATION_RATE = 0.2         # Tasa de mutación (20%)
MUTATION_INTENSITY = 0.4    # Intensidad de la mutación
BONUS_POR_TUBERIA = 300     # Puntos por tubería pasada
```

### Física del juego

```python
GRAVITY = 0.5               # Gravedad aplicada
FLAP_STRENGTH = -10         # Fuerza del aleteo
PIPE_SPEED = 6              # Velocidad de las tuberías
PIPE_GAP = 250              # Tamaño del hueco
```

### Ajustes de audio

```python
MUSIC_VOLUME = 0.4          # Volumen de música (0.0 - 1.0)
SFX_VOLUME = 0.5            # Volumen de efectos (0.0 - 1.0)
```

---

#  10. Librerías utilizadas 

Funciones relevantes de:

* **Pygame** (motor del juego)
* **NumPy** (cálculos del algoritmo genético)
* **Matplotlib** (gráficos dinámicos dentro del juego)

-**qué hace cada función, cuándo se usa y por qué es necesaria**.

---

## 🎮 10.1 PYGAME – TODAS LAS FUNCIONES IMPORTANTES EXPLICADAS

Pygame es el **motor central del proyecto**. Renderiza sprites, procesa eventos, maneja el audio, controla el framerate y permite dibujar gráficos. 

---

### 🔷 A. Inicialización y ventana

#### `pygame.init()` - Inicializa todos los módulos de Pygame: display, audio, teclado, tiempo.

#### `pygame.display.set_mode((w,h))` - Crea la ventana del juego.

#### `pygame.display.set_caption("texto")` - Define el nombre de la ventana.

#### `pygame.display.set_icon(surface)` - Cambia el ícono de la ventana.

---

### 🔷 B. Eventos / Input

#### `pygame.event.get()` - Devuelve una lista con todos los eventos (teclado, mouse, cerrar ventana).

#### `pygame.KEYDOWN`, `pygame.MOUSEBUTTONDOWN`, `pygame.QUIT` - Constantes que representan tipos de evento.

#### `event.key == pygame.K_SPACE` - Revisa teclas específicas.

#### `pygame.mouse.get_pos()` - Devuelve la posición actual del mouse.

---

### 🔷 C. Imágenes

#### `pygame.image.load(path)` - Carga una imagen en un `Surface`.

#### `Surface.convert_alpha()` - Convierte la imagen para permitir transparencia.

#### `pygame.transform.scale(surface, (w,h))` - Escala imágenes (muy usado en tu juego para fondos, pájaros y tuberías).

---

### 🔷 D. Sprites

🧩 ¿Qué es **pygame.sprite.Sprite**?
Es una clase base que facilita la creación y manejo de objetos gráficos (sprites) en un juego. Un sprite es básicamente cualquier objeto visual que aparece en pantalla: personajes, obstáculos, proyectiles, etc.

El proyecto usa **pygame.sprite.Sprite** para pájaros y tuberías para:
   * Colisiones automáticas
      - Pygame ofrece funciones como `pygame.sprite.spritecollide()` o `pygame.sprite.groupcollide()` que detectan choques entre sprites.
      - Esto simplifica mucho la lógica de verificar si el pájaro toca una tubería.
   * Grupos de sprites
      - Se puede agrupar pájaros y tuberías en pygame.sprite.Group().
      - Con un solo método (`group.update()` o `group.draw(surface)`) actualizas o dibujas todos los objetos, en lugar de hacerlo uno por uno.

#### `class Pajaro(pygame.sprite.Sprite)` - Sprites con colisiones y física.

#### `class Tuberia(pygame.sprite.Sprite)` - Sprites móviles que se desplazan hacia la izquierda.

#### `pygame.sprite.Group()`

Agrupa sprites para:

- Dibujarlos
- Actualizarlos
- Detectar colisiones

#### `pygame.sprite.spritecollideany(obj, grupo)` - Devuelve True si `obj` colisiona con algún elemento del grupo.

---

### 🔷 E. Tiempo / FPS

#### `pygame.time.Clock()` - Controla el framerate del juego.

#### `clock.tick(FPS)` - Limita la actualización a FPS cuadros por segundo.

#### `pygame.time.get_ticks()` - Devuelve el tiempo en milisegundos desde que inició el juego.

Usado para:

* Identificar tuberías (`id_tuberia`)
* Cooldown de sonidos
* Control de generaciones

---

### 🔷 F. Audio

El SoundManager utiliza **estas funciones**:

#### `pygame.mixer.init()` - Inicializa el motor de audio.

#### `pygame.mixer.Sound(path)` - Carga efectos de sonido.

#### `sound.play()` - Reproduce un efecto de sonido.

#### `sound.set_volume(vol)` - Cambia su volumen.

#### `pygame.mixer.music.load(path)` - Carga música de fondo.

#### `pygame.mixer.music.play(loop)` - Reproduce música (en loop infinito).

---

### 🔷 G. Dibujar en pantalla

#### `surface.blit(imagen, (x,y))` - Dibuja imágenes.

#### `pygame.draw.rect(surface,color,rect,border_radius)` - Dibuja paneles, botones, gráficos, etc.

#### `pygame.draw.line(surface,color,(x1,y1),(x2,y2))` - Dibuja líneas (usado para separación en panel lateral).

#### `pygame.draw.lines(surface,color,closed,points,width)` - Dibuja la línea del gráfico de fitness.

---

### 🔷 H. Colisiones, rectángulos y posición

#### `surface.get_rect()` - Crea un rectángulo alrededor del sprite.

#### `rect.x`, `rect.y` - Coordenadas del objeto.

#### `rect.top`, `rect.bottom`, `rect.center` - Propiedades útiles en física.

---

## 🔢 10.2 NUMPY – TODAS LAS FUNCIONES USADAS Y SU ROL

NumPy es el corazón del **algoritmo genético**. Permite operar vectores/genes de forma rápida.

---

### 📌 Funciones usadas

#### `np.random.uniform(a, b, size)` - Genera genes iniciales aleatorios en rango [-1.5, 1.5].

#### `np.array([...])` - Transforma listas en vectores.

#### `np.mean(vectores, axis=0)`

Calcula la media de cada gen en la población.
Se usa para mostrar el **genoma promedio**.

#### `np.std(vectores, axis=0)` - Calcula desviación estándar → Varianza genética.

#### `np.argsort(array)` - Ordena individuos por fitness (para elitismo).

#### `np.random.choice(n, p=prob)` - Selección por ruleta.

#### `np.random.normal(0, intensity, shape)` - Mutación gaussiana.

#### `np.clip(array, min, max)` - Garantiza que los genes no salgan del rango [-1.5,1.5].

---

## 📊 10.3 MATPLOTLIB – TODAS LAS FUNCIONES Y EXPLICACIÓN PROFUNDA

Matplotlib se usa dentro de Pygame gracias a:

#### `matplotlib.use("Agg")` - Permite renderizar gráficos **sin abrir ventanas externas**.

---

### Funciones fundamentales

#### `plt.subplots(figsize=(w,h), dpi=100)` - Crea figura + eje.

#### `ax.barh()` - Crea barras horizontales para visualizar los genes.

#### `ax.set_facecolor(color)` - Define fondo del gráfico.

#### `ax.grid(axis="x")` - Dibuja líneas grises verticales para facilitar lectura.

#### `ax.set_yticks()`, `ax.set_yticklabels()` - Labels personalizados: w0, w1, w2…

#### `ax.text(x,y,text)` - Imprime el valor numérico sobre cada barra.

#### `fig.canvas.draw()` - Renderiza el gráfico en memoria.

#### `fig.canvas.buffer_rgba()` - Extrae la imagen como bytes → se convierte a `pygame.Surface`.

---

## 🧠 11. ¿POR QUÉ USAMOS NUMPY + MATPLOTLIB?

### 🔢 **NumPy**

Porque permite evolucionar una población de 100 individuos en milisegundos:

* Operaciones vectoriales ultrarrápidas
* Mutación y crossover por lotes
* Cálculo estadístico instantáneo

Un AG sin NumPy sería **100x más lento**.

---

### 📊 **Matplotlib**

Porque permite:

* Visualizar la evolución genética
* Dibujar barras con varianza
* Renderizar gráficos dentro del juego mediante Pygame

Pygame NO tiene gráficos estadísticos → Matplotlib resuelve eso.

---

## 🎥 12. CÓMO UTILIZAR EL JUEGO (DEMOSTRACIONES EN VIDEO)

---

### 🎬 **Video 1 — Cómo funciona el modo Simulador**


[VIDEO: modo simulador](assets/v_simulador.mp4)

---

### 🎬 **Video 2 — Cómo jugar en Modo Clásico**

[VIDEO: modo clásico](assets/v_clasico.mp4)

---

### 🎬 **Video 3 — Personalización de Temas**

[VIDEO: personalización ](assets/v_personalizar.mp4)

---

## 🏆 13. Estrategias de optimización implementadas

### 1. Mutación adaptativa
La intensidad de mutación disminuye cuando los padres tienen alto fitness:
```python
factor_reduccion = 1.0 / (1.0 + (fitness_promedio_padres / 500))
intensidad = max(MUTATION_INTENSITY * factor_reduccion, 0.01)
```

### 2. Fitness compuesto
Combina múltiples métricas para una evaluación robusta:
- Distancia recorrida (exploración)
- Tuberías pasadas (objetivo principal)
- Bonus de supervivencia prolongada (estabilidad)

### 3. Cooldown de efectos de sonido
Evita saturación de audio con tiempos de cooldown:
```python
if current_time - last_play_time > cooldown:
    sound.play()
```

### 4. Actualización condicional de gráficos
Los gráficos solo se regeneran cuando cambia la generación:
```python
if generation == self.last_generation:
    return  # No recalcular
```

---

## 📈 14. Resultados esperados

### Evolución típica

- **Generación 1-5**: Pájaros mueren rápidamente, pocos pasan tuberías
- **Generación 10-20**: Comienzan a aparecer estrategias básicas
- **Generación 30-50**: Mejora significativa, pasan 5-10 tuberías
- **Generación 70+**: Individuos élite pueden pasar 20+ tuberías

### Convergencia del genoma

Con el tiempo, los pesos genéticos convergen hacia valores óptimos:
- `w1` (Δy) suele volverse fuertemente negativo (volar cuando está bajo)
- `w3` (Δx) influye en el timing del aleteo
- `w5` (vy) ayuda a controlar la velocidad vertical


---

## 👥 15. Créditos

**Desarrolladores:**
- Calvo, Bautista
- Espoz, Rocío
- Isla, Ivan
- Ponce Albarracin, Adrian Santiago
---
- Materia: Pensamiento Computacional
- Universidad: Universidad de San Andrés
- Año: 2025

---
