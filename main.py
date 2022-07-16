from platform import python_branch
import random
import sys
import time
import pygame
from pygame.locals import *
from Coin import Coin
from Player import PLAYER_FALL, Player
import os

from utils import check_hi_score, read_hi_scores


class platform_cs(pygame.sprite.Sprite):
    def __init__(self, initial=False):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50, 100), 12))
        self.surf.fill("blue")
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10), random.randint(0, HEIGHT - 30)))

        # moving platform
        self.speed_quo = random.randint(1, 2)
        self.speed = random.choice([-1, 0, 0, 0, 1])
        if self.speed != 0:
            self.speed *= self.speed_quo

        self.moving = True

    def move(self, player):
        hits = self.rect.colliderect(player.rect)
        if self.moving == True:
            self.rect.move_ip(self.speed, 0)
            # positioning on moving platforms
            if hits:
                player.pos += (self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH

    def generateCoin(self):
        if self.speed == 0:
            global coins
            coins.add(Coin((self.rect.centerx, self.rect.centery - 10)))


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
pygame.mouse.set_visible(False)
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


def show_score(score):
    score_surf = time_font.render(
        f"Score: {int(score)}",
        1,
        "Green",
    )
    score_rect = score_surf.get_rect()

    score_rect.midtop = (WIDTH // 2, 10)

    return score_surf, score_rect


def show_count(platforms):
    global text
    text = f"Platform count: {len(platforms)}"
    count_surf = info_font.render(text, True, "white", "red")
    count_rect = count_surf.get_rect()
    count_rect.topleft = (0, 0)
    display_surface.blit(count_surf, count_rect)


def gen_rand_platforms(platforms, all_sprites):
    # list of platforms then add

    platform_list = []

    # generate 7 platforms
    for i in range(0, 7):
        p = platform_cs()

        # make sure they're off screen (you'll most likely change y value of -50 because it may cause infinite loop)
        p.rect.center = (random.randrange(0, WIDTH - 30), random.randrange(-30, 0))

        if i > 0:
            prev_plat = platform_list[i - 1]
            prev_platx = prev_plat.rect.x
            prev_platy = prev_plat.rect.y
            y_range = prev_platy - 180, prev_platy - 100

            p.rect.center = (random.randrange(0, WIDTH - 20), random.randrange(*y_range))

        else:
            # get the top platform of previous platforms
            prev_plat = platforms.sprites()[-1]

            prev_plat.surf.fill("maroon")

            prev_platx = prev_plat.rect.x
            prev_platy = prev_plat.rect.y
            y_range = prev_platy - 90, prev_platy - 30

            p.rect.center = (random.randrange(0, WIDTH - 20), random.randrange(*y_range))

        p.generateCoin()
        platform_list.append(p)

    all_sprites.add(platform_list)
    platforms.add(platform_list)


def start_screen(isHiScore: bool, score):
    text = "Press 'space' to start"
    start_text = time_font.render(text, 1, "white")
    space_pos = 0

    start_text_rect = start_text.get_rect(center=(WIDTH // 2, (HEIGHT * 2) // 3 + 50))

    pygame.draw.rect(display_surface, "black", (0, 40, WIDTH, HEIGHT), 0, 4)
    pygame.draw.rect(display_surface, "purple", start_text_rect.inflate(120, 90), 0, 4)

    hiScores = read_hi_scores()
    x, y = WIDTH // 2, 80
    if isHiScore:
        score_index = hiScores.index(int(score))
        for line_index, line in enumerate(hiScores):

            color = "orange" if line_index == score_index else "purple"

            hi_text = f"{line_index+1}. {line}"
            hi_text_surf = time_font.render(hi_text, 1, color, "black")
            hi_text_rect = hi_text_surf.get_rect(center=(x, y))

            display_surface.blit(hi_text_surf, hi_text_rect)
            y += 30

        y += 50
        text = "HI-SCORE!!!"
        hi_text_surf = time_font.render(text, 1, "white")
        hi_text_rect = hi_text_surf.get_rect(center=(x, y))
        display_surface.blit(hi_text_surf, hi_text_rect)

        space_pos = (start_text_rect.left, start_text_rect.top + 20)

    space_pos = space_pos if not space_pos == 0 else start_text_rect.topleft

    display_surface.blit(start_text, space_pos)

    pygame.display.update()

    global clock
    clock = pygame.time.Clock()

    loop = True

    while loop:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    loop = False
                    break

        clock.tick(60)


def main():

    # Instantiate entities
    PT1 = platform_cs()
    PT1.surf = pygame.Surface((WIDTH, 20))
    PT1.surf.fill((255, 0, 0))
    PT1.rect = PT1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))
    PT1.moving = False

    P1 = Player()
    hi_score_achieved = False

    # sprite groups
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(PT1)

    platforms = pygame.sprite.Group()
    platforms.add(PT1)

    global coins
    coins = pygame.sprite.Group()

    clock = pygame.time.Clock()
    running = True

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
            if event.type == PLAYER_FALL:
                player_score = int(P1.score)
                hi_score_achieved = check_hi_score(player_score)
                running = False
                break

        display_surface.fill("black")
        display_surface.blit(*show_score(P1.score))

        for entity in all_sprites:
            if isinstance(entity, Player):
                display_surface.blit(entity.surf, entity.rect)
                # pos, acc, vel values
                # display_surface.blit(entity.info_surf, entity.info_rect)

                # velocity vector
                entity.draw_vel_vector(display_surface)

                # acc vector
                entity.draw_acc_vector(display_surface)
            else:
                entity.move(player=P1)
                display_surface.blit(entity.surf, entity.rect)

        for coin in coins:
            display_surface.blit(coin.image, coin.rect)
            coin.update(P1)

        P1.move(platforms)
        P1.update(platforms)

        show_count(platforms)

        pygame.display.update()

        # ***
        # Screen scroll
        if P1.rect.top <= HEIGHT // 3:
            P1.pos.y += abs(P1.vel.y)
            P1.score += 0.1
            for plat in platforms:
                plat.rect.y += abs(P1.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()

            for coin in coins:
                coin.rect.centery += abs(P1.vel.y)

        if (len(platforms)) < 7:
            gen_rand_platforms(platforms, all_sprites)

        # ***

        pygame.display.set_caption(f"Game (FPS: {clock.get_fps().__format__('.2f') })")

        if not running:
            start_screen(hi_score_achieved, player_score)
            main()

        clock.tick(60)


if __name__ == "__main__":
    main()
