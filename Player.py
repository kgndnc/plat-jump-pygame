import pygame

WIDTH, HEIGHT = 800, 600

ACC = 0.5
FRIC = -0.06
GRAVITY = 0.5
vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill("green")
        self.rect = self.surf.get_rect()

        # movement
        self.pos = vec((10, 385))  # (10, 385) konumunda yer alan birim vektor (konum vektoru)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def move(self, group):
        # constant effect of gravity
        # constant vertical acceleration -> Gravity
        # only nullify it when player stands on firm ground (platform in this game)
        self.acc = vec(0, GRAVITY)

        pressed_keys = pygame.key.get_pressed()

        """
            Δx = ΔV . t
            Δv = Δa . t   

            Δx = v  + 1/2 a . t^2      
        """

        # -                           +
        if pressed_keys[pygame.K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[pygame.K_RIGHT]:
            self.acc.x = +ACC
        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_SPACE]:
            self.jump(group)

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

    def jump(self, group):
        # only jump if player is in contact with a platform
        hits = pygame.sprite.spritecollide(self, group, False)
        if hits:
            self.vel.y = -18

    def update(self, group):
        # Return a list containing all Sprites in a Group
        # that intersect with another Sprite.
        hits = pygame.sprite.spritecollide(self, group, False)

        # set the y velocity 0 if it was falling down
        # otherwise don't set it to 0 or else jump is nullified
        if self.vel.y > 0:
            if hits:
                self.vel.y = 0
                self.pos.y = hits[0].rect.top + 1
