import os
import pygame

pygame.mixer.init()

sound = pygame.mixer.Sound(os.path.join("Assets", "coin.wav"))


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load(os.path.join("Assets", "yellow_coin.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (24, 24))

        self.rect = self.image.get_rect()

        self.rect.midbottom = pos

    def update(self, player):
        if self.rect.colliderect(player.rect):
            sound.play()
            player.score += 5
            self.kill()
