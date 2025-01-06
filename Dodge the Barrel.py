import pygame
import random


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Frames
        # Run
        self.run1 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-run-00.png"), (150, 120)).convert_alpha()
        self.run2 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-run-01.png"), (150, 120)).convert_alpha()
        self.run3 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-run-02.png"), (150, 120)).convert_alpha()
        self.run4 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-run-03.png"), (150, 120)).convert_alpha()
        self.run5 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-run-04.png"), (150, 120)).convert_alpha()
        self.run6 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-run-05.png"), (150, 120)).convert_alpha()
        # Idle
        self.idle1 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-idle-00.png"), (150, 120)).convert_alpha()
        self.idle2 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-idle-01.png"), (150, 120)).convert_alpha()
        self.idle3 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-idle-02.png"), (150, 120)).convert_alpha()
        self.idle4 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-idle-03.png"), (150, 120)).convert_alpha()
        # Jump
        self.jump1 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-jump-00.png"), (150, 120)).convert_alpha()
        self.jump2 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-jump-01.png"), (150, 120)).convert_alpha()
        self.jump3 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-jump-02.png"), (150, 120)).convert_alpha()
        self.jump4 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-jump-03.png"), (150, 120)).convert_alpha()
        # Fall
        self.fall1 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-fall-00.png"), (150, 120)).convert_alpha()
        self.fall2 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-fall-01.png"), (150, 120)).convert_alpha()
        self.fall3 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-crouch-03.png"), (150, 120)).convert_alpha()
        self.fall4 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-crouch-00.png"), (150, 120)).convert_alpha()
        self.fall5 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-crouch-03.png"), (150, 120)).convert_alpha()
        # crouch
        self.crouch1 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-crouch-00.png"), (150, 120)).convert_alpha()
        self.crouch2 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-crouch-01.png"), (150, 120)).convert_alpha()
        self.crouch3 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-crouch-02.png"), (150, 120)).convert_alpha()
        self.crouch4 = pygame.transform.scale(pygame.image.load("./Textures/adventurer-crouch-03.png"), (150, 120)).convert_alpha()

        # Lists
        # Jump/Fall
        self.frames_jump = [self.jump1, self.jump2, self.jump3, self.jump4, self.fall1, self.fall2]
        self.hit_ground = [self.fall3, self.fall4, self.fall5]
        self.frames_jump_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_jump]
        self.hit_ground_left = [pygame.transform.flip(frame, True, False) for frame in self.hit_ground]
        # Crouch
        self.frames_crouch = [self.crouch1, self.crouch2, self.crouch3, self.crouch4]
        self.frames_crouch_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_crouch]
        # Idle
        self.frames_idle = [self.idle1, self.idle2, self.idle3, self.idle4]
        self.frames_idle_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_idle]
        # Run
        self.frames_run = [self.run1, self.run2, self.run3, self.run4, self.run5, self.run6]
        self.frames_run_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_run]

        # Sounds
        self.jump_sound = pygame.mixer.Sound("./Sounds/jump2.mp3")
        self.jump_sound.set_volume(0.4)

        self.db_jump_sound = pygame.mixer.Sound("./Sounds/mixkit-cartoon-punch-2149.wav")
        self.db_jump_sound.set_volume(0.5)
        # Animation state
        self.jumping = False
        # Index/Gravity
        self.frame_index = 0
        self.gravity = 0
        self.direction = "left"
        # Main
        self.image = self.frames_idle[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(screen.get_width() / 2, 660))

    def move(self):
        global db
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 660:
            self.frame_index = 0
            self.gravity -= 20
            self.jump_sound.play()
            self.jumping = True
        if keys[pygame.K_w] and self.rect.bottom < 660 and db:
            self.frame_index = 0
            self.db_jump_sound.play()
            self.gravity = 0
            self.gravity -= 20
            db = False
        elif keys[pygame.K_d]:
            self.rect.x += 8
            self.direction = "right"
            self.play_animation("run")
        elif keys[pygame.K_a]:
            self.rect.x -= 8
            self.direction = "left"
            self.play_animation("run")
        elif keys[pygame.K_s] and self.rect.bottom == 660:
            self.play_animation("crouch")
        else:
            self.play_animation("idle")

    def collisions(self):
        if self.rect.left <= -40:
            self.rect.left = -40
        if self.rect.right >= 1280:
            self.rect.right = 1280

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 660:
            self.rect.bottom = 660
            self.gravity = 0

    def play_animation(self, type):
        # Jump
        if self.rect.bottom < 660:
            self.frame_index += 0.08
            if self.frame_index >= 5:
                self.frame_index = 0
            if self.direction == "right":
                self.image = self.frames_jump[int(self.frame_index)]
            else:
                self.image = self.frames_jump_left[int(self.frame_index)]

        # Hit_Ground
        if self.jumping and self.rect.bottom == 660:
            self.frame_index += 0.5
            if self.frame_index >= 3:
                self.frame_index = 0
                self.jumping = False
            if self.direction == "right":
                self.image = self.hit_ground[int(self.frame_index)]
            else:
                self.image = self.hit_ground_left[int(self.frame_index)]
        # Run
        elif type == "run" and self.rect.bottom == 660 and not self.jumping:
            self.frame_index += 0.2
            if self.frame_index >= 6:
                self.frame_index = 0
            if self.direction == "right":
                self.image = self.frames_run[int(self.frame_index)]
            else:
                self.image = self.frames_run_left[int(self.frame_index)]
        # Idle
        elif type == "idle" and self.rect.bottom == 660 and not self.jumping:
            self.frame_index += 0.13
            if self.frame_index >= 4:
                self.frame_index = 0
            if self.direction == "right":
                self.image = self.frames_idle[int(self.frame_index)]
            else:
                self.image = self.frames_idle_left[int(self.frame_index)]
        # Crouch
        elif type == "crouch":
            self.frame_index += 0.13
            if self.frame_index >= 4:
                self.frame_index = 0
            if self.direction == "right":
                self.image = self.frames_crouch[int(self.frame_index)]
            else:
                self.image = self.frames_crouch_left[int(self.frame_index)]

    def update(self):
        self.move()
        self.apply_gravity()
        self.collisions()


