import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import random
import time
from adafruit_display_text import label
import random
import sys
import os

pygame.init()
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)
pygame.font.init()

programIcon = pygame.image.load('Erebus_Nightflitter.bmp')

pygame.display.set_icon(programIcon)

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

door_2_sprite = displayio.OnDiskBitmap("door_2.bmp")

door_2_sprite = displayio.TileGrid(
	door_2_sprite, 
	pixel_shader=space_station_background.pixel_shader
)

food_dispenser = displayio.OnDiskBitmap("food_dispenser.bmp")

food_dispenser_sprite = displayio.TileGrid(
	food_dispenser, 
	pixel_shader=space_station_background.pixel_shader
)

splash.append(bg_sprite)
splash.append(door_1_sprite)
splash.append(door_2_sprite)
splash.append(food_dispenser_sprite)

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
	y=display.height - tile_height - 0
)

splash.append(erebus_sprite)

#here be warnings
score = 10
score_increment = 10
round = 0
hunger = 40
hunger_increment = 20
hunger_round_increment = 10
ate = False
warning = False
warning_door_1 = False
warning_door_2 = False
warning_AME = False
warning_Singulo = False
warning_TEG = False
frame = 0
speed = 32

class Score(object):
    def __init__(self):
        self.black = 0,0,0
        self.count = 0
        self.font = pygame.font.SysFont("comicsans",50, True , True)
        self.text = self.font.render("Score : "+str(self.count),1,self.black)

    def show_score(self, screen):
        screen.blit(self.text, (100 ,100))

    def score_up(self):
        self.count += 1
        self.text = self.font.render("Score : "+str(self.count),1,self.black)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                erebus_sprite.x -= speed
                print ("x:", erebus_sprite.x)
                print ("y:", erebus_sprite.y)
                print ("Hunger: ", hunger)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                erebus_sprite.x += speed
                print ("x:", erebus_sprite.x)
                print ("y:", erebus_sprite.y)
                print ("Hunger: ", hunger)
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                erebus_sprite.y -= speed
                print ("x:", erebus_sprite.x)
                print ("y:", erebus_sprite.y)
                print ("Hunger: ", hunger)

    #wrap around the sides
    if erebus_sprite.x < 0:
        erebus_sprite.x = 0
    elif erebus_sprite.x > display.width - tile_width:
        erebus_sprite.x = display.width - tile_width

    erebus_sprite.x = erebus_sprite.x
    
    #wrap around the top
    if erebus_sprite.y < 0:
        erebus_sprite.y = display.height - tile_height
        score += score_increment #temporary
        round += 1
        hunger += hunger_round_increment
        ate = False
        print ("Round: ", round)
        print ("Score: ", score)
        print ("Hunger: ", hunger)

    if erebus_sprite.x == 96 and erebus_sprite.y == 64 and hunger >= 1 and ate == False:
        hunger -= hunger_increment
        print ("Hunger: ", hunger)
        ate = True

    #if hunger <= 0:
        #hunger = 0
        #print ("Hunger: ", hunger)

    erebus_sprite[0] = frame
    frame = (frame + 1) % (erebus_sheet.width // tile_width)

    pygame.time.wait(100)