import os, json, pygame, sys, files, time
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2 as vector
from os.path import join
from os import walk
from random import randrange, randint, choice

resX, resY = 640, 480
FPS = 60
TILE_SIZE = 32
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
pygame.init()
screen = pygame.display.set_mode((resX, resY), pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Botomless Descent")