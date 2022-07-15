import pygame

pygame.font.init()

WIDTH, HEIGHT = 800, 600

ACC = 0.5
FRIC = -0.06
GRAVITY = 0.5
vec = pygame.math.Vector2

info_font = pygame.font.SysFont("Consolas", 18)


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
        self.jumping = False

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
        if pressed_keys[pygame.K_RIGHT]:
            self.acc.x = +ACC

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
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -18

    def cancel_jump(self):
        # decrease y velocity when player doesn't hold
        # the jump button
        if self.jumping and self.vel.y < -3:
            self.vel.y = -3

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

        self.info_rect.center = (self.rect.centerx, self.rect.centery - 30)
        text = f"Pos:{int(self.pos.x),int(self.pos.x)} Acc:{(self.acc.x).__format__('.2f'),(self.acc.y).__format__('.2f')} Vel:{(self.vel.x).__format__('.2f'),(self.vel.y).__format__('.2f')}"

        # self.info_surf = info_font.render(text, True, "white", "red")
