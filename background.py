'''
created by Jonas Schmidt on 7/4/2022
'''

import os
import pygame
import random


class Background:

    def __init__(self, resolution, tile_size, path_to_tiles_directory="tiles", path="backgrounds", tileset="test"):
        self.resolution = resolution
        self.tileSize = tile_size
        self.path_to_tiles_directory = path_to_tiles_directory
        self.path = path
        self.tileset = tileset

        self.tiles = []
        self.surface = pygame.display.set_mode((resolution[0], resolution[1]), 0, 32)
        self.image = 0

    def randomGeneration(self):
        path = self.path_to_tiles_directory + "/" + self.tileset + "/"
        tiles = os.listdir(path)

        for i in range(len(tiles)):
            tiles[i] = pygame.image.load(path + tiles[i]).convert_alpha()

        print("tiles array initialized")

        i = 0
        j = 0
        while i < self.resolution[0]:

            while j < self.resolution[1]:
                self.surface.blit(tiles[random.randint(0, len(tiles) - 1)], (i, j))
                j = j + self.tileSize

            j = 0
            i = i + self.tileSize

        path = self.path + "/" + self.tileset + "BG.png"

        pygame.image.save_extended(self.surface, path)
        self.image = pygame.image.load(path)

    def display(self, surface):
        surface.blit(self.image, (0, 0))
