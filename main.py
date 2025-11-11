import pygame
from config import WIDTH, HEIGHT
from game import Juego


def main():
    """Función principal que inicia el juego"""
    # Inicializar Pygame
    pygame.init()
    
    # Crear ventana
    pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird Genético")
    
    # Crear y ejecutar el juego
    juego = Juego(pantalla)
    generacion_final, mejor_fitness = juego.run()
    
    # Cerrar Pygame
    pygame.quit()
    
    # Mostrar resultados finales
    print(f"Generaciones completadas: {generacion_final - 1}")
    print(f"Mejor fitness alcanzado: {int(mejor_fitness)}")



if __name__ == "__main__":
    main()