class Obstacles(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        barrel = pygame.transform.scale(pygame.image.load("./Textures/Barrel Sprite.png").convert_alpha(), (70, 80))
        explode1 = pygame.transform.scale(pygame.image.load("./Textures//biggerboom1.png").convert_alpha(), (200, 200))
        explode2 = pygame.transform.scale(pygame.image.load("./Textures/biggerboom2.png").convert_alpha(), (200, 200))
        explode3 = pygame.transform.scale(pygame.image.load("./Textures/biggerboom3.png").convert_alpha(), (200, 200))
        explode4 = pygame.transform.scale(pygame.image.load("./Textures/biggerboom4.png").convert_alpha(), (200, 200))

        self.explode = pygame.mixer.Sound("./Sounds/explode.MP3")
        self.explode.set_volume(0.2)
        self.frames = [barrel, explode1, explode2, explode3, explode4]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(0, 1240), -40))

    def update(self):
        self.rect.y += speed
        if self.rect.bottom >= 660:
            self.rect.bottom = 660
            self.frame_index += 0.2
            if self.frame_index > 4:
                self.explode.play()
                self.kill()
            self.image = self.frames[int(self.frame_index)]
            self.rect = self.image.get_rect(center=self.rect.center)


def update_score():
    run_time = round(pygame.time.get_ticks() / 1000) - start_time
    score_label = font.render(f"Score: {run_time}", False, "Black").convert_alpha()
    score_rect = score_label.get_rect(center=(screen.get_width() / 2, 150))
    screen.blit(score_label, score_rect)
    return run_time


