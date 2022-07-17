import pygame
import game_lib.base as gb

class Particle(gb.Entity):
    def __init__(self, pos=[0,0], size=[2,2],color=(255,255,255), img="none") -> None:
        super().__init__(pos, size, img)
        self.color = color
        self.alive_time = 12
        self.size_dec_time = self.alive_time // 2
        self.kill = False
    def update(self) -> None:
        self.alive_time -= 1
        self.size_dec_time -= 1
        if self.size_dec_time == 0:
            if self.rect.width > 1:
                self.rect.width -= 1
            if self.rect.height > 1:
                self.rect.height -= 1
        if self.alive_time == 0:
            self.kill = True
    def draw(self,surf: pygame.Surface) -> None:
        pygame.draw.rect(surf,self.color,self.rect)