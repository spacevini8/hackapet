import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import adafruit_display_text
import random
import pygame.freetype
import json
from itertools import cycle

pygame.init()
pygame.freetype.init()

font_path = "PressStart2P-Regular.ttf"
font_score = pygame.freetype.Font(font_path, size=22)
font_highscore = pygame.freetype.Font(font_path, size=7)

display = PyGameDisplay(width=128, height=128) # real 128x128
splash = displayio.Group()
display.show(splash)

start_screen = displayio.OnDiskBitmap("start_screen.png")
start_screen_sprite = displayio.TileGrid(start_screen, pixel_shader=start_screen.pixel_shader)

adam_night_background = displayio.OnDiskBitmap("adam_night_background.png")
adam_night_bg_sprite = displayio.TileGrid(adam_night_background, pixel_shader=adam_night_background.pixel_shader)

night_background = displayio.OnDiskBitmap("night_background.png")
night_bg_sprite = displayio.TileGrid(night_background, pixel_shader=night_background.pixel_shader)

sky_background = displayio.OnDiskBitmap("background.bmp")
bg_sprite = displayio.TileGrid(sky_background, pixel_shader=sky_background.pixel_shader)
splash.append(start_screen_sprite)


characters = {
    'mc.png' : (32, 30), 'Stickman.png' : (16, 32), 'ariana_racoon.png': (30, 30)
}

skin_list = list(characters.keys())
skin_cycle = cycle(skin_list)

selection = 'Stickman.png'
pet_sheet = displayio.OnDiskBitmap(selection)


pet_sprite = displayio.TileGrid(
    pet_sheet,
    pixel_shader=pet_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width= 32,
    tile_height= 32,
    default_tile=0,
    x=(display.width - 32) // 2,  
    y=display.height - 32 - 10     
)

exit_button_bitmap = displayio.OnDiskBitmap("exit_button.bmp")
skins_button_bitmap = displayio.OnDiskBitmap("skins_button.bmp")
start_button_bitmap = displayio.OnDiskBitmap("start_button.bmp")

start_button_sprite = displayio.TileGrid(
    start_button_bitmap,
    pixel_shader=start_button_bitmap.pixel_shader,
    width=1,  
    height=1,  
    tile_width=start_button_bitmap.width // 2,  # Width of each frame
    tile_height=start_button_bitmap.height,  # Height of each frame
    x=28,
    y=48
)

skins_button_sprite = displayio.TileGrid(
    skins_button_bitmap,
    pixel_shader=skins_button_bitmap.pixel_shader,
    width=1,  
    height=1,  
    tile_width=skins_button_bitmap.width // 2,  # Width of each frame
    tile_height=skins_button_bitmap.height,  # Height of each frame
    x=28,
    y=65
)

exit_button_sprite = displayio.TileGrid(
    exit_button_bitmap,
    pixel_shader=exit_button_bitmap.pixel_shader,
    width=1,  
    height=1,  
    tile_width=exit_button_bitmap.width // 2,  # Width of each frame
    tile_height=exit_button_bitmap.height,  # Height of each frame
    x=28,
    y=82
)



current_button = 'start'

def scroll_up():
    global selection, current_button, start_button_sprite, skins_button_sprite, exit_button_sprite
    if current_button == 'start':
        current_button = 'exit'
        print(current_button)
        start_button_sprite[0] = 0
        exit_button_sprite[0] = 1
    elif current_button == 'exit':
        current_button = 'skins'
        print(current_button)
        exit_button_sprite[0] = 0
        skins_button_sprite[0] = 1
    elif current_button == 'skins':
        current_button = 'start'
        print(current_button)
        start_button_sprite[0] = 1
        skins_button_sprite[0] = 0
    time.sleep(0.5)
        


current_state = 'day'
bombs = []
bomb_bitmap = displayio.OnDiskBitmap("bomb.bmp")

gem_bitmap = displayio.OnDiskBitmap("gem.png")

gems = []
font_col = 1
score = 0
lives = 3

background_font_colors = {
    'day': 1,  
    'night': 2,  
    'adam_night': 2  
}

heart_bitmap = displayio.OnDiskBitmap("heart.png")

def render_lives(lives):
    hearts = displayio.Group()
    for i in range(lives):
        heart = displayio.TileGrid(
            heart_bitmap,
            pixel_shader=heart_bitmap.pixel_shader,
            width=1,
            height=1,
            tile_width=heart_bitmap.width,
            tile_height=heart_bitmap.height,
            x=display.width - (i + 1) * (heart_bitmap.width + 3),  
            y=5  
        )
        hearts.append(heart)
    return hearts

