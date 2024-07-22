from operator import index
from screeninfo import get_monitors
import pygame, sys,random, math

#initialyse the module:
pygame.init()
pygame.mixer.init()
pygame.joystick.init()
my_screens = get_monitors()
width, height = (my_screens[0].width-100, my_screens[0].height-100)
screen = pygame.display.set_mode((width, height))
surface = pygame.Surface((width, height), pygame.SRCALPHA)
clock = pygame.time.Clock()
