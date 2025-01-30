import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect
import random
from potato import Potato

waterIncrese = 1
foodIncrese = 1
bugDecrese = 1

waterDecrese = 1
foodDecrese = 1
bugIncrese = 1

#Note: Higher number means lower chance
chanceOfDecrese = 1000
chanceOfBug = 500
chanceOfDamg = 700

def updateBar(splash, bar, maxBar, thing, maxThing, color):
    if bar:
        splash.remove(bar)
    if round((maxBar.width/maxThing)*thing) <= 0:
        return None
    bar = Rect(maxBar.x,maxBar.y,round((maxBar.width/maxThing)*thing),maxBar.height,fill=color)
    splash.append(bar)
    return bar
    

pygame.init()
display=PyGameDisplay(width=128, height=128,hw_accel=False)
splash = displayio.Group()

display.show(splash)

bgrImage = displayio.OnDiskBitmap("background.bmp")
bgrSprite = displayio.TileGrid(bgrImage,pixel_shader=bgrImage.pixel_shader)

splash.append(bgrSprite)

tile_width=32
tile_height=32
potatoImage = displayio.OnDiskBitmap("Potato.bmp")
potatoSprite = displayio.TileGrid(
    potatoImage,
    pixel_shader=potatoImage.pixel_shader,
    width=1,
	height=1,
	tile_width=32,
	tile_height=32,
	default_tile=0,
	x=(display.width - tile_width) // 2,
	y=display.height - tile_height - 10
)

splash.append(potatoSprite)

frame = 0

spud = Potato(10,10,10,10)


waterOutline = Rect(10,10,32,4,outline=0xFFFFFF)
foodOutline = Rect(10,16,32,4,outline=0xFFFFFF)
bugOutline = Rect(10,22,32,4,outline=0xFFFFFF)

waterBar = updateBar(splash, None, waterOutline,spud.water,spud.maxWater,0x0000FF)
foodBar = updateBar(splash, None, foodOutline, spud.food, spud.maxFood, 0xDAA06D)
bugBar = updateBar(splash, None, bugOutline, spud.bugs, spud.maxBugs, 0xFF0000)

splash.append(waterOutline)
splash.append(foodOutline)
splash.append(bugOutline)

while True:

    #This check to see if the X on the window has been pressed. Will be replaced for circitpython
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                spud.water+= waterIncrese
                if spud.water > spud.maxWater:
                    spud.water = spud.maxWater
                print(spud.water)
            if event.key == pygame.K_2:
                spud.food += foodIncrese
                if spud.food > spud.maxFood:
                    spud.food = spud.maxFood
                print(spud.food)
            if event.key == pygame.K_3:
                spud.bugs -= bugDecrese
                if spud.bugs < 0:
                    spud.bugs = 0
                print(spud.bugs)
    
    #decrese water and food
    randNum = random.randint(0, chanceOfDecrese)
    if randNum == 0:
        spud.water -= waterDecrese
        if spud.water < 0:
            spud.water = 0
        print(f"water:{spud.water}")
    if randNum == 1:
        spud.food -= foodDecrese
        if spud.food < 0:
            spud.food = 0
        print(f"food:{spud.food}")
    
    #add bugs
    if spud.water > (spud.maxWater*0.75) or spud.food > (spud.maxFood*0.75):
        if spud.water > (spud.maxWater*0.75) and spud.food < (spud.maxFood*0.75):
            tmpChanceOfBug = chanceOfBug/2
        else:
            tmpChanceOfBug = chanceOfBug
        if random.randint(0, tmpChanceOfBug) == 0:
            spud.bugs+=1
            if spud.bugs > spud.maxBugs:
                spud.bugs = spud.maxBugs
            print(f"bugs:{spud.bugs}")
    
    if spud.water < (spud.maxWater*0.25) or spud.food < (spud.maxFood):
        if spud.water < (spud.maxWater*0.25) and spud.food < (spud.maxFood):
            tmpChanceOfDamg = chanceOfDamg/2
        else:
            tmpChanceOfDamg = chanceOfDamg
        if random.randint(0, chanceOfDamg) == 0:
            spud.health -= 1
    
    if spud.bugs > 0:
        if spud.bugs > (spud.maxBugs*0.75):
            tmpChanceOfDamg = chanceOfDamg/2
        else:
            tmpChanceOfDamg = chanceOfDamg
        if random.randint(0, chanceOfDamg) == 0:
            spud.health -= 1
        #TODO: potato image should get sadder as health drops

            

    #textArea.text = f"Water: {spud.water}\nFerilizer: {spud.food}\nBugs: {spud.bugs}"
    
    
    waterBar = updateBar(splash, waterBar, waterOutline, spud.water, spud.maxWater, 0x0000FF)
    foodBar = updateBar(splash, foodBar,foodOutline,spud.food,spud.maxFood,0xDAA06D)
    bugBar = updateBar(splash, bugBar, bugOutline, spud.bugs, spud.maxBugs, 0xFF0000)


    
    
    potatoSprite[0] = (frame + 1) % (potatoImage.width // tile_width)

    time.sleep(0.01)
