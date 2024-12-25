import pygame
import sys
import numpy as np

pygame.init()
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()


class BodyPart():
    def __init__(self, x=0, y=0):
        self.surface = pygame.Surface((100, 200), pygame.SRCALPHA)
        self.surface_rect = self.surface.get_rect(topleft = (x, y))
        pygame.draw.ellipse(self.surface, pygame.Color('red'), (0, 0, *self.surface_rect.size), 3)
        self.angle = 0
        self.update_draw_surface()

    def update_draw_surface(self):
        self.rotated_surf = pygame.transform.rotate(self.surface, self.angle)
        self.rotated_rect = self.rotated_surf.get_rect(center = self.surface_rect.center)

    def draw(self, screen):
        # pygame.draw.rect(screen, pygame.SRCALPHA, self.rotated_rect)
        screen.blit(self.rotated_surf, self.rotated_rect)
    
    def change_angle(self, angle):
        self.angle = angle
        self.update_draw_surface()

    def collide_point(self, point: tuple[2]):
        return self.rotated_rect.collidepoint(point)

    def move(self, vector):
        print(vector)
        self.surface_rect.move_ip(vector)
        self.update_draw_surface()

    
parts = [BodyPart(), BodyPart(100)]
active_part = None
last_active = None
prev_position = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for num, part in enumerate(parts):
                    if part.collide_point(event.pos):
                        print(num)
                        active_part = num
                        last_active = active_part
                        prev_position = None
                        break
            if event.button == 3:
                prev_position = np.array(event.pos) - np.array(parts[last_active].surface_rect.center)
                prev_angle = parts[last_active].angle

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_part = None
            
            if event.button == 3:
                prev_position = None
        
        if event.type == pygame.MOUSEMOTION:
            if active_part != None:
                parts[active_part].move(event.rel)

            if last_active != None and isinstance(prev_position, np.ndarray):
                new_pos = np.array(event.pos) - np.array(parts[last_active].surface_rect.center)            
                v0 = prev_position
                v1 = new_pos
                #https://stackoverflow.com/questions/19852434/calculate-the-angle-between-2-vectors-clockwise-and-from-0-to-2pi
                
                
                # angle = np.mod( - np.arctan2(v0[0]*v1[1]-v1[0]*v0[1],v0[0]*v1[0]+v0[1]*v1[1]), 2*np.pi)
                # angle =  180 / np.pi * angle

                angle = np.mod(-np.arctan2(v0[0]*v1[1]-v1[0]*v0[1], np.sum(v0*(v1.T))), 2*np.pi) * 180/np.pi
                # . #trzeba zrobić z geometrycznych sprawdzenie czy wektor jest w górę czy w dół
                # 
                parts[last_active].change_angle(prev_angle + angle)
                

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    
    # if rotate:
    #     body_part.angle = (body_part.angle + 1)%360

    screen.fill(pygame.Color('gold'))
    for part in parts:
        part.draw(screen)
    # body_part._update_draw_surface()
    # body_part.draw(screen)
    pygame.display.update()
    clock.tick(60)

