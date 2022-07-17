import pygame

def load_image(path: str) -> pygame.Surface:
    return pygame.image.load(path)

def load_image_at(sheet: pygame.Surface,rectangle: tuple) -> pygame.Surface:
    rect = pygame.Rect(rectangle)
    image = pygame.Surface(rect.size).convert()
    image.blit(sheet, (0, 0), rect)

    return image