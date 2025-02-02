import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
import pygame
import time
import random

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

FONT = bitmap_font.load_font("./bitbuntu-full.bdf")

DRAGON_WIDTH = 32
DRAGON_HEIGHT = 32

START_WIDTH = START_HEIGHT = 128

PET_SPEED = DRAGON_HEIGHT
FIREBALL_BASE_SPEED = 4
GRAVITY = 4

frame = 0
start_frame = 0
game_over = False
has_started = False
score = 0
fireball_speed = FIREBALL_BASE_SPEED

sky_background = displayio.OnDiskBitmap("sky-background.bmp")
bg = displayio.TileGrid(
    sky_background, 
    pixel_shader=sky_background.pixel_shader
)
splash.append(bg)

score_label = label.Label(FONT, text='Score: 0', color=0x000000, x=display.width//2-25, y=10)
splash.append(score_label)

dragon_sheet = displayio.OnDiskBitmap("dragon-sheet.bmp")
dragon = displayio.TileGrid(
    dragon_sheet,
    pixel_shader=dragon_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=DRAGON_WIDTH,
    tile_height=DRAGON_HEIGHT,
    default_tile=0,
    x=(display.width - dragon_sheet.width) // 2,  
    y=display.height - dragon_sheet.height
)
splash.append(dragon)

birdplane_bitmap = displayio.OnDiskBitmap("birdplane.bmp")
birdplane = displayio.TileGrid(
    birdplane_bitmap,
    pixel_shader=birdplane_bitmap.pixel_shader,
    width=1,
    height=1,
    tile_width=birdplane_bitmap.width,
    tile_height=birdplane_bitmap.height,
)
splash.append(birdplane)

missile_bitmap = displayio.OnDiskBitmap("missile.bmp")
missile = displayio.TileGrid(
    missile_bitmap,
    pixel_shader=missile_bitmap.pixel_shader,
    width=1,
    height=1,
    tile_width=missile_bitmap.width,
    tile_height=missile_bitmap.height,
)
splash.append(missile)

restart_bitmap = displayio.OnDiskBitmap("restart.bmp")
restart = displayio.TileGrid(
    restart_bitmap,
    pixel_shader=restart_bitmap.pixel_shader,
    width=1,
    height=1,
    tile_width=64,
    tile_height=32,
    default_tile=0,
    x=(display.width - 64) // 2,  
    y=(display.height - 32) // 2  
)

start_sheet = displayio.OnDiskBitmap("start-sheet.bmp")
start = displayio.TileGrid(
    start_sheet, 
    pixel_shader=start_sheet.pixel_shader,
    tile_width=START_WIDTH,
    tile_height=START_HEIGHT,
    default_tile=0
)
splash.append(start)

def spawn_birdplane():
    birdplane.x = display.width
    birdplane.y = random.randint(0, (display.height // birdplane_bitmap.height) - 1) * birdplane_bitmap.height

def spawn_missile():
    missile.x = display.width
    missile.y = random.randint(0, (display.height // missile_bitmap.height) - 1) * missile_bitmap.height

fireball_bitmap = displayio.OnDiskBitmap("fireball.bmp")
fireball = displayio.TileGrid(
        fireball_bitmap,
        pixel_shader=fireball_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=fireball_bitmap.width,
        tile_height=fireball_bitmap.height,
        y=-32
    )
splash.append(fireball)

def spawn_fireball():
    fireball.x=dragon.x
    fireball.y=dragon.y

def despawn_fireball():
    fireball.y=-32
    
def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + sprite2.tile_width and
        sprite1.x + sprite1.tile_width > sprite2.x and
        sprite1.y < sprite2.y + sprite2.tile_height and
        sprite1.y + sprite1.tile_height > sprite2.y
    )

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and game_over == True:
                spawn_birdplane()
                spawn_missile()
                score = 0
                score_label.text = f'Score: {score}'
                splash.remove(restart)
                game_over = False
                dragon.y = display.height - DRAGON_HEIGHT
            if event.key == pygame.K_SPACE and has_started == False:
                has_started = True
                splash.remove(start)
                
    if not has_started:
        start[0] = start_frame
        start_frame = (start_frame + 1) % (start_sheet.width // START_WIDTH)
        continue

    if game_over: continue

    birdplane_speed = random.randrange(3,6)
    missile_speed = random.randrange(3,6)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        dragon.y = dragon.y - PET_SPEED if dragon.y - PET_SPEED > 0 else 0
    if keys[pygame.K_RIGHT]:
        spawn_fireball()
        fireball_speed = FIREBALL_BASE_SPEED

    birdplane.x -= birdplane_speed
    missile.x -= missile_speed
    fireball.x += fireball_speed
    dragon.y += GRAVITY if dragon.y < display.height else 0

    if birdplane.x <= -birdplane_bitmap.width:
        spawn_birdplane()
    elif check_collision(birdplane, fireball):
        spawn_birdplane()
        despawn_fireball()
        fireball_speed = 0
        score += 1
        score_label.text = f'Score: {score}'

    if missile.x <= -missile_bitmap.width:
        spawn_missile()

    if (check_collision(missile, dragon) or 
          check_collision(missile, dragon) or 
          check_collision(missile, fireball)):
        game_over = True
        splash.append(restart)

    dragon[0] = frame
    frame = (frame + 1) % (dragon_sheet.width // DRAGON_WIDTH)

    time.sleep(0.1)