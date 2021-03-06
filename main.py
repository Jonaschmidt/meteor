'''
created by Jonas Schmidt on 6/26/2022
'''

from background import Background
import random
import pygame
from pygame.locals import *
import sys

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
tileSize = 32

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
    global main_menu_BG
    main_menu_BG = pygame.image.load("backgrounds/temp_main_menu_BG.png").convert()

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
        screen.blit(main_menu_BG, (0, 0))

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


class RetryMenu:
    # TODO: create new sprite for this
    global retry_button_image
    retry_button_image = pygame.image.load("sprites/retry_button.png").convert()

    global quit_button_image
    quit_button_image = pygame.image.load("sprites/quit_button.png").convert()

    # TODO: create a new menu background and update display function
    # TODO: force menu background image to tessellate if window resolution larger than image size?
    global retry_menu_BG
    retry_menu_BG = pygame.image.load("backgrounds/temp_retry_menu_BG.png").convert()

    def __init__(self):
        self.buttonMargins = 15

        # "play" button positioned on left side of window
        # horizontal position is determined by buttonMargins, vertical position is mid-screen
        self.retryButtonLocation = pygame.Rect((self.buttonMargins,
                                               (SCREEN_HEIGHT // 2) - (menuButtonHeight // 2)), (menuButtonWidth, menuButtonHeight))

        # "quit" button positioned on right side of window
        # horizontal position is determined by buttonMargins, vertical position is mid-screen
        self.quitButtonLocation = pygame.Rect((SCREEN_WIDTH - menuButtonWidth - self.buttonMargins, (SCREEN_HEIGHT // 2) - (menuButtonHeight // 2)),
                                              (menuButtonWidth, menuButtonHeight))

    def display(self, finalScore):
        screen.blit(retry_menu_BG, (0, 0))

        scoreArr = []
        divisor = 1

        # TODO: instead, use finalScore.display() with the optional argument once implemented...
        while int(finalScore.val / divisor) != 0:
            scoreArr.insert(0, int(finalScore.val / divisor) % 10)
            divisor = divisor * 10

        # scoreArr is now a list containing each decimal of the score

        # TODO: perhaps declare the size of the number sprite sheet and use that here and elsewhere
        x_pos_score_blit = (SCREEN_WIDTH / 2) - len(scoreArr) * 5
        y_pos_score_blit = (SCREEN_HEIGHT / 2) - 5

        for i in scoreArr:
            screen.blit(numberSpriteSheet, (x_pos_score_blit, y_pos_score_blit), (10 * i, 0, 10, 10))

            x_pos_score_blit = x_pos_score_blit + 10
        # ...

        screen.blit(retry_button_image, self.retryButtonLocation)
        screen.blit(quit_button_image, self.quitButtonLocation)

    # TODO: visual indicator when mouse over button
    def checkButtons(self):
        global PLAY
        global QUIT

        # only check if LMB is pressed
        if not pygame.mouse.get_pressed()[0]:
            return

        if self.retryButtonLocation.collidepoint(pygame.mouse.get_pos()):
            PLAY = True

        elif self.quitButtonLocation.collidepoint(pygame.mouse.get_pos()):
            QUIT = True


class Score:
    global numberSpriteSheet
    numberSpriteSheet = pygame.image.load("sprites/numbers_sprite_sheet.png").convert()

    def __init__(self, initial_score):
        self.val = initial_score

    # TODO: give this an optional argument: "position"
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
    meteorSprite = pygame.image.load("sprites/crater.png").convert_alpha()

    # the smaller this number, the faster the meteors fall
    # TODO: make it such that a larger number means meteors fall faster
    global meteorSpeed
    meteorSpeed = 16

    # number of points scored when a meteor falls
    global meteorPoints
    meteorPoints = 10

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

    def __init__(self, speed=3):
        self.speed = speed

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
            pos[1] = pos[1] - self.speed
            self.playerSprite = faceNorth

        # south
        if pygame.key.get_pressed()[K_s] and self.pos[1] < SCREEN_HEIGHT - playerSpriteSize:
            pos[1] = pos[1] + self.speed
            self.playerSprite = faceSouth

        # horizontal movement
        # west
        if pygame.key.get_pressed()[K_a] and self.pos[0] > 0:
            pos[0] = pos[0] - self.speed
            self.playerSprite = faceWest

        # east
        if pygame.key.get_pressed()[K_d] and self.pos[0] < SCREEN_WIDTH - playerSpriteSize:
            pos[0] = pos[0] + self.speed
            self.playerSprite = faceEast

        self.pos = tuple(pos)
        self.hitbox = pygame.Rect(self.pos[0], self.pos[1], playerSpriteSize, playerSpriteSize)

    def changeFace(self, direction):
        if direction == "north":
            self.playerSprite = faceNorth

        elif direction == "east":
            self.playerSprite = faceEast

        elif direction == "south":
            self.playerSprite = faceSouth

        elif direction == "west":
            self.playerSprite = faceWest

    def faceMouse(self):
        position = pygame.mouse.get_pos()

        x = position[0] - (self.pos[0])
        y = - (position[1] - (self.pos[1]))

        if y > x and y > (-x):
            self.playerSprite = faceNorth

        elif x > y > (-x):
            self.playerSprite = faceEast

        elif y < x and y < (-x):
            self.playerSprite = faceSouth

        elif x < y < (-x):
            self.playerSprite = faceWest

    def display(self):
        screen.blit(self.playerSprite, self.pos)

    ### for debugging purposes
    def hitboxDebug(self):
        pygame.draw.rect(screen, (255, 0, 255), self.hitbox)


def main():
    global PLAY
    global QUIT

    pygame.init()

    mainMenu = MainMenu()
    retryMenu = RetryMenu()

    player = Player()

    while not QUIT and not PLAY:
        handle_quit()

        clock.tick(FPS)

        pygame.display.update()

        mainMenu.display()

        player.faceMouse()
        player.display()

        mainMenu.checkButtons()

    gameBG = Background((SCREEN_WIDTH, SCREEN_HEIGHT), tileSize, "sprites/tiles", "backgrounds", "grass")
    gameBG.randomGeneration()

    while not QUIT:
        score = Score(initial_score=0)
        meteor = Meteor()

        while not QUIT and PLAY:
            handle_quit()

            clock.tick(FPS)

            pygame.display.update()

            gameBG.display(screen)

            if meteor.hasFallen():
                score.val = score.val + meteorPoints
                craterList.append(meteor)
                meteor = Meteor()

            meteor.shadowUpdate(screen)

            for c in craterList:
                # TODO: turn this into a function?
                screen.blit(meteorSprite, c.pos)
                if player.checkCollision(c):
                    PLAY = False

            score.val = score.val + 1

            score.display()

            player.move()

            player.display()

        while not QUIT and not PLAY:
            handle_quit()

            clock.tick(FPS)

            pygame.display.update()

            retryMenu.display(finalScore=score)

            retryMenu.checkButtons()

        player = Player()
        craterList.clear()


main()

pygame.quit()
sys.exit()