def render_high_score(high_score):
    high_score_text = f"Best: {high_score}"
    high_score_surface, _ = font_highscore.render(high_score_text, (0, 0, 0))  
    high_score_texture = pygame.image.tostring(high_score_surface, "RGBA", True)
    high_score_bitmap = displayio.Bitmap(high_score_surface.get_width(), high_score_surface.get_height(), 4)
    high_score_palette = displayio.Palette(4)
    high_score_palette.make_transparent(0)
    high_score_palette[1] = 0x000033  
    high_score_palette[2] = 0xFFFFFF  
    high_score_palette[3] = 0xFF0000

    for y in range(high_score_surface.get_height()):
        for x in range(high_score_surface.get_width()):
            pixel = high_score_surface.get_at((x, y))
            if pixel[3] > 0:  # If alpha > 0
                high_score_bitmap[x, y] = font_col  

    high_score_tilegrid = displayio.TileGrid(high_score_bitmap, pixel_shader=high_score_palette, x=50, y=105)
    return high_score_tilegrid


def render_score(score):
    score_surface, _ = font_score.render(str(score), (0, 0, 0))  
    score_texture = pygame.image.tostring(score_surface, "RGBA", True)
    score_bitmap = displayio.Bitmap(score_surface.get_width(), score_surface.get_height(), 4)
    score_palette = displayio.Palette(4)
    score_palette.make_transparent(0)
    score_palette[1] = 0x000033  
    score_palette[2] = 0xFFFFFF  
    score_palette[3] = 0xFF0000

    for y in range(score_surface.get_height()):
        for x in range(score_surface.get_width()):
            pixel = score_surface.get_at((x, y))
            if pixel[3] > 0:  # If alpha > 0
                score_bitmap[x, y] = font_col  

    score_tilegrid = displayio.TileGrid(score_bitmap, pixel_shader=score_palette, x=1, y=1)
    return score_tilegrid

score_display = render_score(score)


def spawn_gem():
    x_position_gem = random.randint(0, display.width - gem_bitmap.width)
    gem = displayio.TileGrid(
        gem_bitmap,
        pixel_shader=gem_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=gem_bitmap.width ,
        tile_height=gem_bitmap.height ,
        x=x_position_gem,
        y=-32
    )

    overlap_g = False
    for i in gems:
        if check_overlap(gem, i):
            overlap_g = True
            break
    if not overlap_g:
        gems.append(gem)
        splash.append(gem)

def spawn_bomb():
    x_position_bomb = random.randint(0, display.width - 16)
    bomb = displayio.TileGrid(
        bomb_bitmap,
        pixel_shader=bomb_bitmap.pixel_shader,
        width=1,
        height=1,
        tile_width=16 ,
        tile_height=16 ,
        x=x_position_bomb,
        y=-32
        
    )
    overlap_b = False
    for i in bombs:
        if check_overlap(bomb, i):
            overlap_b = True
            break
    if not overlap_b:
        bombs.append(bomb)
        splash.append(bomb)
    

def switch_background():
    global current_state, font_col, score_display, lives_display, gems, bombs
    if random.choice([0, 1, 2]) == 1:
        if current_state == 'day':
            current_state = 'night'
            splash.remove(bg_sprite)
            print(current_state)
            splash.append(night_bg_sprite)
            font_col = background_font_colors[current_state]
        elif current_state == 'adam_night':
            current_state = 'night'
            splash.remove(adam_night_bg_sprite)
            print(current_state)
            splash.append(night_bg_sprite)
            font_col = background_font_colors[current_state]
    elif random.choice([0, 1]) == 1:
        if current_state == 'day':
            current_state = 'adam_night'
            font_col = background_font_colors[current_state]
            print(current_state)
            splash.remove(bg_sprite)
            splash.append(adam_night_bg_sprite)
        elif current_state == 'night':
            current_state = 'adam_night'
            splash.remove(night_bg_sprite)
            print(current_state)
            splash.append(adam_night_bg_sprite)
            font_col = background_font_colors[current_state]
    else:
        if current_state == 'night':
            current_state = 'day'
            splash.remove(night_bg_sprite)
            print(current_state)
            splash.append(bg_sprite)
            font_col = background_font_colors[current_state]
        elif current_state == 'adam_night':
            current_state = 'day'
            splash.remove(adam_night_bg_sprite)
            print(current_state)
            splash.append(bg_sprite)
            font_col = background_font_colors[current_state]
        
        
        if score_display in splash:    
            splash.remove(score_display)
        score_display = render_score(score)
        splash.append(score_display)

    if lives_display in splash:
        splash.remove(lives_display)
    lives_display = render_lives(lives)
    splash.append(lives_display)
    if pet_sprite in splash:
        splash.remove(pet_sprite)
    splash.append(pet_sprite) 
    for i in bombs:
        splash.remove(i)
        bombs.remove(i)

