import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame, sys
import time
import random

pygame.init()

scale = 1
display_width = 128 * scale
display_height = 128 * scale
display = PyGameDisplay(width=display_width, height=display_height)
splash = displayio.Group(scale=scale)
display.show(splash)

outback_background = displayio.OnDiskBitmap("outback-background.bmp")
bg_sprite = displayio.TileGrid(
	outback_background,
	pixel_shader=outback_background.pixel_shader
)

tile_width = 32
tile_height = 32

splash.append(bg_sprite)

dragon_sheet = displayio.OnDiskBitmap("jax-idle.bmp")

dragon_sprite = displayio.TileGrid(
	dragon_sheet,
	pixel_shader=dragon_sheet.pixel_shader,
	width=1,
	height=1,
	tile_width = tile_width,
	tile_height = tile_height,
	default_tile=0,
	x=(display.width - tile_width) // 2,
	y=display.height - tile_height - 40
)

splash.append(dragon_sprite)


waterdrop_bitmap = displayio.OnDiskBitmap("water