from pygame import *
import random

from sympy.polys.groebnertools import is_reduced

init()
w = display.set_mode((1200, 800))
display.set_caption("agony")
clock = time.Clock()

croutch0 = transform.scale(image.load("assets/player/croutch_0.png"), (70, 40))
croutch1 = transform.scale(image.load("assets/player/croutch_1.png"), (70, 40))
idle = transform.scale(image.load("assets/player/idle or step 0.png"), (20, 100))
step2 = transform.scale(image.load("assets/player/step 1.png"), (50, 100))
step3 = transform.scale(image.load("assets/player/step 2.png"), (50, 100))
run1 = transform.scale(image.load("assets/player/running 0.png"), (80, 100))
run2 = transform.scale(image.load("assets/player/running 1.png"), (80, 100))
slide = transform.scale(image.load("assets/player/sliding.png"), (80, 40))
bg = transform.scale(image.load("assets/New Piskel-1.png.png"), (45, 40))
ms_d_1 = transform.scale(image.load("assets/ms/dozer/buldozer_1.png"), (400, 400))
ms_d_2 = transform.scale(image.load("assets/ms/dozer/buldozer_2.png"), (400, 400))
ms_d_3 = transform.scale(image.load("assets/ms/dozer/buldozer_3000XXXLLL.png"), (400, 400))
ms_i_1 = transform.scale(image.load("assets/ms/ire/hello just jump.png"), (400, 400))
ms_i_2 = transform.scale(image.load("assets/ms/ire/have you jump.png"), (400, 400))
ms_i_3 = transform.scale(image.load("assets/ms/ire/you don`t jump.png"), (400, 400))
ms_k_1 = transform.scale(image.load("assets/ms/koo koo/any items-1.png.png"), (400, 400))
ms_k_2 = transform.scale(image.load("assets/ms/koo koo/any items-1.png (1).png"), (400, 400))
ms_k_3 = transform.scale(image.load("assets/ms/koo koo/give me this item.png"), (1200, 800))
ms_l_1 = transform.scale(image.load("assets/ms/litany/where are you-1.png.png"), (400, 400))
ms_l_2 = transform.scale(image.load("assets/ms/litany/where are you-2.png.png"), (400, 400))
ms_l_3 = transform.scale(image.load("assets/ms/litany/why didn`t you listen.png"), (400, 400))

ground = 650
keys = None


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.gravity = 0.5
        self.on_ground = True
        self.y_vel = 0
        self.status = "idle"
        self.frame = 0
        self.frame_s = 0.2
        self.anim = {
            "idle": [idle],
            "run": [run1, run2],
            "step": [step2, step3],
            "crouch": [croutch0, croutch0, croutch1, croutch1],
            "idle_crouch": [croutch0],
            "slide": [slide]
        }
        self.image = self.anim["idle"][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.flip = False
        self.sl_sp = 0

    def move(self, keys):
        moving = False

        if keys[K_d]:
            self.x += self.speed
            self.status = "step"
            moving = True
            self.flip = False

        if keys[K_a]:
            self.x -= self.speed
            self.status = "step"
            moving = True
            self.flip = True

        if moving:
            self.speed = 5
        else:
            self.status = "idle"

        if keys[K_LCTRL] and not moving:
            self.status = "idle_crouch"

        elif keys[K_LCTRL] and moving:
            self.status = "crouch"
            self.speed = 2.5

        elif keys[K_LSHIFT] and moving:
            self.status = "run"
            self.speed = 10

        if keys[K_LCTRL] and keys[K_LSHIFT]:
            self.status = "slide"
            self.sl_sp *= 0.98

            if self.flip:
                self.x -= self.sl_sp
            else:
                self.x += self.sl_sp
        else:
            self.sl_sp = 20

        if keys[K_SPACE] and self.on_ground:
            self.y_vel = -10
            self.on_ground = False

    def grav(self):
        global keys

        self.y_vel += self.gravity
        self.y += self.y_vel

        if self.y >= ground and not keys[K_LCTRL]:
            self.y = ground
            self.y_vel = 0
            self.on_ground = True

        elif self.y >= ground and keys[K_LCTRL]:
            self.y = ground + 60
            self.y_vel = 0
            self.on_ground = True

    def animation(self):
        frames = self.anim[self.status]
        self.frame += self.frame_s

        if self.frame >= len(frames):
            self.frame = 0

        self.image = frames[int(self.frame)]

    def update(self):
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface, camera_x):
        img = transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - camera_x, self.rect.y))


