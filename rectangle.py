from setup import *
import pygame

class Rectangle():
    def __init__(self, size, position, color, image=None):
        self.image_path = image
        self.rotation = 0
        self.is_updating = True
        self.size = size
        self.position = position
        self.transparency = 255
        self.color = color
        
        if not image:
            self.rect = pygame.Surface(size)
            self.rect.fill(self.color)
            self.rect.set_alpha(self.transparency)
            self.rect_rect = self.rect.get_rect(center=position)
        else:
            self.image = pygame.image.load(image).convert_alpha()
            self.image = pygame.transform.scale(self.image, size)
            self.image.set_alpha(self.transparency)
            self.image_rect = self.image.get_rect(center=position)
        
    def update(self, surface):
        if self.is_updating:
            if self.image_path is not None:
                surface.blit(self.image, self.image.get_rect(center=self.position))
            else:
                surface.blit(self.rect, self.rect.get_rect(center=self.position))
        
    def set_transparency(self, transparency):
        self.transparency = transparency
        if self.image_path is not None:
            self.image.set_alpha(transparency)
        else:
            self.rect.set_alpha(transparency)

    def set_position(self, xc, yc):
        self.position = (xc, yc)

    def change_position(self, xc, yc):
        self.position = (self.position[0] + xc, self.position[1] + yc)

    def kill(self):
        self.is_updating = False

    def change_rotation(self, rot):
        if self.image_path is not None:
            rotated_image = pygame.transform.rotate(self.image,rot)
            self.image = rotated_image
        else:
            rotated_image = pygame.transform.rotate(self.image,rot)
            self.image = rotated_image

    def get_pos(self):
        return self.position

    def get_point_collide(self, point):
        if self.image_path is not None:
            return self.image.get_rect(center=self.position).collidepoint(point)
        else:
            return self.rect.get_rect(center=self.position).collidepoint(point)
        
    def get_colliding_with(self, colrect):
        if self.image_path is not None:
            return self.image.get_rect(center=self.position).colliderect(colrect.self.image.get_rect(center=self.position) if colrect.image_path is not None else colrect.self.rect.get_rect(center=self.position))
        else:
            return self.rect.get_rect(self.position).colliderect(colrect.self.rect.get_rect(center=self.position) if colrect.image_path is None else colrect.self.image.get_rect(center=self.position))