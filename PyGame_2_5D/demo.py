from pygame2_5d import *
import pygame, sys, math
from pygame.locals import *

def init_scene():
	scene_set_object(pos = pos(0, 6.5), size = pos(0.25, 9), color = GRAY)
	scene_set_object(pos = pos(2, 3.25), size = pos(0.25, 2.5), color = GRAY)
	scene_set_object(pos = pos(4, 3.25), size = pos(0.25, 2.5), color = GRAY)
	scene_set_object(pos = pos(2, 7.75), size = pos(0.25, 2.5), color = GRAY)
	scene_set_object(pos = pos(3, 4.5), size = pos(2, 0.25), color = GRAY)
	scene_set_object(pos = pos(5.25, 6.5), size = pos(6.5, 0.25), color = GRAY)
	scene_set_object(pos = pos(6.5, 11), size = pos(13, 0.25), color = GRAY)
	scene_set_object(pos = pos(5.5, 9), size = pos(7, 0.25), color = GRAY)
	scene_set_object(pos = pos(8.5, 4.25), size = pos(0.25, 4.5), color = GRAY)
	scene_set_object(pos = pos(6.25, 2), size = pos(4.5, 0.25), color = GRAY)
	scene_set_object(pos = pos(6.25, 4.5), size = pos(1.5, 1.5), color = GRAY)
	scene_set_object(pos = pos(9, 6.5), size = pos(0.25, 5), color = GRAY)
	scene_set_object(pos = pos(13, 7.5), size = pos(0.25, 7), color = GRAY)
	scene_set_object(pos = pos(11, 4), size = pos(4, 0.25), color = GRAY)
	scene_set_object(pos = pos(11, 9.5), size = pos(1, 1), color = GRAY)
	scene_set_object(pos = pos(11, 7.5), size = pos(1, 1), color = GRAY)
	scene_set_object(pos = pos(11, 5.5), size = pos(1, 1), color = GRAY)
	player_set_position(pos(1, 1.5))

def main():
	init_scene()
	only_border = input("Border only mode? (y/n)").strip().lower() == "y"
	init_render_settings(width = 1280, height = 720, skycolor = BLACK, only_border = only_border, border_width = 5)
	init(title = "PyGame 2,5D - Dungeon Demo")
	main_loop()

if __name__ == '__main__':
	main()
