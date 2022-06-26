import random
import pygame

SCREEN_WIDTH = 270
SCREEN_HEIGHT = 270

TICK_SPEED = 32

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

meteorSpriteSize = 32


def handle_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


class Meteor:
    global meteorSprite
    meteorSprite = pygame.image.load("sprites/basic_front.png")

    global meteorSpeed
    meteorSpeed = 32

    global craterList
    craterList = []

    global shadowRadius
    shadowRadius = meteorSpriteSize / 2

    def __init__(self):
        self.pos = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        self.hitbox = pygame.Rect(self.pos[0], self.pos[1], meteorSpriteSize, meteorSpriteSize)
        self.shadowCount = -1

    def hasFallen(self):
        return self.shadowCount >= meteorSpeed

    def shadowUpdate(self, screen):
        self.shadowCount = self.shadowCount + 1

        shadowTint = 255 - (self.shadowCount * (255 / meteorSpeed))

        pygame.draw.circle(screen,
                           (shadowTint, shadowTint, shadowTint),
                           (self.pos[0] + shadowRadius, self.pos[1] + shadowRadius),
                           shadowRadius)

def main():
    pygame.init()

    meteor = Meteor()

    while handle_quit():
        clock.tick(TICK_SPEED)

        # TODO: display backdrop
        pygame.display.update()
        screen.fill((255, 255, 255))

        if meteor.hasFallen():
            craterList.append(meteor)
            meteor = Meteor()

        meteor.shadowUpdate(screen)

        for c in craterList:
            screen.blit(meteorSprite, c.pos)

        #meteor.displayShadow()


main()
