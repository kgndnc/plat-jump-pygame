import random
import sys
import pygame
from pygame.locals import *
from Player import Player
import os


class platform_cs(pygame.sprite.Sprite):
    def __init__(self, initial=False):
        super().__init__()
        # updated to handle random level generation
        self.surf = pygame.Surface((random.randint(50, 100), 12))
        self.surf.fill("blue")
        # random position
        if initial:
            self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10), random.randint(0, HEIGHT - 30)))
        else:
            # generate platforms above the screen (out of bounds) and at the top
            self.rect = self.surf.get_rect(
                center=(random.randint(0, WIDTH - 10), random.randint(-HEIGHT + 30, HEIGHT // 3 - 10))
            )


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

    for x in range(random.randint(5, 6)):
        width = random.randrange(50, 100)
        p = platform_cs()
        # p.rect.center = (random.randrange(0, WIDTH - width), random.randrange(-150, 70))
        platforms.add(p)
        all_sprites.add(p)


gen_rand_platforms()


# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    display_surface.fill("black")
    display_surface.blit(*show_time())

    for entity in all_sprites:
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

    if (len(platforms)) < 6:
        gen_rand_platforms()

    print(len(platforms))
    # ***

    pygame.display.set_caption(f"Game (FPS: {clock.get_fps().__format__('.2f') })")

    clock.tick(60)
