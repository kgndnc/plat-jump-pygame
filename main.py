import random
import sys
import pygame
from pygame.locals import *
from Player import Player
import os


class platform_cs(pygame.sprite.Sprite):
    def __init__(self, initial=False):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50, 100), 12))
        self.surf.fill("blue")
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10), random.randint(0, HEIGHT - 30)))


# Constants
WIDTH, HEIGHT = 800, 600
# physics
ACC = 0.5
FRIC = -0.12
vec = pygame.math.Vector2

# init pygame
pygame.init()
pygame.font.init()
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mouse.set_cursor(pygame.cursors.Cursor(SYSTEM_CURSOR_HAND))
pygame.display.set_caption("Game")

time_font = pygame.font.SysFont("Consolas", 26)
info_font = pygame.font.SysFont("Consolas", 20)


def show_time():
    milliseconds = pygame.time.get_ticks()
    seconds = milliseconds // 1000
    minutes = seconds // 60
    seconds -= minutes * 60

    time_surf = time_font.render(
        f"{minutes} {'min' if minutes==1 else 'mins'} {seconds} {'second' if seconds==1 else 'seconds'}",
        1,
        "Green",
    )
    time_rect = time_surf.get_rect()

    time_rect.midtop = (WIDTH // 2, 10)

    return time_surf, time_rect


def draw_lines():
    if pygame.mouse.get_focused():
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.aaline(display_surface, "white", (0, 0), mouse_pos)
        pygame.draw.aaline(display_surface, "purple", (0, display_surface.get_height()), mouse_pos)
        pygame.draw.aaline(display_surface, "yellow", (display_surface.get_width(), 0), mouse_pos)
        pygame.draw.aaline(
            display_surface, "pink", (display_surface.get_width(), display_surface.get_height()), mouse_pos
        )


# Instantiate entities
PT1 = platform_cs()
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255, 0, 0))
PT1.rect = PT1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))

P1 = Player()

# sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(PT1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

clock = pygame.time.Clock()
running = True

# initial random platforms
for x in range(random.randint(5, 6)):
    pl = platform_cs(initial=True)
    platforms.add(pl)
    all_sprites.add(pl)


def gen_rand_platforms():
    """
    another approach implement if you want
    - find the top platform
    - set a lower boundary for the new platform that is above this
    - check to make sure that the lower boundary is off the screen (above what is visible)
    - set an upper boundry that is close enough to the top platform that P1 can jump to it
    - choose a random position between the lower bound and the upper bound
    """

    while len(platforms) < 7:
        width = random.randrange(50, 100)
        p = platform_cs()
        p.rect.center = (random.randrange(0, WIDTH - width), random.randrange(-50, 0))
        platforms.add(p)
        all_sprites.add(p)


gen_rand_platforms()


# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                P1.jump(platforms)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                P1.cancel_jump()

    display_surface.fill("black")
    display_surface.blit(*show_time())

    # P1.move(platforms)
    # P1.update(platforms)

    for entity in all_sprites:
        if isinstance(entity, Player):
            display_surface.blit(entity.surf, entity.rect)
            # display_surface.blit(entity.info_surf, entity.info_rect)

            # velocity vector
            entity.draw_vel_vector(display_surface)

            # acc vector
            entity.draw_acc_vector(display_surface)
        else:
            display_surface.blit(entity.surf, entity.rect)

    P1.move(platforms)
    P1.update(platforms)

    pygame.display.update()

    # ***
    if P1.rect.top <= HEIGHT // 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()

    if (len(platforms)) < 7:
        gen_rand_platforms()

    # ***

    pygame.display.set_caption(f"Game (FPS: {clock.get_fps().__format__('.2f') })")

    clock.tick(60)
