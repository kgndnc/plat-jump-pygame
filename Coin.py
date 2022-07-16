import os
import pygame


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load(os.path.join("Assets", "yellow_coin.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (24, 24))
        # self.image.fill("red")
        self.rect = self.image.get_rect()
        # self.rect.inflate_ip(-10, -10)

        self.rect.midbottom = pos

    def update(self, player):
        if self.rect.colliderect(player.rect):
            player.score += 5
            self.kill()
