import pygame, sys
from pygame.locals import *
from math import *

def rotar_puntos(angulo, pu, pv):
	angulos = {90:pi,
					 30:pi/3,
					 45:pi/2,
					 0:0,
					 360:4*pi,
					 180:2*pi}

	alfa = angulos[angulo]
	px = cos(alfa)*pu - sin(alfa)*pv
	py = sin(alfa)*pu + cos(alfa)*pv
	return (px,py)

def techo (f):
	return int(ceil(f))

def xz(x,z):
	return{'x':x,'z':z}


class Huella(pygame.sprite.Sprite):

	def __init__(self, px, pz,huella, orientation = 0, alpha = 255):
		pygame.sprite.Sprite.__init__(self)
		# Tamano de la huella
		self.largo = 40 
		self.ancho = 20
		self.alpha = alpha		
		self.img = pygame.image.load(huella)
		self.orientation = orientation
		self.position = xz(px,pz) # Esquina superior derecha

	def mostrar(self, surface) :
		x , z = self.position['x'], self.position['z']
		temp = pygame.Surface((self.img.get_width(), self.img.get_height())).convert()
		temp_surface = pygame.transform.rotate(surface,self.orientation)
		temp.blit(surface, (-x, -z))
		temp.blit(self.img, (0, 0))
		temp.set_alpha(self.alpha)
		temp = pygame.transform.rotate(temp,self.orientation)        
		surface.blit(temp, (x,z))
		
	def update_color(self):
		escala = 40
		if self.alpha - escala > 0:
			self.alpha -= escala
			return 0
		else:
			return 1
			


class Personaje(pygame.sprite.Sprite):
	def __init__(self,surface,huella, px=100, py=100, orientation = 0):
		pygame.sprite.Sprite.__init__(self)
		self.position = [px,py]
		self.orientation = orientation
		self.pie_izq = True
		self.velocidad = 30
		self.img_huella = huella
		self.huellas = []
		self.dif_pie = 8
		self.ventana = surface
		self.espera = 5
		self.seg_pie = [2,True]
		self.tiempo = {"med_sg":500, "sg":1000, "o":400}
		self.quieto = [True														# estoy quieto
									,pygame.time.get_ticks()//self.tiempo["o"]		# el ultimo segundo en el que me movi
									,pygame.time.get_ticks()//self.tiempo["o"]] 	# ultimo seg en que se borro una huella

		h_der = Huella(self.position[0], self.position[1] + self.dif_pie,self.img_huella,30)
		h_izq = Huella(self.position[0], self.position[1] - self.dif_pie,self.img_huella,self.orientation)
		for h in [h_izq,h_der]:
			self.huellas += [h]

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
			## Si no estoy parado, aumento la posicion, actualizo los tiempos
			## que indican que me movi
			self.position[0] += 43
			self.quieto[1] = pygame.time.get_ticks()//self.tiempo["o"]
			self.quieto[0] = False
			self.seg_pie[1] = False
		else:
			## Si me tengo que quedar parado, coloco el segundo pie
			self.seg_pie[1] = True

		## Actualizo el tiempo de me quede quieto o camine
		self.quieto[2] = pygame.time.get_ticks()//self.tiempo["o"]

		## Cambio de pie e identifico la x en la diferencia que 
		## va a haber entre los dos pies (separacion)
		if self.pie_izq :
			dif = -1*self.dif_pie
			self.pie_izq = False
		else:
			dif = self.dif_pie
			self.pie_izq = True

		## Creo la huella y actualizo el arreglo de huellas
		huella = Huella(self.position[0], self.position[1] + dif, self.img_huella)
		longitud = len(self.huellas)
		quitados = 0 # Utilizada para poder iterar mientras se eliminan huellas
		for i in range(longitud):
			# Debemos mantener las ultimas dos huellas a full color
			# porque es donde esta parado el personaje
			if i-quitados != longitud - 1:
				invisible = self.huellas[i-quitados].update_color()
				if invisible:
					# Si esta invisible la eliminamos
					self.huellas.pop(i-quitados)
					quitados += 1

		self.huellas += [huella]






pygame.init()

ancho, alto = 1360,730
mapa = pygame.image.load('mapa.jpg')

ventana = pygame.display.set_mode((ancho,alto))
ventana.blit(mapa,(0,0))
pygame.display.set_caption("Prueba")

p1 = Personaje(ventana,"pie_2.png",100,100)
p2 = Personaje(ventana, "pie_2.png",100,300,90)

while True:
	ventana.blit(mapa,(0,0))

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == K_RIGHT:
				p1.move_derecha()
	else:
		if not p1.quieto[0] and (pygame.time.get_ticks()//p1.tiempo["o"] - p1.quieto[1] > p1.espera):
			p1.quieto[0] = True

		elif not p1.seg_pie[1] and pygame.time.get_ticks()//p1.tiempo["o"] - p1.quieto[1] > p1.seg_pie[0]:
			p1.move_derecha(True)


	p1.update()
	p2.update()
	#print pygame.mouse.get_pos()
	pygame.display.update()



