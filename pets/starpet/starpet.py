import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import random
import time

pygame.init()
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

space_station_background = displayio.OnDiskBitmap("spacestationbackground_old.bmp")

bg_sprite = displayio.TileGrid(
	space_station_background, 
	pixel_shader=space_station_background.pixel_shader
)

splash.append(bg_sprite)

erebus_sheet = displayio.OnDiskBitmap("erebus_sheet.bmp")

tile_width = 32
tile_height = 32

erebus_sprite = displayio.TileGrid(
	erebus_sheet,
	pixel_shader=erebus_sheet.pixel_shader,
	width=1,
	height=1,
    tile_width=tile_width,
    tile_height=tile_height,
	default_tile=0,
	x=(display.width - tile_width) // 2,
	y=display.height - tile_height - 10
)

splash.append(erebus_sprite)

frame = 0

keys = pygame.key.get_pressed()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
    
    erebus_sprite[0] = frame
    frame = (frame + 1) % (erebus_sheet.width // tile_width)

    pygame.time.wait(100)