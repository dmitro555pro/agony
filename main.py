from pygame import *
import random

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

bg = transform.scale(image.load("assets/New Piskel-1.png.png"), (90, 80))
close = transform.scale(image.load("assets/New Piskel (68).png"), (45, 40))

went = transform.scale(image.load("assets/New Piskel-1.png (1).png"), (100, 100))
open = transform.scale(image.load("assets/New Piskel-2.png.png"), (100, 100))

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

        if keys[K_LCTRL] and keys[K_LSHIFT] and moving:
            self.status = "slide"
            if self.sl_sp > 5:
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
            if self.status == "slide":
                self.speed = 12

    def grav(self):
        global keys

        current_ground = ground + 60 if keys[K_LCTRL] else ground

        if self.y < current_ground:
            self.on_ground = False

        if not self.on_ground:
            self.y_vel += self.gravity
            self.y += self.y_vel

        if self.y >= current_ground:
            self.y = current_ground
            self.y_vel = 0
            self.on_ground = True

    def animation(self):
        frames = self.anim[self.status]
        self.frame += self.frame_s

        if self.frame >= len(frames):
            self.frame = 0

        self.image = frames[int(self.frame)]

    def platform_collide(self, platforms):
        was_on_platform = False

        for pl in platforms:
            if self.rect.colliderect(pl.rect):
                if self.y_vel > 0 and self.rect.bottom <= pl.rect.top + 15:
                    self.rect.bottom = pl.rect.top
                    self.y = self.rect.y
                    self.y_vel = 0
                    self.on_ground = True
                    was_on_platform = True

                elif self.y_vel < 0 and self.rect.top >= pl.rect.bottom - 15:
                    self.rect.top = pl.rect.bottom
                    self.y = self.rect.y
                    self.y_vel = 0

                if self.rect.colliderect(pl.rect):
                    if not was_on_platform:
                        if self.flip:
                            self.rect.left = pl.rect.right
                        else:
                            self.rect.right = pl.rect.left
                        self.x = self.rect.x

    def update(self):
        self.rect.topleft = (self.x, self.y)
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()

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
        global game_over
        if not self.alive:
            return

        self.x = camera_x + self.x_p
        now = time.get_ticks()

        if not self.attack_started and now - self.spawn_time > 1000:
            self.attack_started = True
            self.image = self.attack_image

        if self.attack_started:
            if pl.status == self.act:
                print("enemy defeated")
                self.alive = False

            elif now - self.spawn_time > 1500:
                print("player failed")
                game_over = True
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
        self.platforms = []

    def check(self, player):
        if self.x1 <= player.x <= self.x2:
            if not self.spawned:
                self.spawn()
                self.spawned = True

    def spawn(self):
        if random.randint(0,2) == 1:
            self.enemies.append(Enemy())
        for i in range(2):
            x_pl = random.randint(self.x1+200 , self.x2-200)
            y_pl = random.choice([630 , 710 ])
            self.platforms.append(Platform(x_pl , y_pl , 135 , 40))


    def update(self, player, camera_x):
        for e in self.enemies:
            e.update(player, camera_x)

    def draw(self, surface, camera_x):

        for e in self.enemies:
            e.draw(surface, camera_x)
        for pl in self.platforms:
            for i in range(3):
                surface.blit(close, (pl.rect.x - camera_x + (i * 45), pl.rect.y))


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

        img = open if self.completed else went
        w.blit(img,(self.finish_x - camera_x , 650))


class Platform:
    def __init__(self , x , y , w , h):
        self.rect = rect.Rect(x , y , w , h)

    def draw(self , surface , camera_x):
        draw.rect(surface ,(255,255,255) , (self.rect.x - camera_x , self.rect.y , self.rect.width , self.rect.height))


oleg = Player(100, 650)
level = Level()
tim = 0
tim_font = font.SysFont("Arial" , 50)
w_font = font.SysFont("Arial" , 100)
running = True
game_over = False
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
    tim +=1
    keys = key.get_pressed()

    if tim >= (60*45):
        game_over = True

    text_tim = tim_font.render(str(45-tim//60), True, (255,255,255))

    oleg.move(keys)
    oleg.grav()
    oleg.animation()
    oleg.update()

    all_platforms = []
    for r in level.rooms:
        all_platforms.extend(r.platforms)

    oleg.platform_collide(all_platforms)
    oleg.update()

    camera_x = oleg.x - 600

    if camera_x < 0:
        camera_x = 0

    if camera_x > 19500:
        camera_x = 19500

    level.update(oleg, camera_x)

    for x in range(0,20800,90):
        for y in range(0 , 800 , 80):
            w.blit(bg, (x-camera_x,y))



    w.blit(text_tim, (1000, 0))

    draw.rect(w, (0, 255, 0), (0 - camera_x, 750, 21000, 50))

    level.draw(w, camera_x)
    oleg.draw(w, camera_x)

    if game_over:
        w.blit(ms_k_3,(0,0))

    display.update()
    clock.tick(60)
