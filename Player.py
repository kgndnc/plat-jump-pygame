import os
import pygame

from utils import check_hi_score

pygame.font.init()

# Custom Event
PLAYER_FALL = pygame.USEREVENT + 1

WIDTH, HEIGHT = 800, 600

ACC = 0.5
FRIC = -0.06
GRAVITY = 0.5
vec = pygame.math.Vector2

info_font = pygame.font.SysFont("Consolas", 18)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("Assets", "char.png")).convert()
        self.jump_img = pygame.image.load(os.path.join("Assets", "jump.png")).convert()
        self.walk_img = [
            pygame.image.load(os.path.join("Assets", "walk.png")).convert(),
            pygame.image.load(os.path.join("Assets", "run.png")).convert(),
        ]

        # (253, 77, 211)
        self.image.set_colorkey((253, 77, 211))
        self.jump_img.set_colorkey((253, 77, 211))
        self.walk_img[0].set_colorkey((253, 77, 211))
        self.walk_img[1].set_colorkey((253, 77, 211))

        self.image = pygame.transform.scale(self.image, (48, 48))
        self.jump_img = pygame.transform.scale(self.jump_img, (48, 48))
        self.walk_img[0] = pygame.transform.scale(self.walk_img[0], (48, 48))
        self.walk_img[1] = pygame.transform.scale(self.walk_img[1], (48, 48))

        self.surf = self.image

        self.flipped_image = pygame.transform.flip(self.image, True, False)
        self.flipped_jump_img = pygame.transform.flip(self.jump_img, True, False)
        self.flipped_walk_img = [
            pygame.transform.flip(self.walk_img[0], True, False),
            pygame.transform.flip(self.walk_img[1], True, False),
        ]
        self.animation_counter = 0

        self.rect = self.image.get_rect()
        self.rect.size = [36, 48]

        # movement
        self.pos = vec((10, 385))  # (10, 385) konumunda yer alan birim vektor (konum vektoru)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.facing_right = True

        # score
        self.score = 0

        # info rect
        text = f"Pos:{int(self.pos.x),int(self.pos.x)} Acc:{(self.acc.x).__format__('.2f'),(self.acc.y).__format__('.2f')} Vel:{(self.vel.x).__format__('.2f'),(self.vel.y).__format__('.2f')}"

        self.info_surf = info_font.render(text, True, "white", "red")
        self.info_rect = self.info_surf.get_rect()
        self.info_rect.center = self.rect.centerx, self.rect.centery - 30
        # pygame.Rect(self.pos.x, self.pos.y, 40, 20)

    def move(self, group):
        # constant effect of gravity
        # constant vertical acceleration -> Gravity
        # only nullify it when player stands on firm ground (platform in this game)
        self.acc = vec(0, GRAVITY)

        pressed_keys = pygame.key.get_pressed()

        """
            Δx = ΔV . t            
            Δv = Δa . t  

            Δx = v.t  + 1/2 a . t^2 
        """

        # -                           +
        if pressed_keys[pygame.K_LEFT]:
            self.acc.x = -ACC
            self.facing_right = False
        if pressed_keys[pygame.K_RIGHT]:
            self.acc.x = +ACC
            self.facing_right = True

        # apply friction (more velocity more friction) (x-axis)
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        # equation of motion (t is unit time so it's omitted as in other equations)
        self.pos += self.vel + 0.5 * self.acc

        # screen warping
        if self.pos.x > WIDTH:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = WIDTH

        # apply the changes to the player rectangle
        self.rect.midbottom = self.pos

        # set score
        if self.vel.y < 0 and self.score < 4:
            self.score += 0.1

    def jump(self, group):
        # only jump if player is in contact with a platform
        hits = pygame.sprite.spritecollide(self, group, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -18

    def cancel_jump(self):
        # decrease y velocity when player doesn't hold
        # the jump button
        if self.jumping and self.vel.y < -2:
            self.vel.y = -2

    def draw_vel_vector(self, display_surface):
        pygame.draw.line(
            display_surface,
            "white",
            self.rect.center,
            (
                self.rect.centerx + (self.vel.x * 4 if self.vel.x != 0 else self.vel.x),
                self.rect.top + (self.vel.y * 4 if self.vel.y != 0 else self.vel.y),
            ),
            2,
        )

    def draw_acc_vector(self, display_surface):
        pygame.draw.line(
            display_surface,
            "cyan",
            self.rect.center,
            (
                (self.rect.centerx + (self.acc.x * 20 if abs(self.acc.x) >= 0.1 else self.acc.x)),
                (self.rect.top + self.acc.y + 50),
            ),
            2,
        )

    def isInGame(self):
        if self.rect.top > HEIGHT:
            pygame.event.post(pygame.event.Event(PLAYER_FALL))

    def update(self, group):
        # limit falling speed
        if self.vel.y > 10:
            self.vel.y = 10
        # Return a list containing all Sprites in a Group
        # that intersect with another Sprite(first argument).
        hits = pygame.sprite.spritecollide(self, group, False)

        # set the y velocity 0 if it was falling down
        # otherwise don't set it to 0 or else jump is nullified
        if self.vel.y > 0:
            if hits:
                # This makes sure that the “landing” isn’t registered
                # until the player’s y-position has not gone above the bottom of the platform
                if self.pos.y < hits[0].rect.bottom:
                    self.vel.y = 0
                    self.pos.y = hits[0].rect.top + 1
                    self.jumping = False

        # Check whether character's on screen
        self.isInGame()

        # flip char image

        if self.jumping:
            if self.facing_right:
                self.surf = self.jump_img
            else:
                self.surf = self.flipped_jump_img
        else:
            if abs(self.vel.x) > 1:
                if self.facing_right:
                    self.surf = self.walk_img[self.animation_counter // 15]
                    self.animation_counter += 1
                else:
                    self.surf = self.flipped_walk_img[self.animation_counter // 15]
                    self.animation_counter += 1
            else:
                if self.facing_right:
                    self.surf = self.image
                else:
                    self.surf = self.flipped_image

        if self.animation_counter >= 30:
            self.animation_counter = 0
