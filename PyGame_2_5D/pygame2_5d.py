import pygame, sys, math
from pygame.locals import *

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARKGRAY = (64, 64, 64)
BLUE = (0, 0, 255)
NAVY = (0, 0, 128)
DARKBLUE = NAVY
SKYBLUE = (135,206,235)
GREEN = (0, 255, 0)
DARKGREEN = (0, 128, 0)
RED = (255, 0, 0)
DARKRED = (128,0,0)
YELLOW = (255, 255, 0)
SILVER = (192, 192, 192)
BROWN = (139,69,19)

FACTOR = 500
initialized = 0

POS = 'pos'
SIZE = 'size'
COLOR = 'color'
INTENSITY = 'intensity'

YAW = 90 # Rotationsschritte
STEP = 75 # Bewegungsschritte

def xz (x, z):
	return {'x': x, 'z': z}

def pos (x, z):
	return xz(x * FACTOR, z * FACTOR)

player_pos = xz(0, 0) # Spielerposition
camera_yaw = 0 # Nach Z
scene = []
scene_lights = []

# Als erstes vor init() aufzurufen
def init_render_settings(fps = 20, width = 640, height = 480, depth = 10000, skycolor = SKYBLUE, light = False, ambient = 0.1, wall_height = None, border = False, only_border = False, border_width = 1):
	global FPS, WINDOWWIDTH, WINDOWHEIGHT, WINDOWMIDDLE, WALL_HEIGHT, RENDER_DEPTH, BG, LIGHT, AMBIENT, BORDER, ONLY_BORDER, BORDER_WIDTH, initialized
	assert initialized == 0, "Don't call init_render_settings() twice"
	FPS = fps
	WINDOWWIDTH = width
	WINDOWHEIGHT = height
	WINDOWMIDDLE = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
	WALL_HEIGHT = WINDOWHEIGHT if wall_height == None else wall_height
	RENDER_DEPTH = depth # Sichtdistanz
	BG = skycolor
	LIGHT = light
	AMBIENT = ambient
	BORDER = border
	ONLY_BORDER = only_border
	BORDER_WIDTH = border_width
	assert not(BORDER and ONLY_BORDER), "Only once of the options (border and border only) can be active!"
	initialized = 1

# Direkt nach init_render_settings() aufzurufen
def init(title = "PyGame 2,5D"):
	global FPSCLOCK, DISPLAYSURF, BASICFONT, initialized
	assert initialized == 1, "Please call init_render_settings() before call init() and don't call init() twice"
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
	pygame.display.set_caption(title)
	initialized = 2

def fps_tick ():
	FPSCLOCK.tick(FPS)

# Der Spieler kann hiermit bewegt werden...
def player_move(x, z, collision_detection = False):
	global player_pos
	pos = rotate_movement(xz(x, z))
	new_player_pos = xz(player_pos['x'] + pos['x'], player_pos['z'] + pos['z'])
	# Wenn collision_detection aktiviert ist und der Weg frei ist, oder eben keine collision_detection aktiviert ist dann:
	if (collision_detection and not(scene_is_object(new_player_pos))) or not(collision_detection):
		player_pos = new_player_pos

# Hiermit kann der Spieler auf eine Position gesetzt werden...
def player_set_position (xz):
	global player_pos
	player_pos = xz

def player_yaw_check ():
	global camera_yaw
	assert camera_yaw % 90 == 0, "Yaw must be a multiply of 90"
	if camera_yaw >= 360:
		camera_yaw -= 360
	elif camera_yaw < 0:
		camera_yaw = 360 - camera_yaw * -1

# Setzt die Rotation
def player_yaw_set (alpha):
	global camera_yaw
	camera_yaw = alpha
	player_yaw_check()

# Addiert zur Rotation
def player_yaw_move (alpha):
	global camera_yaw
	camera_yaw += alpha
	player_yaw_check()

# Zeichnet die Scene, in die der Spieler blickt.
def draw():
	DISPLAYSURF.fill(BG)
	renderscene = scene_get_renderscene()
	for obj in renderscene:
		draw_object(obj)
	pygame.display.update()

def quit():
	pygame.quit()
	sys.exit()

