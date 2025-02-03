import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
# import terminalio
import random







# import bitmaptools

# def bitmar_from_on_disk(on_disk_bitmap):
#     width, height = on_disk_bitmap.width, on_disk_bitmap.height
#     new_bitmap = displayio.Bitmap(width, height, 256)
#     bitmaptools.blit(new_bitmap, on_disk_bitmap, 0, 0)
#     return new_bitmap

# def resize_bitmap(source_bitmap, scale_factor):
#     new_width = max(1, int(source_bitmap.width * scale_factor))
#     new_height = max(1, int(source_bitmap.height * scale_factor))

#     new_bitmap = displayio.Bitmap(new_width, new_height, 256)

#     for y in range(new_height):
#         for x in range(new_width):
#             src_x = int(x / scale_factor)
#             src_y = int(y / scale_factor)
#             new_bitmap[x, y] = source_bitmap[src_x, src_y]
#     return new_bitmap

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()

tile_width = 32
tile_height = 32

game_over = False


# scale = 3
# display_width = 128 * scale
# display_height = 128 * scale
# display = PyGameDisplay(width=384, height=384)
# splash = displayio.Group(scale=scale)

display.show(splash)

castle_background = displayio.OnDiskBitmap("castle.bmp")

bg_castle_sprite = displayio.TileGrid(
    castle_background,
    pixel_shader=castle_background.pixel_shader
)

splash.append(bg_castle_sprite)

grassy_background = displayio.OnDiskBitmap("grassy-field.bmp")

bg_grassy_sprite = displayio.TileGrid(
    grassy_background,
    pixel_shader=grassy_background.pixel_shader
)

eat_icon = displayio.OnDiskBitmap("eat.bmp")

eat_icon_highlighted = displayio.OnDiskBitmap("eat-highlighted.bmp")

game_icon = displayio.OnDiskBitmap("game.bmp")

game_icon_highlighted = displayio.OnDiskBitmap("game-highlighted.bmp")

# eat_icon_original = bitmar_from_on_disk(eat_icon)

# scaled_eat_icon = resize_bitmap(eat_icon, 0.5)

eat_sprite = displayio.TileGrid(
    eat_icon,
    pixel_shader=eat_icon.pixel_shader,
    width=1,
    height=1,
    tile_width=16,
    tile_height=16,
    default_tile=0,
    x=10,
    y=10
)

eat_sprite_highlighted = displayio.TileGrid(
    eat_icon_highlighted,
    pixel_shader=eat_icon_highlighted.pixel_shader,
    width=1,
    height=1,
    tile_width=16,
    tile_height=16,
    default_tile=0,
    x=10,
    y=10
)

game_sprite = displayio.TileGrid(
    game_icon,
    pixel_shader=game_icon.pixel_shader,
    width=1,
    height=1,
    tile_width=16,
    tile_height=16,
    default_tile=0,
    x=31,
    y=10
)

game_sprite_highlighted = displayio.TileGrid(
    game_icon_highlighted,
    pixel_shader=game_icon_highlighted.pixel_shader,
    width=1,
    height=1,
    tile_width=16,
    tile_height=16,
    default_tile=0,
    x=31,
    y=10
)

# splash.append(eat_sprite)

# scale_factor = 0.5

# eat_group = displayio.Group(scale=)
fontFile = "fonts/PressStart2P-Regular-5pt.bdf"
fontToUse = bitmap_font.load_font(fontFile)

arrow_left = displayio.OnDiskBitmap("arrow-left.bmp")

arrow_right = displayio.OnDiskBitmap("arrow-right.bmp")

arrow_left_sprite = displayio.TileGrid(
    arrow_left,
    pixel_shader=arrow_left.pixel_shader,
    width=1,
    height=1,
    tile_width=16,
    tile_height=16,
    default_tile=0,
    x=10,
    y=100
)

arrow_right_sprite = displayio.TileGrid(
    arrow_right,
    pixel_shader=arrow_right.pixel_shader,
    width=1,
    height=1,
    tile_width=16,
    tile_height=16,
    default_tile=0,
    x=100,
    y=100
)



