import random
import time

import displayio
import pygame
from blinka_displayio_pygamedisplay import PyGameDisplay
import math

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)
background_bitmap = displayio.OnDiskBitmap("./assets/Background.bmp")
bg_sprite = displayio.TileGrid(background_bitmap, pixel_shader=background_bitmap.pixel_shader)
splash.append(bg_sprite)

tile_bitmap = displayio.OnDiskBitmap("./assets/Dance Tiles.bmp")
tile_sprite = displayio.TileGrid(tile_bitmap, pixel_shader=tile_bitmap.pixel_shader)
tile_sprite.y = 25
splash.append(tile_sprite)

fire_bitmap = displayio.OnDiskBitmap("./assets/Fire.bmp")



try_again_bitmap = displayio.OnDiskBitmap("./assets/Try Again.bmp")
try_again_sprite = displayio.TileGrid(try_again_bitmap, pixel_shader=try_again_bitmap.pixel_shader)
try_again_sprite.y = 25

duck_sheet = displayio.OnDiskBitmap("./assets/Duck Sprites.bmp")

tile_width = 128
tile_height = 128
duck_frame = 0
duck_sprite = displayio.TileGrid(
    duck_sheet,
    pixel_shader=duck_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=0,
    y=25
)

splash.append(duck_sprite)

tile_width = 32
tile_height = 32

arrows = []

game_over = False
score = 0


class Arrow:
    bitmap = displayio.OnDiskBitmap("./assets/Arrow.bmp")
    def __init__(self):

        self.sprite = displayio.TileGrid(
            Arrow.bitmap,
            pixel_shader=Arrow.bitmap.pixel_shader
        )
        self.sprite.y = 26
        splash.append(self.sprite)
        self.frame = 0
        self.orientation = random.randint(1, 3)
        # 1 is left, 2 is top, 3 is right
        if self.orientation ==1:
            self.sprite.x = -64
        elif self.orientation == 2:
            self.sprite.transpose_xy = True
            self.sprite.y = -64
        elif self.orientation == 3:
            self.sprite.flip_x = True
            self.sprite.x = 64

    def move(self):
        speed = 3
        if self.orientation ==1:
            self.sprite.x+=speed
        elif self.orientation ==2:
            self.sprite.y+=speed
        elif self.orientation ==3:
            self.sprite.x-=speed
arrows = []

def changeSprite(duck_frame, new_frame):
    duck_sprite[0] = duck_frame
    return (new_frame)%(duck_sheet.width//tile_width)

def spawn_arrows():
    if random.random() < 0.075:  # spawn rate
        arrows.append(Arrow())


def arrow_collision(arrow_sprite):
    x_offset = 8
    y_offset = 16
    return (
        duck_sprite.x < arrow_sprite.x + x_offset and
        duck_sprite.x + x_offset > arrow_sprite.x and
        duck_sprite.y < arrow_sprite.y + y_offset and
        duck_sprite.y + y_offset > arrow_sprite.y
)

def arrow_dance(arrow_sprite):
    x_offset = 40
    y_offset = 40
    return (
        tile_sprite.x < arrow_sprite.x + x_offset and
        tile_sprite.x + x_offset > arrow_sprite.x and
        tile_sprite.y < arrow_sprite.y + y_offset and
        tile_sprite.y + y_offset > arrow_sprite.y)
        #return (arrow_sprite.x + x_offset-tile_sprite.x, arrow_sprite.y + y_offset-tile_sprite.y)

def display_game_over():
    for f in fires:
        splash.remove(f)
    fires.clear()
    for a in arrows:
        splash.remove(a.sprite)
    arrows.clear()

def remove_arrow(a):
    splash.remove(a.sprite)
    arrows.remove(a)

def reach_score(score, interval):
    if score>interval:
        x = random.randint(15, 95)
        y = random.randint(8, 70)
        print(x, y)
        fire_sprite = displayio.TileGrid(fire_bitmap, pixel_shader=fire_bitmap.pixel_shader)
        fire_sprite.x = x
        fire_sprite.y = y
        fires.append(fire_sprite)
        splash.insert(1, fire_sprite)
        return 0
    return score





fires = []
while True:
    left = False
    mid = False
    right = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                duck_frame = changeSprite(duck_frame, 3)
                left = True
            if keys[pygame.K_UP]or keys[pygame.K_DOWN]:
                duck_frame = changeSprite(duck_frame, 1)
                mid = True
            if keys[pygame.K_RIGHT]:
                duck_frame = changeSprite(duck_frame, 2)
                right = True
        elif event.type == pygame.KEYUP:
            duck_frame = changeSprite(duck_frame, 0)

    if game_over:
        if left or right or mid:
            game_over = False
            splash.remove(try_again_sprite)
    else:
        spawn_arrows()
        score = reach_score(score, 5)
    for a in arrows:
        a.move()
        if arrow_collision(a.sprite):
            display_game_over()
            game_over = True
            score = 0
            splash.append(try_again_sprite)
            break
        if left and a.orientation == 1 and arrow_dance(a.sprite):
            remove_arrow(a)
            score+=1
        elif mid and a.orientation == 2 and arrow_dance(a.sprite):
            remove_arrow(a)
            score += 1
        elif right and a.orientation == 3 and arrow_dance(a.sprite):
            remove_arrow(a)
            score += 1




    time.sleep(0.1)