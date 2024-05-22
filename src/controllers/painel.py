import pygame
from .services.texto import Texto

class Painel(object):
    def __init__(self, melhorias, x, y, width, height):
        self.melhorias = melhorias

        self.x, self.y = x, y
        self.width, self.height = width, height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.rect.topleft = (self.x, self.y)

        self.exibir = True
        
    def draw(self, surface, dinheiro_total):
        if self.exibir:
            pygame.draw.rect(surface, (90, 50, 10), self.rect)
            x, y = self.x, 150
            for melhoria in self.melhorias:
                self.melhorias[melhoria].draw_melhorias(surface, x, y, self.width, self.height, dinheiro_total)
                y += 100

    def alternar_exibicao(self):
        self.exibir = not self.exibir