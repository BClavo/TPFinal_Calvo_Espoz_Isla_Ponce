import random
import numpy as np

class Pajaro:
    def __init__(self,genes=None):
        if genes == None:
            self.genes = [random.uniform(-1,1) for _ in range(0,6)] #Genera los genes de forma aleatoria, representados como vectores de 6 elementos.
        else:
            self.genes = genes

        #self.y = altura_de_la pantalla // 2 #El pajaro se inicia en la mitad de la pantalla.
        self.vy = 0 #Velocidad para subir y bajar
        self.x = 0
        self.vivo = True

    def aleteo(self, delta_y, delta_x):
        w0,w1,w2,w3,w4,w5 = self.genes
        valor = w0 + w1*delta_y + w2*(delta_y**2)+w3*delta_x+w4*(delta_x**2) + w5 * self.vy
        return valor > 0 #Si es menor a cero no aletea, si es mayor a 0 aletea.

    def actualizar_posicion(self, delta_y, delta_x, aleteo, gravedad = 0.5,fuerza_de_aleteo = -10):
        if aleteo:
            self.vy += fuerza_de_aleteo

        self.vy += gravedad
        self.y = self.vy

        # <========== CASO DE COLISIONES ===============>










