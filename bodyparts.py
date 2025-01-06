import pygame

class BodyPart():
    def __init__(self, surface, box, x=0, y=0, alpha=255):
        self.oryginal_surface = surface

        self.box = box
        self.alpha = alpha
        self.angle = 0

        self.surface = surface
        self.surface_rect = self.surface.get_rect(topleft = (x, y))

        self.update_draw_surface()


        # must be under update_draw_surface, needs rotated_surf
        self.update_allowed_position()
        self.update_allowed_angle()

    # -- changing placement
    def move(self, vector):
        self.surface_rect.move_ip(vector)
        self.update_draw_surface()

    def update_allowed_position(self):
        self.last_allowed_position = (self.rotated_rect.x, self.rotated_rect.y)

    def update_allowed_angle(self):
        self.last_allowed_angle = self.angle
    
    def change_angle(self, angle):
        self.angle = angle
        self.update_draw_surface()

    # -- utils
    def collide_point(self, pointer, position: tuple[2]):
        return self._collides_mask(pointer, tuple(pos - 1 for pos in position))
    
    def collides(self, other):

        if not isinstance(other, BodyPart):
            raise ValueError
        
        if self.__class__ != other.__class__:
            return False
        
        return self._collides_mask(other.mask, (other.rotated_rect.x, other.rotated_rect.y))
    
    def _collides_mask(self, other_mask: pygame.mask.Mask, position: tuple):
        return self.mask.overlap(other_mask, 
                          (position[0] - self.rotated_rect.x,
                           position[1] - self.rotated_rect.y)
        )

    # -- drawing
    def update_surface_alpha(self, alpha):
        self.alpha = alpha
        self.update_draw_surface()


    def update_draw_surface(self):
        self.rotated_surf = pygame.transform.rotate(self.surface, self.angle)
        
        self.rotated_surf.set_alpha(self.alpha)
        
        mask = pygame.transform.rotate(self.box, self.angle)
        self.mask = pygame.mask.from_surface(mask)

        self.rotated_rect = self.rotated_surf.get_rect(center = self.surface_rect.center)

    def draw(self, screen):
        # screen.blit(pygame.transform.rotate(self.box, self.angle), self.rotated_rect)
        screen.blit(self.rotated_surf, self.rotated_rect)


class Torso(BodyPart):

    def __init__(self, x=0, y=0):
        surface = pygame.Surface((200, 400), pygame.SRCALPHA)
        box = pygame.Surface((200, 400), pygame.SRCALPHA)
        pygame.draw.ellipse(box, pygame.Color('white'), (0, 0, *box.get_rect().size))
        super().__init__(surface, box, x, y)

        pygame.draw.ellipse(self.surface, pygame.Color('green'), (0, 0, *self.surface_rect.size), 3)
        pygame.draw.circle(self.surface, pygame.Color('green'), (self.surface_rect.size[0] / 2, self.surface_rect.size[1] / 2), 80, 3)
        
        
        self.update_draw_surface()
        


class Foot(BodyPart):
    def __init__(self, x=0, y=0, male=True, left=True):
        if male:
            image = pygame.image.load('male_footprint.png').convert_alpha()
            box = pygame.image.load('male_footprint_box.png').convert_alpha()
        else:
            image = pygame.image.load('female_footprint.png').convert_alpha()
            box = pygame.image.load('female_footprint_box.png').convert_alpha()
        
        if not left:
            image = pygame.transform.flip(image, True, False)
            box = pygame.transform.flip(box, True, False)

        image = pygame.transform.scale(image, (100, 200))
        box = pygame.transform.scale(box, (100, 200))
        
        super().__init__(image, box, x, y)



    def draw_texture_on_surface(self):
        pygame.draw.ellipse(self.surface, pygame.Color('red'), (0, 0, *self.surface_rect.size), 3)