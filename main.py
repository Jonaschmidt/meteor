'''
created by Jonas Schmidt on 6/26/2022
'''

import random
import pygame
from pygame.locals import *

# TODO: find a good screen ratio
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 320

# TODO: find a good FPS
FPS = 32

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption("Meteor!")
pygame.display.set_icon(pygame.image.load("sprites/meteor_icon.png"))

# TODO: get these values from the file automatically as opposed to assigning it manually?
meteorSpriteSize = 32
playerSpriteSize = 32

menuButtonWidth, menuButtonHeight = 80, 40

# game states
PLAY = False
QUIT = False


def handle_quit():
    global QUIT

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            QUIT = True
    return True


class MainMenu:
    global play_button_image
    play_button_image = pygame.image.load("sprites/play_button.png").convert()

    global quit_button_image
    quit_button_image = pygame.image.load("sprites/quit_button.png").convert()

    # TODO: create a new menu background and update display function
    # TODO: force menu background image to tessellate if window resolution larger than image size?
    global menu_BG
    menu_BG = pygame.image.load("backgrounds/temp_grass_BG.png").convert()

    def __init__(self):
        self.buttonMargins = 15

        # "play" button positioned on left side of window
        # horizontal position is determined by buttonMargins, vertical position is mid-screen
        self.playButtonLocation = pygame.Rect((self.buttonMargins,
                                               (SCREEN_HEIGHT // 2) - (menuButtonHeight // 2)), (menuButtonWidth, menuButtonHeight))

        # "quit" button positioned on right side of window
        # horizontal position is determined by buttonMargins, vertical position is mid-screen
        self.quitButtonLocation = pygame.Rect((SCREEN_WIDTH - menuButtonWidth - self.buttonMargins, (SCREEN_HEIGHT // 2) - (menuButtonHeight // 2)),
                                              (menuButtonWidth, menuButtonHeight))

    def display(self):
        screen.blit(menu_BG, (0, 0))

        screen.blit(play_button_image, self.playButtonLocation)
        screen.blit(quit_button_image, self.quitButtonLocation)

    # TODO: visual indicator when mouse over button
    def checkButtons(self):
        global PLAY
        global QUIT

        # only check if LMB is pressed
        if not pygame.mouse.get_pressed()[0]:
            return

        if self.playButtonLocation.collidepoint(pygame.mouse.get_pos()):
            PLAY = True

        elif self.quitButtonLocation.collidepoint(pygame.mouse.get_pos()):
            QUIT = True


class Background:
    global temp_grass_BG
    temp_grass_BG = pygame.image.load("backgrounds/temp_grass_BG.png").convert()

    global grass_tile_0
    grass0 = pygame.image.load("sprites/grass_tile_0.png")

    def __init__(self):
        self.BGarray = []

    # TODO: define a function to generate a background randomly using grass tiles to use as a background


class Score:
    global numberSpriteSheet
    numberSpriteSheet = pygame.image.load("sprites/numbers_sprite_sheet.png").convert()

    def __init__(self, initial_score):
        self.val = initial_score

    def display(self):
        scoreArr = []
        divisor = 1

        while int(self.val / divisor) != 0:
            scoreArr.insert(0, int(self.val / divisor) % 10)
            divisor = divisor * 10

        # scoreArr is now a list containing each decimal of the score

        x_pos_score_blit = 0

        for i in scoreArr:
            screen.blit(numberSpriteSheet, (x_pos_score_blit, 0), (10 * i, 0, 10, 10))

            x_pos_score_blit = x_pos_score_blit + 10


class Meteor:
    global meteorSprite
    meteorSprite = pygame.image.load("sprites/basic_front.png").convert_alpha()

    # the smaller this number, the faster the meteors fall
    # TODO: make it such that a larger number means meteors fall faster
    global meteorSpeed
    meteorSpeed = 16

    # number of points scored when a meteor falls
    global meteorPoints
    meteorPoints = 50

    global craterList
    craterList = []

    global shadowRadius
    shadowRadius = meteorSpriteSize / 2

    def __init__(self):
        # position is a random location within the window bounds
        self.pos = (random.randint(0, SCREEN_WIDTH - meteorSpriteSize), random.randint(0, SCREEN_HEIGHT - meteorSpriteSize))
        self.hitbox = pygame.Rect(self.pos[0], self.pos[1], meteorSpriteSize, meteorSpriteSize)
        self.shadowCount = -1

    def hasFallen(self):
        return self.shadowCount >= meteorSpeed

    # TODO: rename function to shadowDisplay? separate into two functions?
    def shadowUpdate(self, screen):
        self.shadowCount = self.shadowCount + 1

        shadowTint = 255 - (self.shadowCount * (255 / meteorSpeed))

        pygame.draw.circle(screen,
                           (shadowTint, shadowTint, shadowTint),
                           (self.pos[0] + shadowRadius, self.pos[1] + shadowRadius),
                           shadowRadius)

    ### for debugging purposes
    def hitboxDebug(self):
        pygame.draw.rect(screen, (0, 255, 0), self.hitbox)


class Player:
    global faceNorth
    faceNorth = pygame.image.load("sprites/basic_back.png").convert_alpha()

    global faceSouth
    faceSouth = pygame.image.load("sprites/basic_front.png").convert_alpha()

    global faceWest
    faceWest = pygame.image.load("sprites/basic_side_l.png").convert_alpha()

    global faceEast
    faceEast = pygame.image.load("sprites/basic_side_r.png").convert_alpha()

    def __init__(self):
        # player starting position is in the center of the screen
        self.pos = ((SCREEN_WIDTH / 2) - (playerSpriteSize / 2), (SCREEN_HEIGHT / 2) - (playerSpriteSize / 2))
        self.playerSprite = faceSouth
        self.hitbox = pygame.Rect(self.pos[0], self.pos[1], playerSpriteSize, playerSpriteSize)

    def checkCollision(self, meteor):
        return pygame.Rect.colliderect(self.hitbox, meteor.hitbox)

    def move(self):
        pos = list(self.pos)

        # vertical movement
        # north
        if pygame.key.get_pressed()[K_w] and self.pos[1] > 0:
            pos[1] = pos[1] - 3
            self.playerSprite = faceNorth

        # south
        if pygame.key.get_pressed()[K_s] and self.pos[1] < SCREEN_HEIGHT - playerSpriteSize:
            pos[1] = pos[1] + 3
            self.playerSprite = faceSouth

        # horizontal movement
        # west
        if pygame.key.get_pressed()[K_a] and self.pos[0] > 0:
            pos[0] = pos[0] - 3
            self.playerSprite = faceWest

        # east
        if pygame.key.get_pressed()[K_d] and self.pos[0] < SCREEN_WIDTH - playerSpriteSize:
            pos[0] = pos[0] + 3
            self.playerSprite = faceEast

        self.pos = tuple(pos)
        self.hitbox = pygame.Rect(self.pos[0], self.pos[1], playerSpriteSize, playerSpriteSize)

    ### for debugging purposes
    def hitboxDebug(self):
        pygame.draw.rect(screen, (255, 0, 255), self.hitbox)


def main():

    pygame.init()

    mainMenu = MainMenu()

    score = Score(initial_score=0)
    meteor = Meteor()
    player = Player()

    while not QUIT and not PLAY:
        handle_quit()

        clock.tick(FPS)

        pygame.display.update()

        mainMenu.display()

        mainMenu.checkButtons()

    while not QUIT and PLAY:
        handle_quit()

        clock.tick(FPS)

        # TODO: display backdrop here
        pygame.display.update()
        screen.fill((255, 255, 255))

        if meteor.hasFallen():
            score.val = score.val + meteorPoints
            craterList.append(meteor)
            meteor = Meteor()

        meteor.shadowUpdate(screen)

        for c in craterList:
            # TODO: turn this into a function?
            screen.blit(meteorSprite, c.pos)
            if player.checkCollision(c):
                # TODO: trigger a "death"/continue/score screen here (within while loop until game quit or play again)

                ### for debugging purposes
                print("collision!")

        score.display()

        player.move()

        # TODO: turn this into a function?
        screen.blit(player.playerSprite, player.pos)


main()
