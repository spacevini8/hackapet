import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
import time
import pygame
import random

# Initialize display
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()

# Load and apply background
background = displayio.OnDiskBitmap("assets/background.bmp")
bg_tile = displayio.TileGrid(background, pixel_shader=displayio.ColorConverter())
splash.append(bg_tile)

# Load Fox animation
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
    y=128 - frame_height,  # Ensures fox stays in frame
)
splash.append(fox)

# Load the custom font
font = bitmap_font.load_font("assets/Dina_r400-10.bdf")

# Level Display
level_label = label.Label(
    font, text="Level: 1", color=0xFFFFFF, x=5, y=5
)
splash.append(level_label)

# Bytes (Food) Display
bytes_label = label.Label(
    font, text="Bytes: 0/3", color=0xFFFFFF, x=5, y=20
)
splash.append(bytes_label)

# Feedback Message Display
feedback_label = label.Label(
    font, text="", color=0xFFFF00, x=5, y=35
)
splash.append(feedback_label)

# Initial Byte Settings
byte_size = 16
byte_speed = 1
fox_x = 32
fox_speed = 8
byte_y = 0
current_frame = 0
animation_speed = 0.05
feedback_timer = 0
current_level = 1
bytes_collected = 0
bytes_required = 3

# Generate Byte (Food)
def generate_byte():
    global byte_size
    byte = displayio.Bitmap(byte_size, byte_size, 2)
    byte_palette = displayio.Palette(2)
    byte_palette[0] = 0x000000
    byte_palette[1] = 0xFFFF00  # Yellow
    byte_item = displayio.TileGrid(byte, pixel_shader=byte_palette, x=random.randint(0, 128 - byte_size), y=0)

    for x in range(byte_size):
        for y in range(byte_size):
            byte[x, y] = 1

    return byte_item

# First byte
byte_item = generate_byte()
splash.append(byte_item)

display.show(splash)

# Game Loop
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

    # Move Byte
    byte_y += byte_speed
    byte_item.y = int(byte_y)

    # Check Collision with Fox
    if byte_y >= 128 - frame_height and fox_x <= byte_item.x <= fox_x + frame_width:
        bytes_collected += 1
        feedback_label.text = "You caught a byte!"
        feedback_timer = 20

        # Reset byte
        splash.remove(byte_item)
        byte_y = 0
        byte_item = generate_byte()
        splash.append(byte_item)

        # Check Level Up
        if bytes_collected >= bytes_required:
            current_level += 1
            bytes_collected = 0
            bytes_required += 2  # Increase bytes needed for next level

            byte_speed += 1  # Make bytes fall faster
            fox_speed = min(16, fox_speed + 2)  # Increase fox movement speed
            byte_size = max(4, byte_size - 2)  # Make bytes smaller

            splash.remove(byte_item)  # Clear previous bytes
            byte_item = generate_byte()
            splash.append(byte_item)

            feedback_label.text = f"Level {current_level}!"

    elif byte_y > 128:
        feedback_label.text = "You missed a byte!"
        feedback_timer = 20
        splash.remove(byte_item)
        byte_y = 0
        byte_item = generate_byte()
        splash.append(byte_item)

    # Update text
    level_label.text = f"Level: {current_level}"
    bytes_label.text = f"Bytes: {bytes_collected}/{bytes_required}"

    # Remove feedback after time
    if feedback_timer > 0:
        feedback_timer -= 1
    else:
        feedback_label.text = ""

    # Handle Animation
    current_frame = (current_frame + 1) % total_frames
    fox[0] = current_frame

    time.sleep(animation_speed)

pygame.quit()
