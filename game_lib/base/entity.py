import pygame
import math

class Entity:
    def __init__(self,pos=[0,0],size=[0,0],img="none") -> None:
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(self.pos[0],self.pos[1],self.size[0],self.size[1])
        self.img = None
        if img != "none":
            self.img = pygame.image.load(img)

    def draw(self,win: pygame.Surface) -> None:
        if self.img == None:
            pygame.draw.rect(win,(255,0,0),self.rect)
        else:
            win.blit(self.img,self.pos)

    def collide_rect(self,entity) -> bool:
        return self.rect.colliderect(entity.rect)
    
    def collide_circle(self,center_x, center_y, radius):  # circle definition

        # complete boundbox of the rectangle
        rright, rbottom = self.rect.x + self.rect.width/2, self.rect.y + self.rect.height/2

        # bounding box of the circle
        cleft, ctop     = center_x-radius, center_y-radius
        cright, cbottom = center_x+radius, center_y+radius

        # trivial reject if bounding boxes do not intersect
        if rright < cleft or self.rect.x > cright or rbottom < ctop or self.rect.y > cbottom:
            return False  # no collision possible

        # check whether any point of rectangle is inside circle's radius
        for x in (self.rect.x, self.rect.x+self.rect.width):
            for y in (self.rect.y, self.rect.y+self.rect.height):
                # compare distance between circle's center point and each point of
                # the rectangle with the circle's radius
                if math.hypot(x-center_x, y-center_y) <= radius:
                    return True  # collision detected

        # check if center of circle is inside rectangle
        if self.rect.x <= center_x <= rright and self.rect.y <= center_y <= rbottom:
            return True  # overlaid

        return False

    def use_pos(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def clicked_on(self,event: pygame.event.Event) -> bool:
        retstat = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                pos = pygame.mouse.get_pos()
                if self.rect.collidepoint(pos[0],pos[1]):
                    retstat = True

        return retstat
