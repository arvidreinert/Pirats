from setup import *
class Rectangle():
    def __init__(self, size, position, color, image):
        self.image = image
        self.rotation = 0
        self.is_updating = True
        self.size = size
        self.position = position
        self.transparency = 255
        self.color = color
        if not image:
            self.rect = pygame.Surface(size)
            self.rect.fill(self.color)
            self.position = position
            self.rect_rect = self.rect.get_rect()
            #self.rect_rect.center = self.position[0] - self.size[0] / 2, self.position[1] - self.size[1] / 2
            self.position = self.rect_rect.center
        else:
            self.position = position
            self.image = pygame.image.load(image).convert_alpha()
            self.image = pygame.transform.scale(self.image, size)
            self.image_rect = self.image.get_rect()
            self.image_rect.center = self.position[0]-self.size[0],self.position[1]-self.size[1]
            self.position = self.image_rect.center
        

    def update(self):
        if self.is_updating:
            surface.fill((0, 0, 0, 0))  # Clear the surface
            #some transforming:
            col = list(self.color)
            col.append(self.transparency)
            col = tuple(col)
            surface.set_alpha(self.transparency)
            if self.image != False:
                self.image_rect.center = self.position
                surface.blit(self.image, self.image_rect.center)
            else:
                self.rect_rect.center = self.position
                #self.position[0]-self.size[0], self.position[1]-self.size[1]
                surface.blit(self.rect, self.image_rect.center)
            screen.blit(surface, (0, 0))

    def set_transparency(self, transparency):
        self.transparency = transparency

    def set_position(self,xc,yc):
        self.position = xc, yc
        self.update()

    def change_position(self, xc, yc):
        self.position = self.position[0]+xc,self.position[1]+yc
        self.update()

    def kill(self):
        self.is_updating = False

    def set_rotation(self, rot):
        if self.image == False:
            self.rect = pygame.transform.rotate(self.rect, rot)
            self.rect_rect = self.rect.get_rect(center = self.rect_rect.center)
        else:
           self.image = pygame.transform.rotate(self.image, rot)
           self.image_rect = self.image.get_rect(center = self.image_rect.center)

    def get_pos(self):
        if self.image == False:
            return self.position
        else:
            return self.position

    def get_point_colide(self,point):
        if self.image != False:
            return self.image_rect.collidepoint(point)
        else:
            return self.rect_rect.collidepoint(point)
        
    def get_colliding_with(self,colrect):
        if self.image == False:
            return self.rect_rect.colliderect(colrect.rect_rect if not colrect.image else colrect.image_rect)
        else:
            return self.image_rect.colliderect(colrect.image_rect if not colrect.image else colrect.image_rect)