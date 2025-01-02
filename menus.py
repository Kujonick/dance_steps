import pygame
import numpy as np

from bodyparts import Foot, Torso

class StepEditMenu():
    def __init__(self):
        self.active_part = None
        self.last_active = None
        self.prev_position = None
        self.prev_angle = None
        self.parts = [Foot(), Foot(100, left=False), Torso(200)]

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for num, part in enumerate(self.parts):
                        if part.collide_point(event.pos):
                            self.active_part = num
                            self.last_active = self.active_part
                            self.prev_position = None
                            break
                if event.button == 3:
                    self.prev_position = np.array(event.pos) - np.array(self.parts[self.last_active].surface_rect.center)
                    self.prev_angle = self.parts[self.last_active].angle

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.active_part = None
                
                if event.button == 3:
                    self.prev_position = None
            
            if event.type == pygame.MOUSEMOTION:
                if self.active_part != None:
                    self.parts[self.active_part].move(event.rel)

                if self.last_active != None and isinstance(self.prev_position, np.ndarray):
                    new_pos = np.array(event.pos) - np.array(self.parts[self.last_active].surface_rect.center)            
                    v0 = self.prev_position
                    v1 = new_pos
                    #https://stackoverflow.com/questions/19852434/calculate-the-angle-between-2-vectors-clockwise-and-from-0-to-2pi
                    angle = np.mod(-np.arctan2(v0[0]*v1[1]-v1[0]*v0[1], np.sum(v0*(v1.T))), 2*np.pi) * 180/np.pi

                    self.parts[self.last_active].change_angle(self.prev_angle + angle)

    def draw(self, screen):
        for part in self.parts:
            part.draw(screen)