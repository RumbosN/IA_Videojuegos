import pygame, sys
from pygame.locals import *

def porCiento(valor, porcentaje):
	return valor*porcentaje//100

class Huella(pygame.sprite.Sprite):

	def __init__(self, px, py, inicio, alpha = 255):
		pygame.sprite.Sprite.__init__(self)
		# Ancho y Largo del elipse
		self.largo = 25 
		self.ancho = 10 

		# Posicion inicial de la superficie
		self.pos_ini_x = px - porCiento(self.largo,60)
		self.pos_ini_y = py-5

		self.color = pygame.Color(92,92,92, alpha) # Color de huella

		# Centro dado para la huella
		self.px = px 
		self.py = py 

		self.time = inicio # Cambiar el Alpha de la huella

		# Para que se pueda poner transparente, se pinta sobre una superficie
		self.alpha_surface =  pygame.Surface((self.largo+porCiento(self.largo,40)+5, self.ancho), pygame.SRCALPHA, 32)  # the size of your rect
		self.alpha_surface.set_alpha(128)


	def mostrar(self, surface):
		#### Suela ####
		# Datos Trapecio
		ROJO = 0xF01818
		sx1 = sx4 = (self.px-self.pos_ini_x) - porCiento(self.largo,10)
		sx2 = sx3 = (self.px-self.pos_ini_x) + porCiento(self.largo,50)
		sy2 = (self.py-self.pos_ini_y) - self.ancho//2 
		sy3 = (self.py-self.pos_ini_y) + self.ancho//2
		sy1, sy4 = sy2+porCiento(self.ancho,30), sy3-porCiento(self.ancho,30)
		puntos = ((sx1,sy1),(sx2,sy2),(sx3,sy3),(sx4,sy4))
		# Datos Elipse
		s_rect = pygame.Rect(((self.px-self.pos_ini_x), sy2, self.largo, self.ancho))

		pygame.draw.ellipse(self.alpha_surface, self.color, s_rect)
		pygame.draw.polygon(self.alpha_surface, self.color, puntos)
		
		#### Tacon ####
		# Datos Circulo
		radio = (sy4 - sy1 + 2) /  2
		tx = sx1 - porCiento(self.largo,30)
		ty = sy1 + radio
		pos = (tx,ty)
		# Datos Rectangulo
		t_rect = pygame.Rect((tx, sy1, porCiento(radio,105), 2*radio))
		
		pygame.draw.circle(self.alpha_surface, self.color, pos, radio)
		pygame.draw.rect(self.alpha_surface, self.color, t_rect)
		surface.blit(self.alpha_surface,(self.pos_ini_x,self.pos_ini_y))
		
	def update_color(self, seg):
		diferencia = seg - self.time
		escala = 50
		if diferencia > 0:
			self.time = seg
			if self.color.a - escala > 0:
				self.color.a -= escala
			


pygame.init()

ancho, alto = 1360,715
ventana = pygame.display.set_mode((ancho,alto))
pygame.display.set_caption("Prueba")
huella = Huella(100,100,pygame.time.get_ticks()//500)

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	ventana.fill(0xFFFFFF)
	huella.update_color(pygame.time.get_ticks()//500)
	huella.mostrar(ventana)
	#print pygame.mouse.get_pos()
	pygame.display.update()



