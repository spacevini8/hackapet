import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
from adafruit_display_text import label
import terminalio
import time
import pygame
import random

display = PyGameDisplay(width=128, height=128)

splash = displayio.Group()

background = displayio.OnDiskBitmap("assets/background.bmp")
bg_tile = displayio.TileGrid(background, pixel_shader=displayio.ColorConverter())
splash.append(bg_tile)

fox_sprites = displayio.OnDiskBitmap("assets/glitch_fox_idle.bmp")
frame_width = 64
frame_height = 64
total_frames = 32
fox = displayio.TileGrid(
    fox_sprites,
    pixel_shader=displayio.ColorConverter(),
    width=1, height=1,
    tile_width=frame_width,
    tile_height=frame_height,
    x=32,
    y=128 - frame_height,
)
splash.append(fox)

level_label = label.Label(
    terminalio.FONT, text="Level: 1", color=0xFFFFFF, x=5, y=5
)
splash.append(level_label)

bytes_label = label.Label(
    terminalio.FONT, text="Bytes: 0/3", color=0xFFFFFF, x=5, y=20
)
splash.append(bytes_label)

feedback_label = label.Label(
    terminalio.FONT, text="", color=0xFFFF00, x=5, y=35
)
splash.append(feedback_label)

byte_size = 8
byte = displayio.Bitmap(byte_size, byte_size, 2)
byte_palette = displayio.Palette(2)
byte_palette[0] = 0x000000
byte_palette[1] = 0xFFFF00
byte_item = displayio.TileGrid(byte, pixel_shader=byte_palette, x=random.randint(0, 128 - byte_size), y=0)
splash.append(byte_item)

for x in range(byte_size):
    for y in range(byte_size):
        byte[x, y] = 1

display.show(splash)

fox_x = 32
fox_speed = 8
byte_y = 0
byte_speed = 1
current_frame = 0
animation_speed = 0.05
feedback_timer = 0
current_level = 1
bytes_collected = 0
bytes_required = 3

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                fox_x = max(0, fox_x - fox_speed)
            elif event.key == pygame.K_RIGHT:
                fox_x = min(128 - frame_width, fox_x + fox_speed)

    fox.x = fox_x

    byte_y += byte_speed
    byte_item.y = int(byte_y)

    if byte_y >= 128 - frame_height and fox_x <= byte_item.x <= fox_x + frame_width:
        bytes_collected += 1
        feedback_label.text = "You caught a byte!"
        feedback_timer = 20
        byte_y = 0
        byte_item.x = random.randint(0, 128 - byte_size)

        if bytes_collected >= bytes_required:
            current_level += 1
            bytes_collected = 0
            bytes_required += 2
            byte_speed += 1
            fox_speed = min(16, fox_speed + 2)
            byte_size = max(4, byte_size - 2)

            splash.remove(byte_item)

            byte = displayio.Bitmap(byte_size, byte_size, 2)
            for x in range(byte_size):
                for y in range(byte_size):
                    byte[x, y] = 1
            byte_item = displayio.TileGrid(byte, pixel_shader=byte_palette, x=random.randint(0, 128 - byte_size), y=0)
            splash.append(byte_item)

            feedback_label.text = f"Level {current_level}!"

    elif byte_y > 128:
        feedback_label.text = "You missed a byte!"
        feedback_timer = 20
        byte_y = 0
        byte_item.x = random.randint(0, 128 - byte_size)

    level_label.text = f"Level: {current_level}"
    bytes_label.text = f"Bytes: {bytes_collected}/{bytes_required}"

    if feedback_timer > 0:
        feedback_timer -= 1
    else:
        feedback_label.text = ""

    current_frame = (current_frame + 1) % total_frames
    fox[0] = current_frame

    time.sleep(animation_speed)

pygame.quit()
