import pygame, sys
from pygame.locals import *
from math import *


def porCiento(valor, porcentaje):
	return valor*porcentaje//100

def rot_center(supp, angle):
	print "superficie"
	print supp

	orig_rect = supp.get_rect()
	print "rectangulo de la superficie sin rotar"
	print orig_rect

	rot_supp = pygame.transform.rotate(supp, angle)
	print "superficie rotada"
	print rot_supp

	rot_rect = orig_rect.copy()
	print "rectangulo antes de rotar"
	print rot_rect

	print "rectangulo de la superficie rotada"
	print rot_supp.get_rect()
	print "centro del rectangulo de la superficie rotada"
	print rot_supp.get_rect().center


	
	rot_rect.center = rot_supp.get_rect().center
	print "rectangulo rotado"
	print rot_rect

	rot_supp = rot_supp.subsurface(rot_rect).copy()
	return rot_supp

def rotar_puntos(angulo, pu, pv):
	angulos = {90:pi,
					 30:pi/3,
					 45:pi/2,
					 0:0}
	alfa = angulos[angulo]
	px = cos(alfa)*pu - sin(alfa)*pv
	py = sin(alfa)*pu + cos(alfa)*pv
	return px,py

def techo (f):
	return int(ceil(f))

class Huella(pygame.sprite.Sprite):

	def __init__(self, px, py, orientation = 0, alpha = 255):
		pygame.sprite.Sprite.__init__(self)
		# Ancho y Largo del elipse
		self.largo = 25 
		self.ancho = 10 

		# Posicion inicial de la superficie
		self.pos_ini_x = px - porCiento(self.largo,60) 
		self.pos_ini_y = py-5
		# self.pos_ini_y = py-5
		self.orientation = orientation

		self.color = pygame.Color(92,92,92, alpha) # Color de huella

		# Centro dado para la huella
		self.px,self.py = rotar_puntos(orientation,px,py)

		# Para que se pueda poner transparente, se pinta sobre una superficie, pygame.SRCALPHA, 32
		self.alpha_surface =  pygame.Surface((self.largo+porCiento(self.largo,40)+5, self.ancho))  # the size of your rect
		# self.alpha_surface =  pygame.Surface((1000, 1000))  # the size of your rect
		self.alpha_surface.set_alpha(128)
		self.alpha_surface = pygame.transform.rotate(self.alpha_surface,self.orientation)

		#self.alpha_surface = rot_center(self.alpha_surface,self.orientation)


		# COLOCAR ALGO DE LA ORIENTACION DE LA SUPERFCIE?
		self.i=0

	def mostrar(self, surface) :
		#### Suela ####
		# Datos Trapecio
		sx1 = sx4 = (self.px-self.pos_ini_x) - porCiento(self.largo,10)
		sx2 = sx3 = (self.px-self.pos_ini_x) + porCiento(self.largo,50)
		sy2 = (self.py-self.pos_ini_y) - self.ancho//2 
		sy3 = (self.py-self.pos_ini_y) + self.ancho//2
		sy1, sy4 = sy2+porCiento(self.ancho,30), sy3-porCiento(self.ancho,30)
		puntos = ((sx1,sy1),(sx2,sy2),(sx3,sy3),(sx4,sy4))
		if self.i==0:
			print "px py"
			print (4)
			print "puntos poligono:"
			print puntos
			print "\n"

			print "comienzo elipce"
			print (((self.px-self.pos_ini_x),sy2))
			print "\n"
		# Datos Elipse
		s_rect = pygame.Rect(((self.px-self.pos_ini_x), sy2, self.largo, self.ancho))

		pygame.draw.ellipse(self.alpha_surface, self.color, s_rect)
		pygame.draw.polygon(self.alpha_surface, self.color, puntos)
		
		#### Tacon ####
		# Datos Circulo
		radio = (sy4 - sy1 + 2) /  2
		tx = sx1 - porCiento(self.largo,30)
		ty = sy1 + radio
		pos = (techo(tx),techo(ty))
		# Datos Rectangulo
		t_rect = pygame.Rect((tx, sy1, porCiento(radio,105), 2*radio))
		if self.i==0:		
			print "datos circulo"
			print pos
			print int(radio)
			print t_rect
			print "\n"
			print "posiciones iniciales"
			print ((self.pos_ini_x,self.pos_ini_y))
			self.i=1

		pygame.draw.circle(self.alpha_surface, self.color, pos, techo(radio))
		pygame.draw.rect(self.alpha_surface, self.color, t_rect)
		surface.blit(self.alpha_surface,(self.pos_ini_x,self.pos_ini_y))
		# surface.blit(self.alpha_surface,(0,0))

		
	def update_color(self):
		escala = 40
		if self.color.a - escala > 0:
			self.color.a -= escala
			return 0
		else:
			return 1
			


