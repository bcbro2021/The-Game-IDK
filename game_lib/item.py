import game_lib.base as gb
import pygame

class Item():
    def __init__(self) -> None:
        self.id = 0
        self.pos = [0,0]
        self.size = [8,8]
        self.damage = 0
        self.flip_x = False
        self.flip_y = False
        self.parent_entity = None
        self.instance = None
    def create_item(self,parent_entity=None,type="sword",id=0,texpath="none",damage=5) -> None:
        if type == "sword":
            self.id = id
            self.parent_entity = parent_entity
            self.damage = damage
            self.pos = [self.parent_entity.rect.x+(self.parent_entity.rect.width/2),self.parent_entity.rect.y+(self.parent_entity.rect.height/2)]
            self.instance = gb.Entity(pos=self.pos,size=self.size,img=texpath)
    def draw(self,win):
        self.instance.pos = self.pos
        self.instance.use_pos()
        win.blit(pygame.transform.flip(self.instance.img,self.flip_x,self.flip_y),self.instance.pos)
            