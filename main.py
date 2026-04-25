from pygame import*

init()
w = display.set_mode((1200, 800))
display.set_caption("agony")
clock = time.Clock()
croutch0 = transform.scale(image.load("assets/player/croutch_0.png") , (70 , 40))
croutch1 = transform.scale(image.load("assets/player/croutch_1.png") , (70 , 40))
idle = transform.scale(image.load("assets/player/idle or step 0.png") , (20 , 100))
step2 = transform.scale(image.load("assets/player/step 1.png") , (50 , 100))
step3 = transform.scale(image.load("assets/player/step 2.png") , (50 , 100))
run1 = transform.scale(image.load("assets/player/running 0.png") , (80 , 100))
run2 = transform.scale(image.load("assets/player/running 1.png") , (80 , 100))
slide = transform.scale(image.load("assets/player/sliding.png") , (80 , 40))
ground = 650
class Player:
    def __init__(self, x , y):
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
            "idle":[idle],
            "run":[run1 , run2],
            "step":[step2 , step3],
            "crouch":[croutch0,croutch0,croutch1,croutch1],
            "idle_crouch":[croutch0],
            "slide":[slide]
        }
        self.image = self.anim["idle"][0]
        self.rect = self.image.get_rect(topleft=(x,y))
        self.flip = False

    def move(self,keys):
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
        elif not moving:
            self.status = "idle"

        if  keys[K_LCTRL] and not moving:
            self.status = "idle_crouch"
        elif keys[K_LCTRL] and moving:
            self.status = "crouch"
            self.speed = 2.5
        elif keys[K_LSHIFT] and moving:
            self.status = "run"
            self.speed = 10

        if keys[K_LCTRL] and keys[K_LSHIFT]:
            self.status = "slide"
            if self.flip:
                for i in range(30):
                    self.x -= 1
            else:
                for i in range(30):
                    self.x += 1

        if keys[K_SPACE] and self.on_ground:
            self.y_vel = -10
            self.on_ground = False

    def grav(self):
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
        self.rect.topleft = (self.x , self.y)

    def draw(self , surface):
        img = transform.flip(self.image , self.flip , False)
        surface.blit(img , self.rect)
import random


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 40
        self.alive = True
        self.act = random.choice(["step", "run", "crouch", "jump", "slide"])
        self.rect = Rect(self.x, self.y, self.size, self.size)

        self.spawn_time = time.get_ticks()  # час появи
        self.attack_started = False

    def update(self, pl):
        if not self.alive:
            return

        now = time.get_ticks()

        if not self.attack_started and now - self.spawn_time > 1000:
            self.attack_started = True
            print("Ворог атакує! Треба:", self.act)

        if self.attack_started:
            if pl.status == self.act:
                print("✔ Ти врятувався")
                self.alive = False
            else:

                if now - self.spawn_time > 1500:
                    print("❌ Ти не зробив дію:", self.act)
                    self.alive = False

    def draw(self, surface):
        if self.alive:
            color = (255, 0, 0) if not self.attack_started else (255, 100, 100)
            draw.rect(surface, color, self.rect)

oleg = Player(100 , 650)
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
    w.fill((0,0,255))
    draw.rect(w ,(0,255,0) , (0 , 750 , 1200 , 50))
    oleg.draw(w)
    display.update()
    clock.tick(60)
