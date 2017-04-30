# import pygame, sys
# from pygame.locals import *
# from math import *

# pygame.init()

# ancho, alto = 1360,730
# ventana = pygame.display.set_mode((ancho,alto))
# ventana.fill(0xFF3c1F)
# pygame.display.set_caption("Prueba")
# superficie = pygame.Surface((40,20), pygame.SRCALPHA, 32)
# superficie.fill(0xFFFFFF)
# pie = pygame.image.load("pie.png")
# superficie.blit(pie,(0,0))

# r_90 = pygame.transform.rotate(superficie,90)
# r_30 = pygame.transform.rotate(superficie,30)
# r_0 = pygame.transform.rotate(superficie,0)
# r_180 = pygame.transform.rotate(superficie,180)
# r_270 = pygame.transform.rotate(superficie,270)
# r_45 = pygame.transform.rotate(superficie,45)

# def update(superficie):
# 	escala = 40
# 	alfa = superficie.get_alpha()
# 	print alfa
# 	if alfa - escala > 0:
# 		superficie.set_alpha(alfa - escala)

# while True:
# 	ventana.fill(0xFFFFFF)

# 	for event in pygame.event.get():
# 		if event.type == QUIT:
# 			pygame.quit()
# 			sys.exit()
# 		elif event.type == pygame.KEYDOWN:
# 			if event.key == K_RIGHT:
# 				update(r_45)

# 	# ventana.blit(r_90,(0,0))
# 	# ventana.blit(r_30,(0,0))
# 	# ventana.blit(r_0,(0,0))
# 	# ventana.blit(r_180,(0,0))
# 	# ventana.blit(r_270,(0,0))
# 	ventana.blit(r_45,(0,0))



# 	pygame.display.update()
import pygame
import time

def blit_alpha(target, source, location, opacity):
	x = location[0]
	y = location[1]
	temp = pygame.Surface((source.get_width(), source.get_height())).convert()
	temp.blit(target, (-x, -y))
	temp.blit(source, (0, 0))
	temp.set_alpha(opacity)        
	target.blit(temp, location)


pygame.init()
screen = pygame.display.set_mode((300, 300))
done = False

happy = pygame.image.load('pie_2.png') # our happy blue protagonist
checkers = pygame.image.load('DSCN4596.JPG') # 32x32 repeating checkered image
i = 255
while not done:
	start = time.time()
	# pump those events!
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			done = True
	# checker the background
	screen.fill(0xFF0000)
	# here comes the protagonist
	if i <= 0:
		i = 255
	blit_alpha(screen, happy, (100, 100), i)
	i -=10

	pygame.display.flip()

	# yeah, I know there's a pygame clock method
	# I just like the standard threading sleep
	end = time.time()
	diff = end - start
	framerate = 30
	delay = 1.0 / framerate - diff
	if delay > 0:
		time.sleep(delay)