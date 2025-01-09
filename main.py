import pygame
import sys
import numpy as np

from menus import StepEditWindow
from global_parameters import ScreenParameters

pygame.init()
screen = pygame.display.set_mode((ScreenParameters.width, ScreenParameters.height))
clock = pygame.time.Clock()


menu = StepEditWindow()

while True:
    events = [event for event in pygame.event.get()]
                
    if any(filter(lambda event: event.type == pygame.QUIT, events)):
        pygame.quit()
        sys.exit()
        
    menu.update(events)

    screen.fill(pygame.Color('gold'))
    
    menu.draw(screen)

    pygame.display.update()
    clock.tick(60)

