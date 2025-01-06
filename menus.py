import pygame
import numpy as np

from bodyparts import Foot, Torso, BodyPart

class Tick():
    def __init__(self, pointer, both_partners=True):

        self.active_part: BodyPart= None     # part that is currently moved
        self.last_active: BodyPart= None     # part that was moved last
        self.prev_position = None   # first position when mouse started rotating
        self.prev_angle = None      # angle, from which part started rotating

        # parts inluded in the tick
        self.parts = [Foot(), 
                      Foot(100, left=False),
                      ]

        if both_partners:
            self.parts.extend([Foot(0, 200, male=False), 
                               Foot(100, 200, male=False, left=False)])
            
        self.parts.append(Torso())
        self.parts.append(Torso(200))
        # self.foots = list(filter(lambda x: isinstance(x, Foot), self.parts))

        self.pointer = pointer

    def check_for_collision(self, part):
        for foot in self.parts:
            if foot == part:
                continue
            
            if part.collides(foot):
                return True
        return False
    
    def history_steps(self, behind: int):
        new_alpha = 255 // (behind + 1) ** 2 if behind >= 0 else 0
        for part in self.parts:
            part.update_surface_alpha(new_alpha)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for num, part in enumerate(self.parts):
                        if part.collide_point(self.pointer, event.pos):
                            self.active_part = part
                            self.last_active = self.active_part
                            self.prev_position = None
                            break

                if event.button == 3:
                    if self.last_active is None:
                        continue
                    self.prev_position = np.array(event.pos) - np.array(self.last_active.surface_rect.center)
                    self.prev_angle = self.last_active.angle

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.active_part != None:
                    
                    allowed_pos = self.active_part.last_allowed_position
                    rect = self.active_part.rotated_rect
                    vector = (allowed_pos[0] - rect.x, allowed_pos[1] - rect.y)
                    self.active_part.move(vector)
                    
                    self.active_part = None
                
                if event.button == 3 and self.last_active != None:
                    self.last_active.angle = self.last_active.last_allowed_angle
                    self.last_active.update_draw_surface()
                    
                    self.prev_position = None
            
            if event.type == pygame.MOUSEMOTION:
                if self.active_part != None:
                    self.active_part.move(event.rel)

                    if not self.check_for_collision(self.active_part):
                        self.active_part.update_allowed_position()

                if self.last_active != None and isinstance(self.prev_position, np.ndarray):
                    new_pos = np.array(event.pos) - np.array(self.last_active.surface_rect.center)            
                    v0 = self.prev_position
                    v1 = new_pos
                    #https://stackoverflow.com/questions/19852434/calculate-the-angle-between-2-vectors-clockwise-and-from-0-to-2pi
                    angle = np.mod(-np.arctan2(v0[0]*v1[1]-v1[0]*v0[1], np.sum(v0*(v1.T))), 2*np.pi) * 180/np.pi

                    self.last_active.change_angle(self.prev_angle + angle)

                    if not self.check_for_collision(self.last_active):
                        self.last_active.update_allowed_angle()



    def draw(self, screen):
        for part in self.parts:
            part.draw(screen) 
        

class StepEditWindow():
    def __init__(self):
        pointer = pygame.surface.Surface((3, 3))
        pointer.fill('white')
        self.pointer = pygame.mask.from_surface(pointer)


        self.ticks = [  Tick(self.pointer),
                        Tick(self.pointer),
                        Tick(self.pointer)]
        self.active_tick = len(self.ticks) - 1

        self.update_history()

    def update_history(self):
        for i in range(min(self.active_tick + 2, len(self.ticks))):
            self.ticks[i].history_steps(self.active_tick - i)  

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.active_tick = min(len(self.ticks) - 1, self.active_tick + 1)

                if event.key == pygame.K_DOWN:
                    self.active_tick = max(0, self.active_tick - 1)


            self.update_history()

        self.ticks[self.active_tick].update(events)

    def draw(self, screen):
        for tick in self.ticks:
            tick.draw(screen)