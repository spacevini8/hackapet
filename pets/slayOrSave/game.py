''' for now, use left and right arrow keys to move the player, B to kick the ball, C to end game'''
import pygame
import time
import random

pygame.init()
W, H = 128, 128
pygame.display.set_caption("Slay or Save")
clk = pygame.time.Clock()

screen = pygame.display.set_mode((W, H))

def load_img(file):
    return pygame.image.load(file)

start_img = load_img("starte.bmp")
screen.blit(start_img, (0, 0))
pygame.display.update()
time.sleep(4)

bg_files = ["bg_1.bmp", "bg_2.bmp", "bg_3.bmp"]
bgs = [load_img(f) for f in bg_files]
bg_idx = 0

p_imgs = [load_img("player_idle.bmp"), load_img("player_kick_1.bmp"), load_img("player_kick_2.bmp")]
gk_imgs = [load_img("goalkeeper_idle.bmp"), load_img("goalkeeper_hands_up.bmp")]
fb_imgs = [load_img("football_1.bmp"), load_img("football_2.bmp")]
gp_img = load_img("goalpost.bmp")

p_x, p_y = 10, 80
gk_x, gk_y = 50, 30
gp_x, gp_y = 32, 10
fb_x, fb_y = 40, 90

gk_dir = 1
score = 0
font = pygame.font.Font(None, 16) 

def reset_ball():
    global fb_x, fb_y, score
    if fb_y <= gp_y and not (gp_x < fb_x < gp_x + 32):
        score -= 1 
    fb_x = random.randint(10, W - 20)
    fb_y = 90

def animate_kick():
    for img in p_imgs[1:]:
        screen.blit(img, (p_x, p_y))
        pygame.display.update()
        time.sleep(0.1)

run = True
fb_dx, fb_dy = random.choice([-2, 2]), 0
ball_kicked, frame, bg_frame, fb_frame = False, 0, 0, 0

while run:
    screen.blit(bgs[bg_idx], (0, 0))
    screen.blit(gp_img, (gp_x, gp_y))
    screen.blit(p_imgs[0], (p_x, p_y))
    screen.blit(gk_imgs[0], (gk_x, gk_y))
    screen.blit(fb_imgs[0], (fb_x, fb_y))

    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and p_x > 0:
        p_x -= 2
    if keys[pygame.K_RIGHT] and p_x < W - 20:
        p_x += 2

    if keys[pygame.K_b]:
        animate_kick()
        ball_kicked, fb_dy = True, -3

    if keys[pygame.K_c]:  
        run = False

    if ball_kicked:
        fb_y += fb_dy

    fb_x += fb_dx
    if fb_x <= 0 or fb_x >= W - 16:
        fb_dx *= -1

    if fb_y <= gp_y and gp_x < fb_x < gp_x + 32:
        score += 1
        reset_ball()

    if fb_y <= gk_y + 16 and gk_x < fb_x < gk_x + 16:
        score -= 1
        reset_ball()

    if fb_y < 0: 
        score -= 1
        reset_ball()

    if score <= -3:  
        run = False

    gk_x += gk_dir
    if gk_x <= 0 or gk_x >= W - 16:
        gk_dir *= -1

    frame += 1
    bg_frame += 1
    fb_frame += 1

    if frame >= 20:
        frame = 0
        gk_imgs.reverse()

    if bg_frame >= 20:
        bg_frame = 0
        bg_idx = (bg_idx + 1) % len(bgs)

    if fb_frame >= 10:
        fb_frame = 0
        fb_imgs.reverse()

    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (5, 5))

    pygame.display.update()
    clk.tick(30)

end_img = load_img("ende.bmp")
screen.blit(end_img, (0, 0))
pygame.display.update()

end_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
screen.blit(end_text, (20, 60))
pygame.display.update()
time.sleep(4)

pygame.quit()