def generate_mask(sprite, bitmap):
    width, height = characters[selection][0], characters[selection][1]
    mask = []
    for y in range(height):
        row = []
        for x in range(width):
            pixel = bitmap[x, y]
            row.append(pixel != 0)  
        mask.append(row)
    return mask


def check_pet_collision(pet_sprite, other_sprite, bitmap):
    pet_width, pet_height = characters[selection][0], characters[selection][1]
    other_width, other_height = other_sprite.tile_width, other_sprite.tile_height

    x_overlap_start = max(pet_sprite.x, other_sprite.x)
    y_overlap_start = max(pet_sprite.y, other_sprite.y)
    x_overlap_end = min(pet_sprite.x + pet_width, other_sprite.x + other_width)
    y_overlap_end = min(pet_sprite.y + pet_height, other_sprite.y + other_height)

    pet_mask = generate_mask(pet_sprite, pet_sheet)
    other_mask = generate_mask(other_sprite, bitmap)

    for y in range(y_overlap_start, y_overlap_end):
        for x in range(x_overlap_start, x_overlap_end):
            pixel1_x = x - pet_sprite.x
            pixel1_y = y - pet_sprite.y
            pixel2_x = x - other_sprite.x
            pixel2_y = y - other_sprite.y

            if pet_mask[pixel1_y][pixel1_x] and other_mask[pixel2_y][pixel2_x]:
                return True

    return False


def check_overlap(item1, item2):
    return (
        item1.x < item2.x + item2.tile_width and
        item1.x + item1.tile_width > item2.x and
        item1.y < item2.y + item2.tile_height and
        item1.y + item1.tile_height > item2.y
    )

death = displayio.OnDiskBitmap("deathscreen.png")

def display_game_over():
    global death_hi
    death_hi = displayio.TileGrid(
        death,
        pixel_shader=pet_sheet.pixel_shader,
        width=1,
        height=1,
        tile_width=display.width,
        tile_height=display.height,
        default_tile=0,
        x=0,  
        y=0 
    )
    splash.append(death_hi)
    if gems or bombs:
        for i in gems + bombs:
            splash.remove(i)
        gems.clear()
        bombs.clear()