def play_game(splash):
    print("Playing game")
    score = 0
    round = 0

    score_display = label.Label(font=fontToUse, color=0x581845, text="Score:"+str(score))
    round_display = label.Label(font=fontToUse, color=0x581845, text="Round:"+str(round))

    score_display.x = 10
    score_display.y = 40

    round_display.x = 10
    round_display.y = 50

    splash.append(score_display)
    splash.append(round_display)

    princess_sprite.x = 64 - 16

    while round < 5:

        pygame.event.clear()

        event = pygame.event.wait()

        # if event.type == pygame.KEYDOWN:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
        # while True:
        #     for event in pygame.event.get():
        #         if event.type == KEYDOWN:
        #             return

            left = False
            right = False

            left_selected = False
            right_selected = False

            number = random.randint(0, 1)

            print(number)

            if number == 0:
                left_selected = True
                right_selected = False
            elif number == 1:
                left_selected = False
                right_selected = True

            

            

            
            
            if keys[pygame.K_LEFT]:
                left = True
                right = False
            elif keys[pygame.K_RIGHT]:
                left = False
                right = True

            time.sleep(0.1)

            if left_selected == True:
                splash.append(arrow_left_sprite)
                try:
                    splash.remove(arrow_right_sprite)
                except:
                    pass

            if right_selected == True:
                splash.append(arrow_right_sprite)
                try:
                    splash.remove(arrow_left_sprite)
                except:
                    pass

            print("Left:", left, "Right:", right)

            if left == left_selected or right == right_selected:
                score += 1
                score_display.text = "Score:"+str(score)

            round = round + 1
            round_display.text = "Round:"+str(round)
            print("Round:", round)

        time.sleep(0.5)
        try:
            splash.remove(arrow_left_sprite)
        except:
            pass
        
        try:
            splash.remove(arrow_right_sprite)
        except:
            pass
    
    try:
        splash.remove(arrow_left_sprite)
    except:
        pass

    try:
        splash.remove(arrow_right_sprite)
    except:
        pass

    try:
        splash.remove(score_display)
    except:
        pass

    try:
        splash.remove(round_display)
    except:
        pass


princess_sheet = displayio.OnDiskBitmap("princess_kitty_sheet.bmp")


princess_sprite = displayio.TileGrid(
    princess_sheet,
    pixel_shader=princess_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=32,
    tile_height=32,
    default_tile=0,
    x=(display.width - tile_width) // 2,
    y=display.height - tile_height - 10
)


splash.append(princess_sprite)

grass = False
castle = True
playing = False

frame = 0
speed = 4
display_width = 128

# princess_sprite.x = 64

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    princess_sprite[0] = frame
    frame = (frame + 1) % (princess_sheet.width // tile_width)

    time.sleep(0.1)

    keys = pygame.key.get_pressed()

    if game_over == False and playing == False:
        if keys[pygame.K_LEFT]:
            princess_sprite.x -= speed
        if keys[pygame.K_RIGHT]:
            princess_sprite.x += speed
    

        if (castle_background.width - 32 < princess_sprite.x):
            if grass == False:
                splash.remove(bg_castle_sprite)
                splash.append(bg_grassy_sprite)
                splash.append(princess_sprite)
                splash.append(eat_sprite)
                splash.append(game_sprite)
                princess_sprite.x = -4
                grass = True
                castle = False
            else:
                princess_sprite.x = castle_background.width - 32

        if princess_sprite.x == -8:
            if grass == True:
                # print("out of bounds - right")
                splash.remove(bg_grassy_sprite)
                splash.append(bg_castle_sprite)
                splash.append(princess_sprite)
                splash.remove(eat_sprite)
                splash.remove(game_sprite)
                princess_sprite.x = display_width - 32
                grass = False
                castle = True
            else:
                princess_sprite.x = -4

        # if (princess_sprite.x == -4):
        #     if grass == True:
        #         # print("out of bounds - right")
        #         splash.remove(bg_grassy_sprite)
        #         splash.append(bg_castle_sprite)
        #         splash.append(princess_sprite)

        if princess_sprite.x > 0 and princess_sprite.x < 16 and grass == True:
            try:
                splash.remove(eat_sprite)
            except:
                pass
            splash.append(eat_sprite_highlighted)
            # if keys[pygame.K_UP]:


        elif grass == True:
            try:
                splash.remove(eat_sprite_highlighted)
            except:
                pass
            splash.append(eat_sprite)
        
        if princess_sprite.x > 16 and princess_sprite.x < 31 and grass == True:
            try:
                splash.remove(game_sprite)
            except:
                pass
            splash.append(game_sprite_highlighted)

            if keys[pygame.K_UP]:
                playing = True
                print("Game started")
                play_game(splash=splash)
                print("Game ended")
                playing = False

        elif grass == True:
            try:
                splash.remove(game_sprite_highlighted)
            except:
                pass
            splash.append(game_sprite)
    
