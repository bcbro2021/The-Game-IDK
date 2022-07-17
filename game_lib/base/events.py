from pyclbr import Function
import pygame

def quit_event(event,func: Function) -> None:
    if event.type == pygame.QUIT:
        func(event)

def keydown_event(event,func: Function) -> None:
    if event.type == pygame.KEYDOWN:
        func(event)
def keyup_event(event,func: Function) -> None:
    if event.type == pygame.KEYUP:
        func(event)
