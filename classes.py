class Pajarito:
    def __init__ (self,tamaño=30,fuerza_aleteo=-10):
        self.tamaño=tamaño
        self.fuerza_aleteo=fuerza_aleteo
    
class Tuberia:
    def __init__(self,ancho=70,gap=200,min_gap=150,velocidad=6):
        self.ancho=ancho
        self.gap=gap
        self.min_gap=min_gap
        self.vel=velocidad

# class Fondo:
#     def __init__(self,ancho,alto):

class Juego:
    def __init__(self,ancho,fps,tiempo_max,gravedad):
        self.ancho=ancho
        self.fps=fps
        self.tiempo_max=tiempo_max
        self.gravedad=gravedad
    





{
	"WIDTH": 1000 ,
	"HEIGHT" : 600 ,
	"PANEL_WIDTH" : 280 ,
	"GAME_WIDTH" : 400 ,
	"FPS" : 60 ,
	"MAX_TIME" : 120 ,
	"GRAVITY" : 0.5 ,

	# "FLAP_STRENGTH" : -10 ,

	# "PIPE_WIDTH" : 70 ,
	# "PIPE_GAP" : 200  ,
	# "MIN_PIPE_GAP" : 150 ,
	# "PIPE_SPEED" : 6 ,

	# "BIRD_SIZE" : 30
}