# Setzt ein Objekt in die Welt
def scene_set_object(pos = xz(0, 0), size = xz(50, 50), color = WHITE, scene = scene):
	scene.append({POS: pos, SIZE: size, COLOR: color})

# Gibt die Scene zurück
def scene_get ():
	return scene

# Setzt ein Licht in die Welt
def scene_set_light(pos = xz(0, 0), intensity = 100):
	scene_lights.append({POS: pos, INTENSITY: intensity})

# Gibt die Scene zurück
def scene_light_get ():
	return scene_lights

# Berechnet, ob die Position pos ein Objekt ist. (Kollision)
def scene_is_object (pos):
	for obj in scene:
		HALF_X = obj[SIZE]['x'] / 2
		MIN_X = obj[POS]['x'] - HALF_X
		MAX_X = obj[POS]['x'] + HALF_X
		HALF_Z = obj[SIZE]['z'] / 2
		MIN_Z = obj[POS]['z'] - HALF_Z
		MAX_Z = obj[POS]['z'] + HALF_Z
		if pos['x'] >= MIN_X and pos['x'] <= MAX_X and pos['z'] >= MIN_Z and pos['z'] <= MAX_Z:
			return True
	return False

def transform(pos):
	res = xz(pos['x'] - player_pos['x'], pos['z'] - player_pos['z']) # Zum Nullpunkt (Spieler)
	return rotate(res)

def rotate(pos):
	if camera_yaw == 0:
		return pos
	if camera_yaw == 90:
		return xz(pos['z'] * -1, pos['x'])
	if camera_yaw == 180:
		return xz(pos['x'] * -1, pos['z'] * -1)
	if camera_yaw == 270:
		return xz(pos['z'], pos['x'] * -1)

def rotate_size (pos):
	if camera_yaw == 0 or camera_yaw == 180:
		return pos
	if camera_yaw == 90 or camera_yaw == 270:
		return xz(pos['z'], pos['x'])

def rotate_movement(pos):
	if camera_yaw == 0:
		return pos
	if camera_yaw == 90:
		return xz(pos['z'], pos['x'] * -1)
	if camera_yaw == 180:
		return xz(pos['x'] * -1, pos['z'] * -1)
	if camera_yaw == 270:
		return xz(pos['z'] * -1, pos['x'])

# Wie viel Licht scheint den nun auf das Objekt?
def scene_object_get_light (pos):
	light = AMBIENT
	for l in scene_lights:
		dist_x = abs(l[POS]['x'] - pos['x'])
		dist_z = abs(l[POS]['z'] - pos['z'])
		dist = math.sqrt(math.pow(dist_x, 2) + math.pow(dist_z, 2)) # Pythagoras
		if dist < l[INTENSITY]: # Ist im Licht
			percent = (l[INTENSITY] - dist) / l[INTENSITY]
			light += percent
	return light

def scene_sort_key (obj):
	res = obj[POS]['z'] - obj[SIZE]['z'] / 2
	if res < 0: # Wand!
		return obj[POS]['z'] + obj[SIZE]['z'] / 2
	return res

def scene_get_renderscene ():
	renderscene = []
	for o in scene:
		color = o[COLOR]
		if LIGHT:
			percent = scene_object_get_light(o[POS])
			color = (color[0] * percent, color[1] * percent, color[2] * percent)
		pos = transform(o[POS]) # Position verschieben und rotieren
		size = rotate_size(o[SIZE]) # Größe ebenfalls rotieren
		Z = pos['z'] - size['z'] / 2 # Wirkliche Position Z
		Z_THRESHOLD = pos['z'] + size['z'] / 2 # Wirkliche Position Z

		color = (255 if color[0] > 255 else color[0], \
			255 if color[1] > 255 else color[1], \
			255 if color[2] > 255 else color[2])

		# Wenn die Position nicht hinter dem Spieler ist und die Sichtweite nicht überboten ist...
		if Z_THRESHOLD > 0 and Z < RENDER_DEPTH:
			scene_set_object(pos, size, color, scene=renderscene)

	# Position Z minus die halbe Größe von Z!
	renderscene.sort(key=scene_sort_key) # Sortiere die Liste der z Achse nach. 0 - Render depth
	renderscene.reverse() # Render depth - 0
	return renderscene