def collision():
    global speed, db
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        speed = 5
        lost.play()
        explode = pygame.mixer.Sound("./Sounds/explode.MP3")
        explode.set_volume(0.2)
        explode.play()
        db = False
        return False
    else:
        return True


score = 0
start_time = 0
pygame.init()
screen = pygame.display.set_mode((1240, 720))
running = True
clock = pygame.time.Clock()
font = pygame.font.Font("./Textures/Pixeltype.ttf", 60)
title_font = pygame.font.Font("./Textures/Pixeltype.ttf", 80)
pygame.display.set_caption("Dodge The Barrel!")

player = pygame.sprite.GroupSingle()
player.add(Player())

music = pygame.mixer.Sound("./Sounds/barrel.mp3")
music.set_volume(0.2)


obstacle_group = pygame.sprite.Group()

title = title_font.render("Dodge the Barrel!", False, "Black")
title_rect = title.get_rect(center=(screen.get_width()/2, 240))

floor = pygame.image.load("./Textures/floor.png").convert_alpha()
floor_rect = floor.get_rect(midbottom=(screen.get_width() / 2, 720))

reset = pygame.transform.scale2x(pygame.image.load("./Textures/Restart.png").convert_alpha())
reset_rect = floor.get_rect(center=(screen.get_width()-30, screen.get_height()/2))

start = pygame.transform.scale(pygame.image.load("./Textures/start.png").convert_alpha(), (120, 120))
start_rect = floor.get_rect(center=(screen.get_width()+20, screen.get_height()/2))

lost = pygame.mixer.Sound("./Sounds/mixkit-retro-arcade-game-over-470.wav")
lost.set_volume(0.5)

cursor_image = pygame.image.load("./Textures/cross.png").convert_alpha()
pygame.mouse.set_visible(False)

db_jump = pygame.transform.scale2x(pygame.image.load("./Textures/Item__26.png"))
db_rect = db_jump.get_rect(topleft=(10, 10))

background = pygame.transform.rotozoom(pygame.image.load("./Textures/Free-Sky-with-Clouds-Background.png").convert_alpha(), 0, 1)
background_rect = background.get_rect(center=(screen.get_width()/2, screen.get_height()/2))
playing = False

db = False

speed = 5

spawn = pygame.USEREVENT + 1
pygame.time.set_timer(spawn, 1000)

db_timer = pygame.USEREVENT + 2
pygame.time.set_timer(db_timer, 8000)

difficulty = pygame.USEREVENT + 3
pygame.time.set_timer(difficulty, 10000)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if playing:
            if event.type == spawn:
                obstacle_group.add(Obstacles())

            if event.type == difficulty:
                speed += 1

            if event.type == db_timer:
                db = True

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if reset_rect.collidepoint(event.pos):
                    start_time = round(pygame.time.get_ticks() / 1000)
                    music.play(loops=-1)
                    playing = True

    if playing:
        screen.blit(background, background_rect)
        screen.blit(floor, floor_rect)
        screen.blit(cursor_image, pygame.mouse.get_pos())
        playing = collision()
        player.draw(screen)
        if db:
            screen.blit(db_jump, db_rect)
        score = update_score()
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

    else:
        music.stop()
        if score:
            score_message_surf = font.render(f"Score: {score}", False, "black").convert_alpha()
            score_message_rect = score_message_surf.get_rect(center=(screen.get_width()/2, 420))
            start_time = 0
            screen.blit(background, background_rect)
            screen.blit(title, title_rect)
            screen.blit(reset, reset_rect)
            screen.blit(score_message_surf, score_message_rect)
        else:
            start_time = 0
            screen.blit(background, background_rect)
            screen.blit(start, start_rect)
            screen.blit(title, title_rect)
            screen.blit(cursor_image, pygame.mouse.get_pos())
            
    screen.blit(cursor_image, pygame.mouse.get_pos())
    pygame.display.update()
    clock.tick(60)
