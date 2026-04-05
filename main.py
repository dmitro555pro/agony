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
backg = transform.scale(image.load("assets/backg.png") , (1200 , 800))

class Player:
    def __init__(self, x , y):
        self.x = x
        self.y = y
        self.speed = 5
        self.gravity = 0.5
        self.on_ground = True
        self.y_vel = 5
        self.status = "idle"
        self.frame = 0
        self.frame_s = 0.2
        self.anim = {
            "idle":[idle],
            "run":[run1 , run2],
            "step":[step2 , step3],
            "crouch":[croutch0,croutch1],
            "slide":[slide]
        }
        self.image = self.anim["idle"][0]
        self.rect = self.image.get_rect(topleft=(x,y))

    def move(self,keys):
        if keys[K_d]:
            self.x += self.speed
            self.status = "step"
        elif keys[K_a]:
            self.x -= self.speed
            self.status = "step"
        else:
            self.status = "idle"

        if keys[K_LCTRL]:
            self.status = "crouch"


running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
    w.blit(backg,(0,0))
    display.update()
    clock.tick(60)