def draw_object (obj):
	# Größe des Objekts in der Tiefe:
	HALF_Z = obj[SIZE]['z'] / 2

	# Tiefe des Objekts:
	Z_FRONT = obj[POS]['z'] - HALF_Z
	if Z_FRONT <= 0: # Auch ein Problem, das dadurch behoben wird:
		Z_FRONT = 1
	Z_BACK = obj[POS]['z'] + HALF_Z

	# Tiefe durch FACTOR geteilt
	Z_FACTOR_FRONT = Z_FRONT / FACTOR
	Z_FACTOR_BACK = Z_BACK / FACTOR

	# Die Größe des Objekts im zweidimensionalen.
	SIZE_X_FRONT = obj[SIZE]['x'] / Z_FACTOR_FRONT
	HALF_SIZE_X_FRONT = SIZE_X_FRONT / 2
	SIZE_X_BACK = obj[SIZE]['x'] / Z_FACTOR_BACK
	HALF_SIZE_X_BACK = SIZE_X_BACK / 2

	# Die mittlere Position X auf dem Bildschirm
	MIDDLE_X_FRONT = obj[POS]['x'] / Z_FACTOR_FRONT + WINDOWMIDDLE[0]
	MIDDLE_X_BACK = obj[POS]['x'] / Z_FACTOR_BACK + WINDOWMIDDLE[0]

	# Die Größe des Objekts im zweidimensionalen.
	SIZE_Y_FRONT = WALL_HEIGHT / Z_FACTOR_FRONT
	SIZE_Y_BACK = WALL_HEIGHT / Z_FACTOR_BACK

	# D     C
	#   # #
	#   # #
	# A     B
	# Die Eckpunkte im zweidimensionalen... -> Vorne und Hinten
	X_D_FRONT = int(MIDDLE_X_FRONT - HALF_SIZE_X_FRONT)
	Y_D_FRONT = int(WINDOWMIDDLE[1] - SIZE_Y_FRONT / 2)
	X_D_BACK = int(MIDDLE_X_BACK - HALF_SIZE_X_BACK)
	Y_D_BACK = int(WINDOWMIDDLE[1] - SIZE_Y_BACK / 2)
	D_FRONT = (X_D_FRONT, Y_D_FRONT)
	D_BACK = (X_D_BACK, Y_D_BACK)
	D_FRONT = minimize_position(D_FRONT, D_BACK)

	X_C_FRONT = int(MIDDLE_X_FRONT + HALF_SIZE_X_FRONT)
	Y_C_FRONT = int(WINDOWMIDDLE[1] - SIZE_Y_FRONT / 2)
	X_C_BACK = int(MIDDLE_X_BACK + HALF_SIZE_X_BACK)
	Y_C_BACK = int(WINDOWMIDDLE[1] - SIZE_Y_BACK / 2)
	C_FRONT = (X_C_FRONT, Y_C_FRONT)
	C_BACK = (X_C_BACK, Y_C_BACK)
	C_FRONT = minimize_position(C_FRONT, C_BACK)

	X_B_FRONT = int(MIDDLE_X_FRONT + HALF_SIZE_X_FRONT)
	Y_B_FRONT = int(WINDOWMIDDLE[1] + SIZE_Y_FRONT / 2)
	X_B_BACK = int(MIDDLE_X_BACK + HALF_SIZE_X_BACK)
	Y_B_BACK = int(WINDOWMIDDLE[1] + SIZE_Y_BACK / 2)
	B_FRONT = (X_B_FRONT, Y_B_FRONT)
	B_BACK = (X_B_BACK, Y_B_BACK)
	B_FRONT = minimize_position(B_FRONT, B_BACK)

	X_A_FRONT = int(MIDDLE_X_FRONT - HALF_SIZE_X_FRONT)
	Y_A_FRONT = int(WINDOWMIDDLE[1] + SIZE_Y_FRONT / 2)
	X_A_BACK = int(MIDDLE_X_BACK - HALF_SIZE_X_BACK)
	Y_A_BACK = int(WINDOWMIDDLE[1] + SIZE_Y_BACK / 2)
	A_FRONT = (X_A_FRONT, Y_A_FRONT)
	A_BACK = (X_A_BACK, Y_A_BACK)
	A_FRONT = minimize_position(A_FRONT, A_BACK)

	# Wenn ONLY_BORDER aktviert ist dann...:
	if ONLY_BORDER:
		pygame.draw.lines(DISPLAYSURF, obj[COLOR], True, (A_FRONT, B_FRONT, C_FRONT, D_FRONT), BORDER_WIDTH)
		if D_BACK[0] < D_FRONT[0]: # Perspektive von rechts
			pygame.draw.lines(DISPLAYSURF, obj[COLOR], True, (A_FRONT, A_BACK, D_BACK, D_FRONT), BORDER_WIDTH)
		elif C_BACK[0] > C_FRONT[0]: # Perspektive von links
			pygame.draw.lines(DISPLAYSURF, obj[COLOR], True, (C_FRONT, C_BACK, B_BACK, B_FRONT), BORDER_WIDTH)
		return

	# Die Front:
	pygame.draw.rect(DISPLAYSURF, obj[COLOR], (X_D_FRONT, Y_D_FRONT, SIZE_X_FRONT, SIZE_Y_FRONT)) # Frontseite

	# Die Seiten:
	pygame.draw.polygon(DISPLAYSURF, obj[COLOR], (C_FRONT, C_BACK, B_BACK, B_FRONT)) # Rechts
	pygame.draw.polygon(DISPLAYSURF, obj[COLOR], (A_FRONT, A_BACK, D_BACK, D_FRONT)) # Links

	# Die Randlinien:
	if BORDER:
		pygame.draw.lines(DISPLAYSURF, BLACK, True, (A_FRONT, B_FRONT, C_FRONT, D_FRONT), BORDER_WIDTH)

