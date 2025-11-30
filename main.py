import pygame
from config import *
from game import Juego
from menu import MenuPrincipal


def main():
    """Función principal que inicia el juego"""
    # Inicializar Pygame
    pygame.init()
    
    # Crear ventana
    pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird Genetico")
    icono = pygame.image.load(SPRITE_PATHS['icono']) 
    pygame.display.set_icon(icono)

    menu = MenuPrincipal(pantalla)
    menu.ejecutar()
    # generacion_final, mejor_fitness = Juego.run()
    
    # Cerrar Pygame
    pygame.quit()
    
    # Mostrar resultados finales
    # print(f"Generaciones completadas: {generación_final - 1}")
    # print(f"Mejor fitness alcanzado: {int(mejor_fitness)}")


if __name__ == "__main__":
    main()


