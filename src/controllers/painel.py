import pygame
from .services.botao import Botao

class Painel(object):
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.topright = (self.x, self.y)
        self.exibir = True
        
    def draw(self, surface):
        if self.exibir:
            pygame.draw.rect(surface, (90, 50, 10), self.rect)

    def alternar_exibicao(self):
        self.exibir = not self.exibir