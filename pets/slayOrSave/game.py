''' for now, use left and right arrow keys to move the player, B to kick the ball'''

import pygame
import time
from blinka_displayio_pygamedisplay import PyGameDisplay
import displayio
import random

pygame.init()
W, H = 128, 128
pygame.display.set_caption("Slay or Save")
clk = pygame.time.Clock()

disp = PyGameDisplay(width=W, height=H)

bg_files = ["bg_1.bmp", "bg_2.bmp", "bg_3.bmp"]
p_idle, p_k1, p_k2 = "player_idle.bmp", "player_kick_1.bmp", "player_kick_2.bmp"
gk_idle, gk_up = "goalkeeper_idle.bmp", "goalkeeper_hands_up.bmp"
fb_1, fb_2, gp = "football_1.bmp", "football_2.bmp", "goalpost.bmp"

def load_img(file):
    with open(file, "rb") as f:
        return displayio.OnDiskBitmap(f)

bgs = [load_img(f) for f in bg_files]
bg_idx = 0
bg_tile = displayio.TileGrid(bgs[bg_idx], pixel_shader=bgs[bg_idx].pixel_shader)
bg_grp = displayio.Group()
bg_grp.append(bg_tile)
disp.show(bg_grp)

p_imgs = [load_img(p_idle), load_img(p_k1), load_img(p_k2)]
p_tile = displayio.TileGrid(p_imgs[0], pixel_shader=p_imgs[0].pixel_shader, x=10, y=80)
bg_grp.append(p_tile)

gk_imgs = [load_img(gk_idle), load_img(gk_up)]
gk_tile = displayio.TileGrid(gk_imgs[0], pixel_shader=gk_imgs[0].pixel_shader, x=50, y=30)
gk_dir = 1
bg_grp.append(gk_tile)

fb_imgs = [load_img(fb_1), load_img(fb_2)]
fb_tile = displayio.TileGrid(fb_imgs[0], pixel_shader=fb_imgs[0].pixel_shader, x=40, y=90)
bg_grp.append(fb_tile)

gp_tile = displayio.TileGrid(load_img(gp), pixel_shader=load_img(gp).pixel_shader, x=32, y=10)
bg_grp.append(gp_tile)

score = 0
font = pygame.font.Font(None, 24)

def reset_ball():
    fb_tile.x = random.randint(10, W - 20)
    fb_tile.y = 90

def animate_kick():
    for img in p_imgs[1:]:
        p_tile.bitmap = img
        disp.refresh()
        time.sleep(0.1)
    p_tile.bitmap = p_imgs[0]

run = True
fb_dx, fb_dy = random.choice([-2, 2]), 0
ball_kicked, frame, bg_frame, fb_frame = False, 0, 0, 0

while run:
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and p_tile.x > 0:
        p_tile.x -= 2
    if keys[pygame.K_RIGHT] and p_tile.x < W - 20:
        p_tile.x += 2

    if keys[pygame.K_b]:
        animate_kick()
        ball_kicked, fb_dy = True, -3

    if ball_kicked:
        fb_tile.y += fb_dy

    fb_tile.x += fb_dx
    if fb_tile.x <= 0 or fb_tile.x >= W - 16:
        fb_dx *= -1

    if fb_tile.y <= gp_tile.y and gp_tile.x < fb_tile.x < gp_tile.x + 32:
        score += 1
        reset_ball()
        ball_kicked, fb_dy = False, 0

    if fb_tile.y <= gk_tile.y + 16 and gk_tile.x < fb_tile.x < gk_tile.x + 16:
        reset_ball()
        ball_kicked, fb_dy = False, 0

    gk_tile.x += gk_dir
    if gk_tile.x <= 0 or gk_tile.x >= W - 16:
        gk_dir *= -1

    frame += 1
    bg_frame += 1
    fb_frame += 1

    if frame >= 20:
        frame = 0
        cur_img = gk_imgs.index(gk_tile.bitmap)
        gk_tile.bitmap = gk_imgs[(cur_img + 1) % len(gk_imgs)]

    if bg_frame >= 20: 
        bg_frame = 0
        bg_idx = (bg_idx + 1) % len(bgs)
        bg_tile.bitmap = bgs[bg_idx]

    if fb_frame >= 10:  
        fb_frame = 0
        cur_fb = fb_imgs.index(fb_tile.bitmap)
        fb_tile.bitmap = fb_imgs[(cur_fb + 1) % len(fb_imgs)]

    disp.refresh()
    clk.tick(30)

pygame.quit()