def get_high_score(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            if isinstance(data, dict):
                return data.get('high_score', 0)
            else:
                return 0
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def save_high_score(file_path, score):
    data = {'high_score': score}
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def update_high_score(file_path, current_score):
    high_score = get_high_score(file_path)
    if current_score > high_score:
        save_high_score(file_path, current_score)
        return current_score
    return current_score

def update_score(score, score_display):
    if score_display in splash:
        splash.remove(score_display)
    score_display = render_score(score)
    splash.append(score_display)
    return score_display

def update_lives_display(lives, lives_display):
    if lives_display in splash:
        splash.remove(lives_display)
    lives_display = render_lives(lives)
    splash.append(lives_display)
    return lives_display

pet_frame = 0
bomb_frame = 0
speed = 4 
game_over = False
gem_rate = 0.03
bomb_rate = 0.04
spawned = False
game_started = False
current_button = 'start'
current_preview_sprite = None
high_score = get_high_score('High_scores.json')
high_score_display = render_high_score(high_score)



while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            update_high_score('High_scores.json', score)
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_over == True and game_started == True:
                for x in splash:
                    splash.remove(x)
                splash.append(start_screen_sprite)
                splash.append(start_button_sprite)
                splash.append(skins_button_sprite) 
                splash.append(exit_button_sprite)
                gem_rate = 0.04
                bomb_rate = 0.04
                score = 0
                game_over = False
                game_started = False
                lives = 3
                start_time = time.time()
                current_state = 'day'

    keys = pygame.key.get_pressed()

    if game_started == False:
        if keys[pygame.K_UP]:
            scroll_up()
        if start_button_sprite not in splash:
            splash.append(start_button_sprite)
        if skins_button_sprite not in splash:
            splash.append(skins_button_sprite)
        if exit_button_sprite not in splash:
            splash.append(exit_button_sprite)
        if high_score_display not in splash:
            high_score = get_high_score('High_scores.json')
            high_score_display = render_high_score(high_score)
            splash.append(high_score_display)
        if current_button == 'skins': 
            if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:      
                if current_preview_sprite and current_preview_sprite in splash:
                    splash.remove(current_preview_sprite)
                selection = next(skin_cycle)

                pet_sheet = displayio.OnDiskBitmap(selection)
                pet_sprite = displayio.TileGrid(
                            pet_sheet,
                            pixel_shader=pet_sheet.pixel_shader,
                            width=1,
                            height=1,
                            tile_width= 32,
                            tile_height= 32,
                            default_tile=0,
                            x=(display.width - 32) // 2,  
                            y=display.height - 32 - 10     
                        )

                preview_sprite = displayio.TileGrid(
                            pet_sheet,
                            pixel_shader=pet_sheet.pixel_shader,
                            width=1,
                            height=1,
                            tile_width=32,
                            tile_height=32,
                            default_tile=0,
                            x=5,
                            y=display.height - 32 - 10
                         )
                splash.append(preview_sprite)
                current_preview_sprite = preview_sprite
                time.sleep(0.3)
        elif current_button == 'exit':
            if keys[pygame.K_RIGHT]:
                        pygame.quit()
                        exit()
                        

                
        if current_button == 'start':
            start_button_sprite[0] = 1 
            if keys[pygame.K_RIGHT]:
                game_started = True
                splash.remove(high_score_display)
                splash.remove(start_button_sprite)
                splash.remove(skins_button_sprite)
                splash.remove(exit_button_sprite)
                splash.remove(start_screen_sprite)
                lives_display = render_lives(lives)
                splash.append(score_display)
                splash.append(bg_sprite)
                splash.append(lives_display)
                splash.append(pet_sprite)
                start_time = time.time()



    elif game_over == False and game_started == True:
        if keys[pygame.K_LEFT]:
            pet_sprite.x -= speed
            if pet_sprite.x < 0:
                pet_sprite.x = 0
        if keys[pygame.K_RIGHT]:
            pet_sprite.x += speed
            if pet_sprite.x + characters[selection][0] > display.width:
                pet_sprite.x = display.width - characters[selection][0] 
        if random.random() < gem_rate:  # spawn rate
            spawn_gem()
            spawned = True
        if random.random() < bomb_rate:  # spawn rate
            spawn_bomb()
            spawned = True
        
    

        for gem in gems:
            gem.y += 5 
            if gem.y + gem.tile_height > display.height - 10:
                splash.remove(gem)
                gems.remove(gem)
            elif check_pet_collision(pet_sprite, gem, gem_bitmap):
                score += 1
                score_display = update_score(score, score_display)
                if score % 15 == 0:
                    gem_rate += 0.01
                elif score % 10 == 0:
                    bomb_rate += 0.01
                if score % 10 == 0:
                    switch_background()
                    for j in bombs:
                        splash.remove(j)
                        bombs.remove(j)
                    for i in gems:
                        splash.remove(i)
                        gems.remove(i)
                if gem in gems:
                    gems.remove(gem)
                    splash.remove(gem)

        for bomb in bombs:
            bomb.y += 5 
            for i in gems:
                if check_overlap(bomb, i):
                    splash.remove(i)
                    gems.remove(i)
            if bomb.y + bomb.tile_height > display.height - 10:
                splash.remove(bomb)
                bombs.remove(bomb)
            elif check_pet_collision(pet_sprite, bomb, bomb_bitmap):
                lives -= 1
                lives_display = update_lives_display(lives, lives_display)
                # turn pet red momentarily, turn one led off
                if lives == 0:
                    game_over = True
                    
                    gem_rate = 0.03
                    bomb_rate = 0.03
                    score = update_high_score('High_scores.json', score)
                    display_game_over()
                    break
                else:
                    splash.remove(bomb)
                    bombs.remove(bomb)
            
                

        for bomb in bombs:
            bomb[0] = bomb_frame
            bomb_frame = (bomb_frame + 1) % (bomb_bitmap.width // 16)
        pet_sprite[0] = pet_frame
        pet_frame = (pet_frame + 1) % (pet_sheet.width // 32)

        if time.time() - start_time > 1 and spawned == False :
            start_time = time.time()
            spawn_gem()
        else:
            spawned = False
    time.sleep(0.1)
