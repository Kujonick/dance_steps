import pygame

class BodyPart():
    def __init__(self, surface, x=0, y=0):
        self.surface = surface
        self.surface_rect = self.surface.get_rect(topleft = (x, y))
        self.draw_texture_on_surface()
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


class Torso(BodyPart):
    def __init__(self, x=0, y=0):
        surface = pygame.Surface((200, 400), pygame.SRCALPHA)
        super().__init__(surface, x, y)
    def draw_texture_on_surface(self):
        pygame.draw.ellipse(self.surface, pygame.Color('green'), (0, 0, *self.surface_rect.size), 3)
        pygame.draw.circle(self.surface, pygame.Color('green'), (self.surface_rect.size[0] / 2, self.surface_rect.size[1] / 2), 80, 3)


class Foot(BodyPart):
    def __init__(self, x=0, y=0, male=True, left=True):
        if male:
            image = pygame.image.load('male_footprint.png').convert_alpha()
        else:
            image = pygame.image.load('female_footprint.png').convert_alpha()
        
        if not left:
            image = pygame.transform.flip(image, True, False)
        image = pygame.transform.scale(image, (100, 200))
        super().__init__(image, x, y)

    def draw_texture_on_surface(self):
        pygame.draw.ellipse(self.surface, pygame.Color('red'), (0, 0, *self.surface_rect.size), 3)