class Enemy:
    def __init__(self):
        self.x_p = random.randint(0, 800)
        self.y = random.randint(0, 400)

        self.alive = True
        self.act = random.choice(["idle", "run", "idle_crouch", "slide"])

        if self.act == "idle":
            self.idle_image = ms_k_1
            self.attack_image = ms_k_2

        elif self.act == "run":
            self.idle_image = ms_i_1
            self.attack_image = ms_i_2

        elif self.act == "idle_crouch":
            self.idle_image = ms_d_1
            self.attack_image = ms_d_2

        else:
            self.idle_image = ms_l_1
            self.attack_image = ms_l_2

        self.image = self.idle_image
        self.spawn_time = time.get_ticks()
        self.attack_started = False
        self.x = 0

    def update(self, pl, camera_x):
        if not self.alive:
            return

        self.x = camera_x + self.x_p
        now = time.get_ticks()

        # через 1 секунду починає атаку
        if not self.attack_started and now - self.spawn_time > 1000:
            self.attack_started = True
            self.image = self.attack_image

        if self.attack_started:
            if pl.status == self.act:
                print("enemy defeated")
                self.alive = False

            elif now - self.spawn_time > 1500:
                print("player failed")
                self.alive = False

    def draw(self, surface, camera_x):
        if self.alive:
            surface.blit(self.image, (self.x - camera_x, self.y))


class Room:
    def __init__(self, x1, x2):
        self.x1 = x1
        self.x2 = x2
        self.spawned = False
        self.enemies = []

    def check(self, player):
        if self.x1 <= player.x <= self.x2:
            if not self.spawned:
                self.spawn()
                self.spawned = True

    def spawn(self):
        self.enemies.append(Enemy())

    def update(self, player, camera_x):
        for e in self.enemies:
            e.update(player, camera_x)

    def draw(self, surface, camera_x):
        draw.rect(surface, (0, 0, 0),
                  (self.x1 - camera_x, 600, self.x2 - self.x1, 10))

        for e in self.enemies:
            e.draw(surface, camera_x)


class Level:
    def __init__(self):
        self.rooms = []

        for i in range(20):
            self.rooms.append(Room((i * 1000), ((i + 1) * 1000)))

        self.finish_x = 19900
        self.completed = False

    def update(self, player, camera_x):
        for r in self.rooms:
            r.check(player)
            r.update(player, camera_x)

        all_dead = True

        for r in self.rooms:
            for e in r.enemies:
                if e.alive:
                    all_dead = False

        if all_dead and player.x >= self.finish_x:
            self.completed = True

    def draw(self, surface, camera_x):
        for r in self.rooms:
            r.draw(surface, camera_x)

        color = (0, 255, 0) if self.completed else (100, 0, 0)
        draw.rect(surface, color,
                  (self.finish_x - camera_x, ground - 100, 50, 100))


oleg = Player(100, 650)
level = Level()

running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    keys = key.get_pressed()

    oleg.move(keys)
    oleg.grav()
    oleg.animation()
    oleg.update()

    camera_x = oleg.x - 600

    if camera_x < 0:
        camera_x = 0

    if camera_x > 19500:
        camera_x = 19500

    level.update(oleg, camera_x)

    w.fill((0, 0, 255))

    draw.rect(w, (0, 255, 0), (0 - camera_x, 750, 21000, 50))

    level.draw(w, camera_x)
    oleg.draw(w, camera_x)

    display.update()
    clock.tick(60)
