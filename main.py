import pygame
from config import *
from game import Juego
from menu import MenuPrincipal


def main():
    """Función principal que inicia el juego"""

    # Inicializar todos los módulos de Pygame (display, sound, joystick, etc.)
    pygame.init()
    
    # Crear ventana del juego con dimensiones configuradas
    pantalla: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    
    # Establecer título de la ventana
    pygame.display.set_caption("Flappy Bird Genetico")
    
    # Cargar y establecer ícono de la ventana
    icono: pygame.Surface = pygame.image.load(SPRITE_PATHS['icono'])
    pygame.display.set_icon(icono)

    # Crear instancia del menú principal
    menu: MenuPrincipal = MenuPrincipal(pantalla)
    
    # Ejecutar el bucle del menú
    menu.ejecutar()
 
    # Cerrar Pygame y liberar recursos
    pygame.quit()

  


if __name__ == "__main__":
    main()

