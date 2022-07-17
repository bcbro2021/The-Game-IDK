import pygame
import game_lib.base as gb

class round_light():
    def __init__(self,glow,radius):
        self.lighting_surf = pygame.Surface((radius*2,radius*2))
        layers = 25
        glow = gb.clamp(glow,0,255)
        for i in range(layers):
            k = i * glow
            k = gb.clamp(k,0,255)
            pygame.draw.circle (self.lighting_surf,(k,k,k),self.lighting_surf.get_rect().center,radius - i * 3)
    def create(self):
        return self.lighting_surf