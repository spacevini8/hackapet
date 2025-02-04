import random
import displayio
import pygame
from blinka_displayio_pygamedisplay import PyGameDisplay
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
pygame.init()

class Animation:
    def __init__(self, start_frame, end_frame, ticks_per_frame, one_shot=False):
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.frame = 0
        self.ticks = 0
        self.ticks_per_frame = ticks_per_frame
        self.one_shot = one_shot

    def next_frame(self):
        if self.one_shot and self.frame == self.end_frame:
            return self.frame

        self.ticks += 1

        if self.ticks >= self.ticks_per_frame:
            self.frame += 1
            if self.frame > self.end_frame:
                self.frame = self.start_frame

            self.ticks = 0

        return self.frame

class Player:
    def __init__(self, splash, x, y):
        self.health = 1000
        self.bitmap_sheet = displayio.OnDiskBitmap('res/penguin.png')
        self.sprite = displayio.TileGrid(
            self.bitmap_sheet,
            pixel_shader=self.bitmap_sheet.pixel_shader,
            tile_width=20,
            tile_height=29,
            x=x - 20,
            y=y - 29
        )

        self.walk_animation = Animation(0, 2, 2)
        self.idle_animation = Animation(2, 4, 10)
        self.current_animation = self.idle_animation
        splash.append(self.sprite)

        self.weapon = Bazooka(splash)
        self.firing = False

    def update(self, splash):
        self.sprite[0] = self.current_animation.next_frame()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.sprite.x -= 2
            self.sprite.flip_x = True
        if keys[pygame.K_RIGHT]:
            self.sprite.x += 2
            self.sprite.flip_x = False
        if keys[pygame.K_UP] and not self.firing:
            self.weapon.fire(splash, int((self.sprite.flip_x - 0.5) * -10), 0)
            self.firing = True

        if not keys[pygame.K_UP]:
            self.firing = False

        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.current_animation = self.idle_animation
        else:
            self.current_animation = self.walk_animation

        self.weapon.sprite.x = int(self.sprite.x - self.weapon.bitmap.width // 2 + self.sprite.tile_width // 2 + (self.sprite.flip_x - 0.5) * 2 * -5)
        self.weapon.sprite.y = self.sprite.y + 10
        self.weapon.sprite.flip_x = self.sprite.flip_x

        self.weapon.update()


class Weapon:
    def __init__(self, splash, damage, bitmap, width, height):
        self.damage = damage
        self.bitmap = bitmap
        self.sprite = displayio.TileGrid(
            self.bitmap,
            pixel_shader=self.bitmap.pixel_shader,
            tile_width=width,
            tile_height=height,
        )

        splash.append(self.sprite)
        self.bullets = []

    def fire(self, splash, vel_x, vel_y):
        pass

class Bullet:
    def __init__(self, splash, x, y, x_vel, y_vel, bitmap, width, height):
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.bitmap = bitmap
        self.detonated = False
        self.sprite = displayio.TileGrid(
            bitmap,
            pixel_shader=bitmap.pixel_shader,
            tile_width=width,
            tile_height=height,
            x=x,
            y=y
        )

        splash.append(self.sprite)

    def update(self):
        pass

class Rocket(Bullet):
    def __init__(self, splash, x, y, x_vel, y_vel):
        super().__init__(splash, x, y, x_vel, y_vel, displayio.OnDiskBitmap('res/rocket.png'), 12, 8)

        self.sprite.flip_x = self.x_vel < 0
        splash.append(self.sprite)

    def update(self):
        self.sprite.x += self.x_vel
        self.sprite.y += self.y_vel


class Bazooka(Weapon):
    def __init__(self, splash):
        super().__init__(splash, 50, displayio.OnDiskBitmap('res/bazooka-lowres.png'), 28, 10)

    def update(self):
        for bullet in self.bullets:
            bullet.update()

        new_bullets = []
        for bullet in self.bullets:
            if not bullet.detonated and 0 < bullet.sprite.x < screen_width:
                new_bullets.append(bullet)
            else:
                splash.remove(bullet.sprite)
                # why is this not removing, whatever
                bullet.sprite.x = -100

        self.bullets = new_bullets

    def fire(self, splash, vel_x, vel_y):
        self.bullets.append(Rocket(splash, self.sprite.x, self.sprite.y, vel_x, vel_y))


class Enemy:
    def __init__(self, health, damage):
        self.health = health
        self.damage = damage
        self.dead = False

    def update(self, splash, player):
        pass

class Zombie(Enemy):
    def __init__(self, splash, x, y):
        super().__init__(50, 20)

        self.bitmap_sheet = displayio.OnDiskBitmap('res/zombie.png')
        self.sprite = displayio.TileGrid(
            self.bitmap_sheet,
            pixel_shader=self.bitmap_sheet.pixel_shader,
            tile_width=20,
            tile_height=29,
            default_tile=0,
            x=x - 20,
            y=y - 29
        )

        splash.append(self.sprite)
        self.attack_ticks = 0
        self.ticks_per_attack = 20

        self.walk_animation = Animation(0, 2, 2)
        self.death_animation = Animation(3, 7, 3, one_shot=True)
        self.current_animation = self.walk_animation

    def update(self, splash, player):
        self.sprite[0] = self.current_animation.next_frame()

        if self.dead:
            return

        for bullet in player.weapon.bullets:
            if abs(bullet.sprite.x + bullet.bitmap.width // 2 - self.sprite.x - self.sprite.tile_width // 2) < 10:
                self.health -= player.weapon.damage
                bullet.detonated = True

        if self.health <= 0:
            self.dead = True
            self.current_animation = self.death_animation

        if abs(self.sprite.x - player.sprite.x) < 18:
            self.attack_ticks += 1
            if self.attack_ticks > self.ticks_per_attack:
                self.attack_ticks = 0
                player.health -= 10

            return

        self.attack_ticks = 0
        if self.sprite.x - player.sprite.x > 0:
            self.sprite.x -= 1
            self.sprite.flip_x = True
        else:
            self.sprite.x += 1
            self.sprite.flip_x = False

class World:
    def __init__(self, splash):
        self.ground_bitmap = displayio.OnDiskBitmap('res/ground.png')
        self.ground_y = screen_height - 32
        self.ground_sprite = displayio.TileGrid(
            self.ground_bitmap,
            pixel_shader=self.ground_bitmap.pixel_shader,
            tile_width=128,
            tile_height=32,
            default_tile=0,
            x=0,
            y=self.ground_y
        )

        splash.append(self.ground_sprite)

        self.background_bitmap = displayio.OnDiskBitmap('res/background.png')
        self.background_sprite = displayio.TileGrid(
            self.background_bitmap,
            pixel_shader=self.background_bitmap.pixel_shader,
            tile_width=128,
            tile_height=96,
            default_tile=0,
            x=0,
            y=0
        )

        splash.append(self.background_sprite)

        self.player = Player(splash, screen_width // 2, self.ground_y)
        self.player_health_label = label.Label(bitmap_font.load_font('res/pixelade-8px.bdf'), text='Health: ', color=0x0ab2e, x=5, y=10)
        splash.append(self.player_health_label)
        self.enemies = []

        self.spawn_enemy_ticks = 0
        self.ticks_per_spawn_enemy = 200
        self.add_enemy(random.randint(0, 1) * screen_width, self.ground_y)

    def add_enemy(self, x, y):
        self.enemies.append(Zombie(splash, x, y))

    def update(self, splash):
        self.player.update(splash)
        self.player_health_label.text = f'HP: {self.player.health}'
        for enemy in self.enemies:
            enemy.update(splash, self.player)

        self.spawn_enemy_ticks += 1
        if self.spawn_enemy_ticks >= self.ticks_per_spawn_enemy:
            self.spawn_enemy_ticks = 0
            self.add_enemy(random.randint(0, 1) * screen_width, self.ground_y)
            self.ticks_per_spawn_enemy *= 0.95
            self.ticks_per_spawn_enemy = max(50, self.ticks_per_spawn_enemy)

        if self.player.health <= 0:
            exit()


screen_width = screen_height = 128
display = PyGameDisplay(width=screen_width, height=screen_height)
splash = displayio.Group()
display.show(splash)


world = World(splash)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    world.update(splash)
    clock.tick(30)