# Manchmal ist es notwendig die Koordinaten zu verkleinern
def minimize_position (front, back):
	if front[0] < WINDOWWIDTH and front[1] < WINDOWHEIGHT and front[0] >= 0 and front[1] >= 0:
		return front
	if front[0] == 0: # Umgehe das "ZeroDivisionError: division by zero" Problem
		return front
	percent = abs(WINDOWWIDTH / front[0]) # z.B. 1280 / 234567
	if percent > 1:
		return front
	res_front = [front[0] - back[0], front[1] - back[1]] # Setze die Position auf den hinteren Punkt...
	# Verkleinere die Koordinate -> !!Bleibe aber auf der Linie!!
	res_front[0] *= percent
	res_front[1] *= percent
	# Gehe wieder zurück zum normalen Koordinatensystem
	res_front[0] += back[0]
	res_front[1] += back[1]
	return (res_front[0], res_front[1])
	

def default_update():
	global x_speed, z_speed
	if not('x_speed' in globals()):
		x_speed = 0
		z_speed = 0
	for event in pygame.event.get():
		if event.type == QUIT:
			quit()
		elif event.type == KEYDOWN:
			if event.key == K_LEFT:
				player_yaw_move(-YAW)
			elif event.key == K_RIGHT:
				player_yaw_move(YAW)
			elif event.key == K_w:
				z_speed += STEP
			elif event.key == K_s:
				z_speed -= STEP
			elif event.key == K_a:
				x_speed -= STEP
			elif event.key == K_d:
				x_speed += STEP
			elif event.key == K_ESCAPE:
				quit()
	player_move(x_speed, z_speed, True)
	x_speed /= 1.5
	z_speed /= 1.5

def default_update_old():
	for event in pygame.event.get():
		if event.type == QUIT:
			quit()
		elif event.type == KEYDOWN:
			if event.key == K_LEFT:
				player_yaw_move(-YAW)
			elif event.key == K_RIGHT:
				player_yaw_move(YAW)
			elif event.key == K_w:
				player_move(0, STEP, True)
			elif event.key == K_s:
				player_move(0, -STEP, True)
			elif event.key == K_a:
				player_move(-STEP, 0, True)
			elif event.key == K_d:
				player_move(STEP, 0, True)
			elif event.key == K_ESCAPE:
				quit()

def main_loop (update = default_update):
	while True:
		update()
		draw()
		fps_tick()
