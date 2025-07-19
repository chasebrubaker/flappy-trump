import pygame
import random

import os

# Init
pygame.init()

# Screen
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy  Trump")

# Load images
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
# BIRD_IMG = pygame.image.load(os.path.join(ASSETS_DIR, "bird.png")).convert_alpha()
PIPE_IMG = pygame.image.load(os.path.join(ASSETS_DIR, "pipe.png")).convert_alpha()
BG_COLOR = (135, 206, 250)

# Load sounds
flap_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "flap.wav"))
# hit_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "hit.wav"))
point_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "point.wav"))


# Constants
GRAVITY = 1000     # pixels per second squared
FLAP_POWER = -300  # pixels per second
PIPE_GAP = 150
PIPE_FREQ = 1500   # milliseconds

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_normal = pygame.image.load(os.path.join(ASSETS_DIR, "bird.png")).convert_alpha()
        self.image_hit = pygame.image.load(os.path.join(ASSETS_DIR, "bird_hit.png")).convert_alpha()
        self.base_image = self.image_normal
        self.image = self.base_image
        self.rect = self.image.get_rect(center=(100, HEIGHT // 2))
        self.vel = 0
        self.hit = False
        self.angle = 0  # degrees
        self.rotation_speed = 300  # degrees per second

    def update(self, dt):
        if not self.hit:
            self.vel += GRAVITY * dt
            self.rect.y += self.vel * dt
        else:
            self.vel += GRAVITY * dt * 2
            self.rect.y += self.vel * dt
            self.angle = min(self.angle + self.rotation_speed * dt, 90)

        # Apply rotation (whether hit or not)
        rotated = pygame.transform.rotate(self.base_image, -self.angle)
        old_center = self.rect.center
        self.image = rotated
        self.rect = self.image.get_rect(center=old_center)

    def flap(self):
        if not self.hit:
            self.vel = FLAP_POWER
            self.angle = -20  # quick upward tilt on flap

    def on_hit(self):
        if not self.hit:
            self.hit = True
            self.base_image = self.image_hit
            self.angle = 0  # reset rotation angle



# Pipe Sprite
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, flipped=False):
        super().__init__()
        self.image = pygame.transform.flip(PIPE_IMG, False, flipped) if flipped else PIPE_IMG
        self.rect = self.image.get_rect(midtop=(x, y) if not flipped else (x, y - self.image.get_height()))

    def update(self, dt):
        self.rect.x -= int(200 * dt)  # move left

# Sprite groups
bird = Bird()
all_sprites = pygame.sprite.Group(bird)
pipes = pygame.sprite.Group()

# Pipe timer
pygame.time.set_timer(pygame.USEREVENT, PIPE_FREQ)

score = 0
running = True
last_time = pygame.time.get_ticks()

while running:
    now = pygame.time.get_ticks()
    dt = (now - last_time) / 1000.0  # seconds since last frame
    last_time = now

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.flap()
            flap_sound.play()
        if event.type == pygame.USEREVENT:
            pipe_height = random.randint(100, 400)
            top = Pipe(WIDTH, pipe_height - PIPE_GAP // 2, True)
            bottom = Pipe(WIDTH, pipe_height + PIPE_GAP // 2, False)
            pipes.add(top, bottom)
            all_sprites.add(top, bottom)

    all_sprites.update(dt)

    # Check collision
    if not bird.hit and (pygame.sprite.spritecollideany(bird, pipes) or bird.rect.top <= 0 or bird.rect.bottom >= HEIGHT):
        bird.on_hit()
        pause_timer = pygame.time.get_ticks() + 750  # Pause for 750ms

    if bird.hit and pygame.time.get_ticks() >= pause_timer:
        running = False


    # Score: count pipes that go off screen
    for pipe in list(pipes):  
        if pipe.rect.right < 0:
            pipes.remove(pipe)
            all_sprites.remove(pipe)
            score += 0.5  # each pipe pair adds 1
            point_sound.play()

    # Draw
    screen.fill(BG_COLOR)
    all_sprites.draw(screen)

    score_text = font.render(f"Score: {int(score)}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
