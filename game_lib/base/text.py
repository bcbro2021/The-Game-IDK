import pygame

class Text:
    def __init__(self,text: str,fg_color: tuple,bg_color: tuple,size: int,pos: list) -> None:
        self.text = text
        self.fg = fg_color
        self.bg = bg_color
        self.size = size
        self.pos = pos
        self.fontpath = 'assets/font/font.ttf'

        self.font = pygame.font.Font(self.fontpath, size)
        self.ttext = self.font.render(text, False, fg_color, bg_color)
        self.textRect = self.ttext.get_rect()
        self.textRect.center = (pos[0],pos[1])
        if self.bg == (0,0,0):
            self.ttext.set_colorkey((0,0,0))
    def draw(self,surf: pygame.Surface) -> None:
        surf.blit(self.ttext,self.textRect)
    def update(self):
        self.textRect.center = (self.pos[0],self.pos[1])
        self.font = pygame.font.Font(self.fontpath, self.size)
        self.ttext = self.font.render(self.text, True, self.fg, self.bg)
    def clicked_on(self,event):
        retstat = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                pos = pygame.mouse.get_pos()
                if self.textRect.collidepoint(pos[0],pos[1]):
                    retstat = True

        return retstat