class Personaje(pygame.sprite.Sprite):
	def __init__(self,surface, px=100, py=100, orientation = 0):
		pygame.sprite.Sprite.__init__(self)
		self.position = [px,py]
		self.orientation = orientation
		self.pie_izq = True
		self.velocidad = 30
		self.huellas = []
		self.dif_pie = 8
		self.ventana = surface
		self.espera = 1
		self.seg_pie = [2,False]
		self.tiempo = {"med_sg":500, "sg":1000, "o":400}
		self.quieto = [True														# estoy quieto
									,pygame.time.get_ticks()//self.tiempo["o"]		# el ultimo segundo en el que me movi
									,pygame.time.get_ticks()//self.tiempo["o"]] 	# ultimo seg en que se borro una huella
		h_der = Huella(self.position[0], self.position[1] + self.dif_pie)
		h_izq = Huella(self.position[0], self.position[1] - self.dif_pie)
		for h in [h_izq,h_der]:
			self.huellas += [h]
			h.mostrar(surface)

	def update(self):
		tiempo = pygame.time.get_ticks()//self.tiempo["o"]	
		actualizar = 	self.quieto[0] and (tiempo - self.quieto[2] > ceil(self.espera*1.0/3))
		quitados = 0
		for i in range(len(self.huellas)):
			invisible = 0
			if actualizar:
				if i-quitados < len(self.huellas) - 2:
					invisible = self.huellas[i-quitados].update_color()
					self.quieto[2] = tiempo
			if invisible:
				self.huellas.pop(i-quitados)
				quitados += 1
			else:
				self.huellas[i-quitados].mostrar(self.ventana)

	def move_derecha(self, parado = False):
		if not parado:
			self.position[0] += 43
			self.quieto[1] = pygame.time.get_ticks()//self.tiempo["o"]
			self.quieto[0] = False
			self.seg_pie[1] = False
		else:
			self.seg_pie[1] = True

		self.quieto[2] = pygame.time.get_ticks()//self.tiempo["o"]

		if self.pie_izq :
			dif = -1*self.dif_pie
			self.pie_izq = False
		else:
			dif = self.dif_pie
			self.pie_izq = True

		huella = Huella(self.position[0], self.position[1] + dif)

		longitud = len(self.huellas)
		quitados = 0
		for i in range(longitud):
			if i-quitados != longitud - 1:
				invisible = self.huellas[i-quitados].update_color()
				if invisible:
					self.huellas.pop(i-quitados)
					quitados += 1

		self.huellas += [huella]






pygame.init()

ancho, alto = 1360,730
ventana = pygame.display.set_mode((ancho,alto))
ventana.fill(0xFFFFFF)
pygame.display.set_caption("Prueba")
# p1 = Personaje(ventana,100,100)
h_90 = Huella(200, 200, 90)
#h_0 = Huella(200, 200, 0)
# huella = Huella(100,100)

while True:
	ventana.fill(0xFFFFFF)

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == K_RIGHT:
				# p1.move_derecha()
				pass
	# else:
	# 	if not p1.quieto[0] and (pygame.time.get_ticks()//p1.tiempo["o"] - p1.quieto[1] > p1.espera):
	# 		p1.quieto[0] = True
	# 		pass

	# 	elif not p1.seg_pie[1] and pygame.time.get_ticks()//p1.tiempo["o"] - p1.quieto[1] > p1.seg_pie[0]:
	# 		p1.move_derecha(True)
	# 		pass


	# p1.update()
	h_90.mostrar(ventana)
	#h_0.mostrar(ventana)
	# huella.update_color()
	# huella.mostrar(ventana)
	#print pygame.mouse.get_pos()
	pygame.display.update()



