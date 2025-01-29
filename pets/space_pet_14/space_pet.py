import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import random
import time
from adafruit_display_text import label
import random

pygame.init()
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

space_station_background = displayio.OnDiskBitmap("spacestationbackground.bmp")

bg_sprite = displayio.TileGrid(
	space_station_background, 
	pixel_shader=space_station_background.pixel_shader
)

tile_width = 32
tile_height = 32

door_1 = displayio.OnDiskBitmap("door_1.bmp")

door_1_sprite = displayio.TileGrid(
	door_1, 
	pixel_shader=space_station_background.pixel_shader
)

door_2 = displayio.OnDiskBitmap("door_2.bmp")

door_2_sprite = displayio.TileGrid(
	door_2, 
	pixel_shader=space_station_background.pixel_shader
)

splash.append(bg_sprite)
splash.append(door_1_sprite)
splash.append(door_2_sprite)

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
	x=(display.width - tile_width) // 3,
	y=display.height - tile_height - 1
)

splash.append(erebus_sprite)

frame = 0
speed = 32

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == pygame.K_LEFT:
                erebus_sprite.x -= speed
            elif event.key == pygame.K_RIGHT:
                erebus_sprite.x += speed
            elif event.key == pygame.K_UP:
                erebus_sprite.y -= speed
    
    if erebus_sprite.x < 0:
        erebus_sprite.x = 0
    elif erebus_sprite.x > display.width - tile_width:
        erebus_sprite.x = display.width - tile_width

    erebus_sprite.x = erebus_sprite.x
    
    if erebus_sprite.y < 0:
        erebus_sprite.y = display.height - tile_height
    
    erebus_sprite[0] = frame
    frame = (frame + 1) % (erebus_sheet.width // tile_width)

    pygame.time.wait(100)