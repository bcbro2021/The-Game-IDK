import pygame

class Window:
    def __init__(self,size: tuple,title: str) -> None:
        self.size = size
        self.title = title
        self.win = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.title)
    def return_window(self) -> pygame.Surface:
        return self.win
