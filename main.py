import pygame
import sys
import numpy as np

from menus import StepEditWindow
pygame.init()
screen = pygame.display.set_mode((1000, 800))
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

