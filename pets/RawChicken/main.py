import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import random

scale = 2
display_width = 128 * scale
display_height = 128 * scale
display = PyGameDisplay(width=display_width, height=display_height)
splash = displayio.Group(scale=scale)
display.show(splash)

backgrounds = [
    displayio.OnDiskBitmap("background1.bmp"),
    displayio.OnDiskBitmap("background2.bmp")
]
current_bg = 0

bird_frames = [
    displayio.OnDiskBitmap("fly1.bmp"),
    displayio.OnDiskBitmap("fly2.bmp")
]
dead_bird = displayio.OnDiskBitmap("dead.bmp")

columns = {
    "short": displayio.OnDiskBitmap("short-column.bmp"),
    "medium": displayio.OnDiskBitmap("medium-column.bmp")
}

food = displayio.OnDiskBitmap("Food.bmp")

bg_sprite = displayio.TileGrid(backgrounds[current_bg], pixel_shader=backgrounds[current_bg].pixel_shader)
splash.append(bg_sprite)

bird = displayio.TileGrid(
    bird_frames[0],
    pixel_shader=bird_frames[0].pixel_shader,
    x=16,
    y=56
)
splash.append(bird)

active_columns = []
active_collectibles = []

score = 0
score_bitmap = displayio.Bitmap(128, 8, 1)
score_palette = displayio.Palette(1)
score_palette[0] = 0xFFFFFF
score_display = displayio.TileGrid(score_bitmap, pixel_shader=score_palette, x=0, y=4)
splash.append(score_display)

bird_velocity = 0
gravity = 0.5
jump_strength = -8
game_over = False
last_bg_switch = time.monotonic()

def reset_game():
    global game_over, bird_velocity, score, current_bg, last_bg_switch, bird
    
    game_over = False
    bird_velocity = 0
    score = 0
    
    bird = displayio.TileGrid(
        bird_frames[0],
        pixel_shader=bird_frames[0].pixel_shader,
        x=16,
        y=56
    )
    splash.append(bird)
    
    score_bitmap.fill(0)
    
    for column in active_columns[:]:
        splash.remove(column)
    active_columns.clear()
    
    for collectible in active_collectibles[:]:
        splash.remove(collectible)
    active_collectibles.clear()
    
    current_bg = 0
    bg_sprite.bitmap = backgrounds[current_bg]
    last_bg_switch = time.monotonic()

def switch_background():
    global current_bg
    current_bg = (current_bg + 1) % len(backgrounds)
    bg_sprite.bitmap = backgrounds[current_bg]

def spawn_column():
    column_type = random.choice(["short", "medium"])
    y_position = 0 if column_type == "short" else 128 - 32
    column = displayio.TileGrid(
        columns[column_type],
        pixel_shader=columns[column_type].pixel_shader,
        x=128,
        y=y_position
    )
    active_columns.append(column)
    splash.append(column)

def spawn_food():
    collectible = displayio.TileGrid(
        food,
        pixel_shader=food.pixel_shader,
        x=128,
        y=random.randint(16, 112)
    )
    active_collectibles.append(collectible)
    splash.append(collectible)

def check_collision(obj1, obj2):
    return (
        obj1.x < obj2.x + obj2.tile_width and
        obj1.x + obj1.tile_width > obj2.x and
        obj1.y < obj2.y + obj2.tile_height and
        obj1.y + obj1.tile_height > obj2.y
    )

def game_over_screen():
    dead_bird_grid = displayio.TileGrid(
        dead_bird,
        pixel_shader=dead_bird.pixel_shader,
        x=bird.x,
        y=bird.y
    )
    splash.remove(bird)
    splash.append(dead_bird_grid)
    
    overlay_palette = displayio.Palette(1)
    overlay_palette[0] = 0x404040 
    overlay = displayio.Bitmap(128, 128, 1)
    overlay_tilegrid = displayio.TileGrid(
        overlay,
        pixel_shader=overlay_palette,
        x=0,
        y=0
    )
    
    text_palette = displayio.Palette(1)
    text_palette[0] = 0xFFFFFF
    text = displayio.Bitmap(64, 8, 1)
    text_tilegrid = displayio.TileGrid(
        text,
        pixel_shader=text_palette,
        x=32,
        y=60
    )
    
    splash.append(overlay_tilegrid)
    splash.append(text_tilegrid)
    
    return overlay_tilegrid, text_tilegrid, dead_bird_grid

last_frame = time.monotonic()
last_spawn = time.monotonic()
game_over_elements = None

while True:
    current_time = time.monotonic()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_over:
                if game_over_elements:
                    overlay, text, dead_bird_grid = game_over_elements
                    splash.remove(overlay)
                    splash.remove(text)
                    splash.remove(dead_bird_grid)
                    game_over_elements = None
                reset_game()
            else:
                bird_velocity = jump_strength
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            bird_velocity = jump_strength

    if not game_over:
        if current_time - last_frame > 0.15:
            bird.bitmap = bird_frames[int((current_time % 0.3) > 0.15)]
            last_frame = current_time

        bird_velocity += gravity
        bird.y += int(bird_velocity)

        if current_time - last_bg_switch > 10:
            switch_background()
            last_bg_switch = current_time

        if current_time - last_spawn > 2:
            spawn_column()
            if random.random() < 0.3:
                spawn_food()
            last_spawn = current_time

        for column in active_columns:
            column.x -= 2
            if check_collision(bird, column):
                game_over = True
                game_over_elements = game_over_screen()

        for food_item in active_collectibles:
            food_item.x -= 2
            if check_collision(bird, food_item):
                score += 1
                score_bitmap[score-1, 0] = 1
                splash.remove(food_item)
                active_collectibles.remove(food_item)

        active_columns[:] = [c for c in active_columns if c.x > -32]
        active_collectibles[:] = [f for f in active_collectibles if f.x > -16]

        bird.y = max(16, min(112, bird.y))

    time.sleep(0.016)