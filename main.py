import sys
import pygame
from pygame.locals import *
from Player import Player
import os


class platform_cs(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill("blue")
        self.rect = self.surf.get_rect(bottomleft=(0, HEIGHT))


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
P1 = Player()

# sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(PT1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

clock = pygame.time.Clock()
running = True

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

    pygame.display.set_caption(f"Game (FPS: {clock.get_fps().__format__('.2f') })")

    clock.tick(60)
